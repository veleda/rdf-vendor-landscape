#!/usr/bin/env python3
"""
One-time migration: converts vendors.json into vendors.ttl (the new source of truth).

Ontology design:
  @base          <http://data.veronahe.no/vendors/>     -- vendor instances
  vl:            <http://data.veronahe.no/vocab#>       -- classes & properties
  focus:         <http://data.veronahe.no/focus/>        -- focus-area instances
  std:           <http://data.veronahe.no/standard/>     -- W3C standard instances
  region:        <http://data.veronahe.no/region/>       -- region instances
  country:       <http://data.veronahe.no/country/>      -- country instances
  speed:         <http://data.veronahe.no/speed/>        -- speed-tier instances
  scale:         <http://data.veronahe.no/scale/>        -- scale-tier instances
"""

import json, re, pathlib

HERE = pathlib.Path(__file__).parent
VENDORS_JSON = HERE / "vendors.json" if (HERE / "vendors.json").exists() else HERE.parent / "vendors.json"

# ---------------------------------------------------------------------------
# IRI helpers
# ---------------------------------------------------------------------------

def slugify(text: str) -> str:
    """Turn a human string into a Turtle-safe local name (must start with a letter)."""
    s = text.strip()
    s = re.sub(r"[/\\()]+", "-", s)
    s = re.sub(r"[^a-zA-Z0-9_-]", "-", s)
    s = re.sub(r"-{2,}", "-", s)
    s = s.strip("-")
    # Turtle local names must start with a letter or underscore
    if s and not s[0].isalpha() and s[0] != "_":
        s = "_" + s
    return s


def esc_turtle(s: str) -> str:
    """Escape a string for Turtle literal."""
    return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")


W3C_STANDARD_IRIS = {
    "RDF 1.1":      "https://www.w3.org/TR/rdf11-concepts/",
    "RDF-star":     "https://www.w3.org/TR/rdf-star/",
    "SPARQL 1.1":   "https://www.w3.org/TR/sparql11-query/",
    "SPARQL-star":  "https://www.w3.org/TR/sparql-star/",
    "OWL 2":        "https://www.w3.org/TR/owl2-overview/",
    "SHACL":        "https://www.w3.org/TR/shacl/",
    "SKOS":         "https://www.w3.org/TR/skos-reference/",
    "R2RML":        "https://www.w3.org/TR/r2rml/",
    "RML":          "https://rml.io/specs/rml/",
    "JSON-LD":      "https://www.w3.org/TR/json-ld11/",
    "CSVW":         "https://www.w3.org/TR/tabular-data-primer/",
    "N3":           "https://www.w3.org/TeamSubmission/n3/",
    "LDP":          "https://www.w3.org/TR/ldp/",
}


# ---------------------------------------------------------------------------
# Build the Turtle
# ---------------------------------------------------------------------------

def build_turtle(vendors: list[dict]) -> str:
    lines = []

    # -- Prefixes -----------------------------------------------------------
    lines.append("@base          <http://data.veronahe.no/vendors/> .")
    lines.append("@prefix vl:      <http://data.veronahe.no/vocab#> .")
    lines.append("@prefix focus:   <http://data.veronahe.no/focus/> .")
    lines.append("@prefix std:     <http://data.veronahe.no/standard/> .")
    lines.append("@prefix region:  <http://data.veronahe.no/region/> .")
    lines.append("@prefix country: <http://data.veronahe.no/country/> .")
    lines.append("@prefix speed:   <http://data.veronahe.no/speed/> .")
    lines.append("@prefix scale:   <http://data.veronahe.no/scale/> .")
    lines.append("@prefix schema:  <https://schema.org/> .")
    lines.append("@prefix rdfs:    <http://www.w3.org/2000/01/rdf-schema#> .")
    lines.append("@prefix rdf:     <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .")
    lines.append("@prefix xsd:     <http://www.w3.org/2001/XMLSchema#> .")
    lines.append("@prefix owl:     <http://www.w3.org/2002/07/owl#> .")
    lines.append("")

    # -- Ontology header ----------------------------------------------------
    lines.append("# ======================================================================")
    lines.append("# Ontology: RDF Vendor Landscape vocabulary")
    lines.append("# ======================================================================")
    lines.append("")
    lines.append("vl:Vendor       a owl:Class ; rdfs:label \"Vendor\" .")
    lines.append("vl:Database     a owl:Class ; rdfs:subClassOf vl:Vendor ; rdfs:label \"Database\" .")
    lines.append("vl:Framework    a owl:Class ; rdfs:subClassOf vl:Vendor ; rdfs:label \"Framework\" .")
    lines.append("vl:Tool         a owl:Class ; rdfs:subClassOf vl:Vendor ; rdfs:label \"Tool\" .")
    lines.append("")
    lines.append("vl:FocusArea    a owl:Class ; rdfs:label \"Focus Area\" .")
    lines.append("vl:Standard     a owl:Class ; rdfs:label \"W3C/Community Standard\" .")
    lines.append("vl:Region       a owl:Class ; rdfs:label \"Region\" .")
    lines.append("vl:Country      a owl:Class ; rdfs:label \"Country\" .")
    lines.append("vl:SpeedTier    a owl:Class ; rdfs:label \"Speed Tier\" .")
    lines.append("vl:ScaleTier    a owl:Class ; rdfs:label \"Scale Tier\" .")
    lines.append("")

    # Properties
    props = [
        ("vl:subcategory",      "owl:DatatypeProperty", "Subcategory"),
        ("vl:language",         "owl:DatatypeProperty", "Programming language(s)"),
        ("vl:license",          "owl:DatatypeProperty", "License"),
        ("vl:pricing",          "owl:DatatypeProperty", "Pricing model"),
        ("vl:github",           "owl:DatatypeProperty", "GitHub URL"),
        ("vl:hasDemo",          "owl:DatatypeProperty", "Has a demo available"),
        ("vl:demoUrl",          "owl:DatatypeProperty", "Demo URL"),
        ("vl:hasBenchmark",     "owl:DatatypeProperty", "Included in benchmark"),
        ("vl:logoHint",         "owl:DatatypeProperty", "Logo search hint"),
        ("vl:logoUrl",          "owl:DatatypeProperty", "Logo URL"),
        ("vl:speedNote",        "owl:DatatypeProperty", "Speed description"),
        ("vl:scaleNote",        "owl:DatatypeProperty", "Scale description"),
        ("vl:warning",          "owl:DatatypeProperty", "Warning note"),
        ("vl:flag",             "owl:DatatypeProperty", "Emoji flag"),
        ("vl:focusArea",        "owl:ObjectProperty",   "Focus area"),
        ("vl:supportsStandard", "owl:ObjectProperty",   "Supports standard"),
        ("vl:region",           "owl:ObjectProperty",   "Region"),
        ("vl:country",          "owl:ObjectProperty",   "Country"),
        ("vl:speedTier",        "owl:ObjectProperty",   "Speed tier"),
        ("vl:scaleTier",        "owl:ObjectProperty",   "Scale tier"),
    ]
    for iri, ptype, label in props:
        lines.append(f'{iri} a {ptype} ; rdfs:label "{label}" .')
    lines.append("")

    # -- Controlled-vocabulary instances ------------------------------------
    lines.append("# ======================================================================")
    lines.append("# Controlled vocabularies (IRIs for filters)")
    lines.append("# ======================================================================")
    lines.append("")

    # Collect all unique values
    all_focus = sorted({fa for v in vendors for fa in v.get("focusAreas", [])})
    all_stds = sorted({s for v in vendors for s in v.get("standards", [])})
    all_regions = sorted({v["region"] for v in vendors if v.get("region")})
    all_countries = sorted({(v["country"], v.get("flag", "")) for v in vendors if v.get("country")})
    all_speed = sorted({v["speedTier"] for v in vendors if v.get("speedTier")})
    all_scale = sorted({v["scaleTier"] for v in vendors if v.get("scaleTier")})

    lines.append("# -- Focus areas -------------------------------------------------------")
    for fa in all_focus:
        slug = slugify(fa)
        lines.append(f'focus:{slug}  a vl:FocusArea ; rdfs:label "{esc_turtle(fa)}" .')
    lines.append("")

    lines.append("# -- Standards ---------------------------------------------------------")
    for s in all_stds:
        slug = slugify(s)
        w3c = W3C_STANDARD_IRIS.get(s)
        see_also = f" ;\n    rdfs:seeAlso <{w3c}>" if w3c else ""
        lines.append(f'std:{slug}  a vl:Standard ; rdfs:label "{esc_turtle(s)}"{see_also} .')
    lines.append("")

    lines.append("# -- Regions -----------------------------------------------------------")
    for r in all_regions:
        slug = slugify(r)
        lines.append(f'region:{slug}  a vl:Region ; rdfs:label "{esc_turtle(r)}" .')
    lines.append("")

    lines.append("# -- Countries ---------------------------------------------------------")
    for cname, flag in all_countries:
        slug = slugify(cname)
        flag_triple = f' ; vl:flag "{esc_turtle(flag)}"' if flag else ""
        lines.append(f'country:{slug}  a vl:Country ; rdfs:label "{esc_turtle(cname)}"{flag_triple} .')
    lines.append("")

    lines.append("# -- Speed tiers -------------------------------------------------------")
    for t in all_speed:
        slug = slugify(t)
        lines.append(f'speed:{slug}  a vl:SpeedTier ; rdfs:label "{esc_turtle(t)}" .')
    lines.append("")

    lines.append("# -- Scale tiers -------------------------------------------------------")
    for t in all_scale:
        slug = slugify(t)
        lines.append(f'scale:{slug}  a vl:ScaleTier ; rdfs:label "{esc_turtle(t)}" .')
    lines.append("")

    # -- Vendor instances ---------------------------------------------------
    lines.append("# ======================================================================")
    lines.append("# Vendor instances")
    lines.append("# ======================================================================")

    cat_class = {"database": "vl:Database", "framework": "vl:Framework", "tool": "vl:Tool"}

    for v in sorted(vendors, key=lambda x: x["name"].lower()):
        slug = slugify(v["name"])
        cls = cat_class[v["category"]]

        lines.append("")
        lines.append(f"<{slug}>  a {cls} ;")
        lines.append(f'    schema:name        "{esc_turtle(v["name"])}" ;')
        lines.append(f'    schema:description "{esc_turtle(v["description"])}" ;')
        lines.append(f'    schema:url         <{v["website"]}> ;')

        if v.get("subcategory"):
            lines.append(f'    vl:subcategory     "{esc_turtle(v["subcategory"])}" ;')
        if v.get("language"):
            lines.append(f'    vl:language         "{esc_turtle(v["language"])}" ;')
        if v.get("license"):
            lines.append(f'    vl:license          "{esc_turtle(v["license"])}" ;')
        if v.get("pricing"):
            lines.append(f'    vl:pricing          "{esc_turtle(v["pricing"])}" ;')
        if v.get("github"):
            lines.append(f'    vl:github           <{v["github"]}> ;')
        if v.get("logoHint"):
            lines.append(f'    vl:logoHint         "{esc_turtle(v["logoHint"])}" ;')
        if v.get("logoUrl"):
            lines.append(f'    vl:logoUrl          <{v["logoUrl"]}> ;')

        # Booleans (Turtle native keywords)
        lines.append(f'    vl:hasDemo          {"true" if v.get("hasDemo") else "false"} ;')
        if v.get("demoUrl"):
            lines.append(f'    vl:demoUrl          <{v["demoUrl"]}> ;')
        lines.append(f'    vl:hasBenchmark     {"true" if v.get("hasBenchmark") else "false"} ;')

        # Speed / scale
        if v.get("speedNote"):
            lines.append(f'    vl:speedNote        "{esc_turtle(v["speedNote"])}" ;')
        if v.get("scaleNote"):
            lines.append(f'    vl:scaleNote        "{esc_turtle(v["scaleNote"])}" ;')
        if v.get("speedTier"):
            lines.append(f'    vl:speedTier        speed:{slugify(v["speedTier"])} ;')
        if v.get("scaleTier"):
            lines.append(f'    vl:scaleTier        scale:{slugify(v["scaleTier"])} ;')

        # Warning
        if v.get("warning"):
            lines.append(f'    vl:warning          "{esc_turtle(v["warning"])}" ;')

        # Region / country
        if v.get("region"):
            lines.append(f'    vl:region           region:{slugify(v["region"])} ;')
        if v.get("country"):
            lines.append(f'    vl:country          country:{slugify(v["country"])} ;')

        # Focus areas (object links)
        for fa in v.get("focusAreas", []):
            lines.append(f"    vl:focusArea        focus:{slugify(fa)} ;")

        # Standards (object links)
        for s in v.get("standards", []):
            lines.append(f"    vl:supportsStandard std:{slugify(s)} ;")

        # Close the resource: replace last " ;" with " ."
        if lines[-1].endswith(" ;"):
            lines[-1] = lines[-1][:-2] + " ."
        else:
            lines.append(".")

    lines.append("")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    with open(VENDORS_JSON) as f:
        vendors = json.load(f)

    ttl = build_turtle(vendors)
    out = HERE / "vendors.ttl"
    out.write_text(ttl, encoding="utf-8")
    print(f"Wrote {len(vendors)} vendors to {out} ({out.stat().st_size:,} bytes)")
