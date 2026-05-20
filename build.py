#!/usr/bin/env python3
"""
Build step: reads vendors.ttl (the RDF source of truth) via maplib,
reconstructs the VENDORS JS array, and injects it into index.html.

Usage:
    python build.py              # reads vendors.ttl, patches index.html
    python build.py --check      # dry-run: prints JSON but does not write
"""

import json, re, sys, pathlib
from maplib import Model

HERE = pathlib.Path(__file__).parent
TTL_PATH  = HERE / "vendors.ttl"
HTML_PATH = HERE / "index.html"

PREFIXES = """
PREFIX vl:      <http://data.veronahe.no/vocab#>
PREFIX schema:  <https://schema.org/>
PREFIX rdfs:    <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd:     <http://www.w3.org/2001/XMLSchema#>
"""

# Maps the RDF class IRI label back to the JS category string
CLASS_TO_CATEGORY = {
    "Database":  "database",
    "Framework": "framework",
    "Tool":      "tool",
}


def strip_iri(val):
    """Strip <> brackets from IRI strings returned by maplib."""
    if val and isinstance(val, str) and val.startswith("<") and val.endswith(">"):
        return val[1:-1]
    return val


def load_model() -> Model:
    m = Model()
    m.read(str(TTL_PATH))
    return m


def query_vendors(m: Model) -> list[dict]:
    """Run SPARQL queries and assemble the vendor dicts matching the JS schema."""

    # --- 1. Scalar properties per vendor ----------------------------------
    scalars = m.query(PREFIXES + """
        SELECT ?v ?name ?desc ?url ?cat
               ?subcategory ?language ?license ?pricing
               ?github ?logoHint ?logoUrl
               ?hasDemo ?demoUrl ?hasBenchmark
               ?speedNote ?scaleNote ?warning
               ?speedLabel ?scaleLabel
               ?regionLabel ?countryLabel ?flag
               ?firstRelease ?reviewUrl
        WHERE {
            ?v a ?cls .
            ?cls rdfs:subClassOf vl:Vendor ; rdfs:label ?cat .
            ?v schema:name ?name ;
               schema:description ?desc ;
               schema:url ?url .
            OPTIONAL { ?v vl:subcategory ?subcategory }
            OPTIONAL { ?v vl:language    ?language }
            OPTIONAL { ?v vl:license     ?license }
            OPTIONAL { ?v vl:pricing     ?pricing }
            OPTIONAL { ?v vl:github      ?github }
            OPTIONAL { ?v vl:logoHint    ?logoHint }
            OPTIONAL { ?v vl:logoUrl     ?logoUrl }
            OPTIONAL { ?v vl:hasDemo     ?hasDemo }
            OPTIONAL { ?v vl:demoUrl     ?demoUrl }
            OPTIONAL { ?v vl:hasBenchmark ?hasBenchmark }
            OPTIONAL { ?v vl:speedNote   ?speedNote }
            OPTIONAL { ?v vl:scaleNote   ?scaleNote }
            OPTIONAL { ?v vl:warning     ?warning }
            OPTIONAL { ?v vl:speedTier   ?st . ?st rdfs:label ?speedLabel }
            OPTIONAL { ?v vl:scaleTier   ?sc . ?sc rdfs:label ?scaleLabel }
            OPTIONAL { ?v vl:region      ?rg . ?rg rdfs:label ?regionLabel }
            OPTIONAL { ?v vl:country     ?co . ?co rdfs:label ?countryLabel }
            OPTIONAL { ?v vl:country     ?co2 . ?co2 vl:flag ?flag }
            OPTIONAL { ?v vl:firstRelease ?firstRelease }
            OPTIONAL { ?v vl:reviewUrl ?reviewUrl }
        }
    """)

    # --- 2. Multi-valued: focusAreas per vendor ---------------------------
    focus_df = m.query(PREFIXES + """
        SELECT ?v ?label WHERE {
            ?v vl:focusArea ?fa .
            ?fa rdfs:label ?label .
        } ORDER BY ?v ?label
    """)

    # --- 3. Multi-valued: standards per vendor ----------------------------
    stds_df = m.query(PREFIXES + """
        SELECT ?v ?label WHERE {
            ?v vl:supportsStandard ?s .
            ?s rdfs:label ?label .
        } ORDER BY ?v ?label
    """)

    # Build lookup dicts: vendor IRI -> list of strings
    focus_map: dict[str, list[str]] = {}
    for row in focus_df.iter_rows(named=True):
        focus_map.setdefault(row["v"], []).append(row["label"])

    stds_map: dict[str, list[str]] = {}
    for row in stds_df.iter_rows(named=True):
        stds_map.setdefault(row["v"], []).append(row["label"])

    # --- 4. Assemble vendor dicts -----------------------------------------
    vendors = []
    for row in scalars.iter_rows(named=True):
        v_iri = row["v"]
        v = {
            "name":         row["name"],
            "category":     CLASS_TO_CATEGORY.get(row["cat"], row["cat"].lower()),
            "subcategory":  row.get("subcategory") or "",
            "language":     row.get("language") or "",
            "license":      row.get("license") or "",
            "pricing":      row.get("pricing") or "",
            "website":      strip_iri(row.get("url") or ""),
            "github":       strip_iri(row.get("github") or ""),
            "description":  row.get("desc") or "",
            "hasDemo":      bool(row.get("hasDemo")),
            "demoUrl":      strip_iri(row.get("demoUrl")) or None,
            "hasBenchmark": bool(row.get("hasBenchmark")),
            "logoHint":     row.get("logoHint") or "",
            "logoUrl":      strip_iri(row.get("logoUrl") or ""),
            "focusAreas":   focus_map.get(v_iri, []),
            "speedNote":    row.get("speedNote") or "",
            "scaleNote":    row.get("scaleNote") or "",
            "standards":    stds_map.get(v_iri, []),
            "region":       row.get("regionLabel") or "",
            "country":      row.get("countryLabel") or "",
            "flag":         row.get("flag") or "",
            "speedTier":    row.get("speedLabel") or "",
            "scaleTier":    row.get("scaleLabel") or "",
            "firstRelease": int(row["firstRelease"]) if row.get("firstRelease") else None,
            "reviewUrl":    strip_iri(row.get("reviewUrl") or "") or None,
        }
        if row.get("warning"):
            v["warning"] = row["warning"]
        vendors.append(v)

    vendors.sort(key=lambda x: x["name"].lower())
    return vendors


def vendors_to_js(vendors: list[dict]) -> str:
    """Format vendor list as the JS constant for embedding in HTML."""
    lines = ["const VENDORS = ["]
    for v in vendors:
        lines.append("  " + json.dumps(v, ensure_ascii=False) + ",")
    lines.append("];")
    return "\n".join(lines)


def inject_into_html(js_block: str) -> None:
    """Replace the VENDORS array in index.html with the new data."""
    html = HTML_PATH.read_text(encoding="utf-8")
    pattern = r"const VENDORS = \[.*?\];"
    match = re.search(pattern, html, re.DOTALL)
    if not match:
        raise RuntimeError("Could not find 'const VENDORS = [...];\' block in index.html")
    html = html[:match.start()] + js_block + html[match.end():]
    HTML_PATH.write_text(html, encoding="utf-8")


def main():
    check_only = "--check" in sys.argv

    print(f"Reading {TTL_PATH} ...")
    m = load_model()
    vendors = query_vendors(m)
    print(f"Queried {len(vendors)} vendors from RDF")

    js = vendors_to_js(vendors)

    if check_only:
        print("\n--- JS output (dry run, not written) ---")
        print(js[:2000], "..." if len(js) > 2000 else "")
        print(f"\nTotal JS size: {len(js):,} chars")
    else:
        inject_into_html(js)
        print(f"Injected into {HTML_PATH} ({HTML_PATH.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
