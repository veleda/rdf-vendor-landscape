# RDF Vendor Landscape

A comprehensive, interactive guide to 68 databases, frameworks, and tools in the RDF and semantic web ecosystem. Built as a single-page website with filtering, comparison, benchmarks, and an in-browser SPARQL editor.

**Live site:** [rdf-vendor-landscape](https://veleda.github.io/rdf-vendor-landscape/)


## How it works

All vendor data lives in a single RDF file (`vendors.ttl`), which serves as the source of truth. A build script reads the Turtle file using [maplib](https://github.com/DataTreehouse/maplib), runs SPARQL queries to extract structured data, and injects the result as a JavaScript array into `index.html`.

```
vendors.ttl  -->  build.py (maplib + SPARQL)  -->  index.html
```

The website is fully self-contained: one HTML file, no server required.


## Project structure

| File | Purpose |
|---|---|
| `vendors.ttl` | RDF source of truth for all vendor data |
| `build.py` | Build script: TTL to JS injection via maplib |
| `index.html` | The complete single-page website |


## Contributing

Contributions are welcome and encouraged! Whether you want to add a missing vendor, correct a description, update a license, or fix a broken link, your help makes this resource better for everyone.

### Adding or updating a vendor

1. Edit `vendors.ttl` directly. Each vendor is a block of RDF triples following a consistent pattern. Look at any existing vendor entry as a template.

2. Run the build to regenerate the site:

```bash
pip install maplib
python build.py
```

3. Open `index.html` in your browser to verify the changes look right.

4. Submit a pull request with a short note about what you changed and why.

### What to contribute

- **New vendors** you think belong in the landscape
- **Corrections** to descriptions, standards tags, licensing, or pricing
- **Updated links** if a project has moved or a demo URL has changed
- **Release year fixes** if a "Since YYYY" date is off
- **Regional or country corrections** for vendor headquarters
- **Benchmark data** if you have run the [trainmarks](https://github.com/DataTreehouse/trainmarks) suite against an RDF store not yet included

### Guidelines

- Keep descriptions factual and concise. Avoid marketing language.
- Standards tags (RDF 1.1, SPARQL 1.1, OWL 2, SHACL, etc.) should reflect what the vendor actually implements, not what it plans to support.
- When in doubt, link to the source that supports your claim.
- One vendor per pull request makes review easier, but batches are fine too.


## Running locally

The site is a single HTML file. Open it directly in your browser:

```bash
open index.html        # macOS
xdg-open index.html    # Linux
```

To rebuild after editing `vendors.ttl`:

```bash
pip install maplib
python build.py
```

The build script requires Python 3.10+ and maplib.


## License

The vendor data and website code are open for reuse. See individual vendor entries for their respective licenses and trademarks.
