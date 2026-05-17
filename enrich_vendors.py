import json

with open("/sessions/zen-gracious-shannon/mnt/rdf vendor landscape/vendors.json") as f:
    vendors = json.load(f)

# Enrichment data: focusAreas, speedNote, scaleNote
# speedNote: honest take on speed characteristics
# scaleNote: honest take on scalability
# focusAreas: what the vendor is best at / designed for

enrichment = {
    "maplib": {
        "focusAreas": ["OTTR templates", "DataFrame-to-RDF", "SPARQL", "Knowledge graph construction", "SHACL validation"],
        "speedNote": "Very fast — Rust core with Polars/Arrow gives near-native I/O and sub-second SPARQL on millions of triples",
        "scaleNote": "In-memory by default, so bounded by RAM. Disk mode trades ~2-3x speed for larger-than-memory datasets"
    },
    "Oxigraph": {
        "focusAreas": ["SPARQL 1.1", "Embedded database", "RDF storage", "Python/JS bindings"],
        "speedNote": "Good read/write performance from Rust + RocksDB. Mid-pack on SPARQL queries — solid but not the fastest",
        "scaleNote": "Disk-backed via RocksDB, handles tens of millions of triples well. Not designed for billion-triple scale"
    },
    "rdflib": {
        "focusAreas": ["RDF parsing", "SPARQL", "Serialization", "Prototyping", "Education"],
        "speedNote": "Slow — pure Python, 10-100x slower than native alternatives. Fine for small datasets and prototyping",
        "scaleNote": "Struggles above ~1M triples due to memory and CPU. Not suitable for production-scale workloads"
    },
    "Apache Jena": {
        "focusAreas": ["SPARQL 1.1", "OWL reasoning", "RDF API", "TDB storage", "Fuseki server"],
        "speedNote": "Solid Java performance for I/O and queries. JVM warmup cost but good sustained throughput",
        "scaleNote": "Mature and proven at scale with TDB2. Handles hundreds of millions of triples in production"
    },
    "Eclipse RDF4J": {
        "focusAreas": ["SPARQL 1.1", "RDF storage", "SAIL API", "Reasoning", "LMDB backend"],
        "speedNote": "Comparable to Jena for most operations. LMDB store mode improves disk performance significantly",
        "scaleNote": "Production-grade. LMDB native store handles large datasets well. Used by GraphDB under the hood"
    },
    "QLever": {
        "focusAreas": ["SPARQL", "Full-text search", "Large-scale querying", "Wikidata-scale"],
        "speedNote": "Exceptionally fast SPARQL — often the fastest in benchmarks, especially on complex queries at scale",
        "scaleNote": "Designed for billions of triples. Handles full Wikidata (~18B triples) on a single machine"
    },
    "Virtuoso": {
        "focusAreas": ["SPARQL 1.1", "SQL + SPARQL hybrid", "Linked Data publishing", "Multi-model"],
        "speedNote": "Fast ingestion and good query performance. Column store architecture helps analytical queries",
        "scaleNote": "Battle-tested at scale — powers DBpedia and many LOD endpoints. Handles billions of triples"
    },
    "GraphDB": {
        "focusAreas": ["SPARQL 1.1", "OWL/RDFS reasoning", "Enterprise RDF", "Visual workbench", "Connectors"],
        "speedNote": "Moderate — reasoning overhead slows it vs. pure stores. Good for enterprise workloads with inference",
        "scaleNote": "Enterprise-grade. Handles billions of triples in cluster mode. Free edition limited to single-node"
    },
    "dotNetRDF": {
        "focusAreas": ["RDF API", "SPARQL", ".NET ecosystem", "Triple store connectors"],
        "speedNote": "Moderate for .NET — pure managed code. I/O is reasonable but SPARQL is slower than Java alternatives",
        "scaleNote": "In-memory store struggles above ~5M triples. Best as a client library connecting to external stores"
    },
    "Neo4j + n10s": {
        "focusAreas": ["Property graph", "RDF import/export", "Cypher queries", "Graph visualization"],
        "speedNote": "Fast native graph queries via Cypher. RDF import has overhead from property graph conversion",
        "scaleNote": "Neo4j itself scales very well. The RDF layer (n10s) adds import overhead but queries run at native speed"
    },
    "Kolibrie": {
        "focusAreas": ["RDF streaming", "SPARQL", "Rule-based reasoning", "Backward chaining"],
        "speedNote": "Very fast I/O and queries — Rust-based. Among the quickest for parsing and simple SPARQL",
        "scaleNote": "Early-stage project. Performance is promising but production-readiness is still developing"
    },
    "Stardog": {
        "focusAreas": ["Knowledge graph platform", "OWL reasoning", "Virtual graphs", "GraphQL", "Enterprise AI"],
        "speedNote": "Good query performance with reasoning enabled. Virtual graph feature avoids data duplication",
        "scaleNote": "Enterprise-proven, handles billions of triples in cluster deployments"
    },
    "Amazon Neptune": {
        "focusAreas": ["Managed cloud service", "SPARQL", "Gremlin", "openCypher", "Serverless option"],
        "speedNote": "Managed service — performance depends on instance size. Competitive but not the fastest per dollar",
        "scaleNote": "Scales via AWS infrastructure. Serverless option auto-scales. No upper limit on data size"
    },
    "AllegroGraph": {
        "focusAreas": ["SPARQL", "Prolog reasoning", "Federated queries", "Geospatial", "Temporal reasoning"],
        "speedNote": "Solid performance especially for complex reasoning queries. Geospatial and temporal indexing are fast",
        "scaleNote": "Handles billions of triples. Multi-master replication for horizontal scaling"
    },
    "Blazegraph": {
        "focusAreas": ["SPARQL 1.1", "Full-text search", "High availability", "Wikidata"],
        "speedNote": "Good performance — powers Wikidata Query Service. Optimized for read-heavy workloads",
        "scaleNote": "Handles billions of triples (proven by Wikidata). Unmaintained since 2020 — no future improvements"
    },
    "AnzoGraph": {
        "focusAreas": ["SPARQL analytics", "OLAP on graphs", "In-memory", "Data integration"],
        "speedNote": "Very fast for analytical/aggregation queries — designed for OLAP-style workloads on graph data",
        "scaleNote": "In-memory architecture. Free edition limited to 16GB. Scales via distributed memory in enterprise"
    },
    "Apache Jena Fuseki": {
        "focusAreas": ["SPARQL server", "HTTP endpoint", "TDB2 storage", "Graph Store Protocol"],
        "speedNote": "Same engine as Jena, with HTTP overhead. TDB2 backend gives good persistent storage performance",
        "scaleNote": "Production-proven with TDB2. Handles hundreds of millions of triples"
    },
    "RDFox": {
        "focusAreas": ["In-memory reasoning", "Datalog", "Incremental materialization", "High-performance"],
        "speedNote": "Extremely fast — among the fastest triple stores for both loading and querying with reasoning",
        "scaleNote": "In-memory, so bounded by RAM. Designed for high-performance reasoning, not raw storage scale"
    },
    "MarkLogic": {
        "focusAreas": ["Multi-model", "Document + RDF", "Full-text search", "Enterprise integration", "Security"],
        "speedNote": "Optimized for mixed document/RDF workloads. SPARQL performance is adequate but not its primary strength",
        "scaleNote": "Enterprise-grade clustering. Handles very large datasets across distributed nodes"
    },
    "Oxigraph Server": {
        "focusAreas": ["SPARQL server", "HTTP endpoint", "Lightweight", "Docker-ready"],
        "speedNote": "Same Rust engine as Oxigraph library, with minimal HTTP overhead. Good for small to medium deployments",
        "scaleNote": "Single-node only. Good for millions of triples, not designed for distributed scale"
    },
    "Ontop": {
        "focusAreas": ["Virtual knowledge graph", "SPARQL-to-SQL", "R2RML mappings", "No data duplication"],
        "speedNote": "Query speed depends on the underlying SQL database. Translation overhead is minimal for simple queries",
        "scaleNote": "Scales with the relational database underneath — no data duplication, no separate RDF storage needed"
    },
    "N3.js": {
        "focusAreas": ["RDF parsing", "Streaming parser", "RDF/JS spec", "Turtle/N3/N-Quads"],
        "speedNote": "Fast for JavaScript — streaming architecture keeps memory low. One of the fastest JS RDF parsers",
        "scaleNote": "Streaming design handles large files well. No SPARQL engine — pair with Comunica for queries"
    },
    "Comunica": {
        "focusAreas": ["SPARQL querying", "Federated queries", "Linked Data", "Modular architecture", "Browser-ready"],
        "speedNote": "Moderate — JS/TS overhead vs. native engines. Strength is querying heterogeneous sources, not raw speed",
        "scaleNote": "Designed for federated querying across many small sources, not for querying a single massive dataset"
    },
    "graphy.js": {
        "focusAreas": ["RDF parsing", "Streaming I/O", "Turtle/N-Triples/N-Quads/TriG"],
        "speedNote": "High-performance streaming parser for JavaScript. Claims fastest JS RDF throughput",
        "scaleNote": "Streaming architecture handles arbitrarily large files. Parser only — no query engine"
    },
    "jsonld.js": {
        "focusAreas": ["JSON-LD processing", "Expansion/compaction", "Framing", "RDF conversion"],
        "speedNote": "Adequate for JSON-LD operations. Not designed for high-throughput RDF processing",
        "scaleNote": "Processes individual JSON-LD documents — not a bulk data tool"
    },
    "rdf-ext": {
        "focusAreas": ["RDF/JS spec", "Developer experience", "Data pipelines", "Stream processing"],
        "speedNote": "Convenience-focused rather than performance-focused. Good DX, moderate throughput",
        "scaleNote": "Stream-based pipelines handle moderate data. Not for high-volume production"
    },
    "Redland (librdf)": {
        "focusAreas": ["RDF API", "C library", "Language bindings", "Multiple storage backends"],
        "speedNote": "Native C performance for parsing — historically fast. Showing its age vs. modern Rust alternatives",
        "scaleNote": "Multiple storage backends (BDB, MySQL, PostgreSQL) offer different scale characteristics"
    },
    "Raptor": {
        "focusAreas": ["RDF parsing", "Serialization", "RDF/XML", "Turtle", "N-Triples"],
        "speedNote": "Fast C parser — still one of the quickest for RDF/XML. Battle-tested in production since the 2000s",
        "scaleNote": "Streaming parser with constant memory usage. Handles arbitrarily large files"
    },
    "Sophia": {
        "focusAreas": ["RDF 1.2", "Rust toolkit", "Generic API", "Type-safe graph operations"],
        "speedNote": "Rust performance for parsing and graph operations. Less mature than Oxigraph but promising",
        "scaleNote": "In-memory by default. Good for moderate datasets where type safety and API design matter"
    },
    "Apache Commons RDF": {
        "focusAreas": ["RDF API abstraction", "Jena/RDF4J interop", "Type-safe interfaces"],
        "speedNote": "API layer only — performance depends entirely on the backing implementation (Jena, RDF4J, etc.)",
        "scaleNote": "No storage — delegates to backing implementation"
    },
    "Titanium JSON-LD": {
        "focusAreas": ["JSON-LD 1.1", "Java processing", "Expansion/compaction/framing"],
        "speedNote": "Fast Java JSON-LD processing. Focused and optimized for the JSON-LD spec",
        "scaleNote": "Document-level processing — not a bulk data tool"
    },
    "HDT (Header-Dictionary-Triples)": {
        "focusAreas": ["Compressed RDF", "Archival", "Triple-pattern queries", "Linked Data publishing"],
        "speedNote": "Extremely fast triple-pattern lookups on compressed data. 5-10x smaller than raw Turtle/NT",
        "scaleNote": "Handles billions of triples in compressed form. Read-only — no updates without rebuilding"
    },
    "EasyRdf": {
        "focusAreas": ["PHP RDF", "Linked Data consumption", "Simple API", "Web development"],
        "speedNote": "Adequate for PHP web applications. Not performance-oriented",
        "scaleNote": "Designed for consuming small amounts of Linked Data in web apps, not bulk processing"
    },
    "ARC2": {
        "focusAreas": ["PHP RDF", "SPARQL", "MySQL storage", "Legacy PHP projects"],
        "speedNote": "Slow by modern standards. PHP + MySQL overhead. Largely superseded by other tools",
        "scaleNote": "MySQL-backed, limited by PHP memory. Suitable for small datasets only"
    },
    "RDFSharp": {
        "focusAreas": ["RDF modeling", "SPARQL", "SHACL validation", "SKOS", ".NET ecosystem"],
        "speedNote": "Moderate .NET performance. Lighter weight than dotNetRDF with simpler API",
        "scaleNote": "In-memory graph — suitable for small to moderate datasets"
    },
    "Owlready2": {
        "focusAreas": ["OWL ontologies", "Reasoning", "Python-native", "SQLite backend", "HermiT/Pellet"],
        "speedNote": "Slow for RDF I/O but convenient for ontology work. Automatic reasoning via HermiT/Pellet",
        "scaleNote": "SQLite backend helps with larger ontologies but still limited by Python performance"
    },
    "pySHACL": {
        "focusAreas": ["SHACL validation", "Constraint checking", "SPARQL-based constraints", "Python"],
        "speedNote": "Validation speed depends on shape complexity and rdflib backend. Adequate for typical ontologies",
        "scaleNote": "Inherits rdflib's limitations — validation on large graphs can be slow"
    },
    "Morph-KGC": {
        "focusAreas": ["RDF mapping", "R2RML/RML", "YARRRML", "Heterogeneous data sources", "Knowledge graph construction"],
        "speedNote": "Good throughput for materialization. Optimized for batch mapping from tabular/JSON/XML sources",
        "scaleNote": "Handles large mapping jobs well. Designed for ETL pipelines, not runtime querying"
    },
    "Protege": {
        "focusAreas": ["Ontology editing", "OWL 2", "Reasoning", "Plugin ecosystem", "Visualization"],
        "speedNote": "Desktop app — responsive for typical ontologies. Can slow down on very large ontologies (>100K axioms)",
        "scaleNote": "Designed for ontology engineering, not large-scale data processing"
    },
    "WebProtege": {
        "focusAreas": ["Collaborative editing", "Change tracking", "Discussion threads", "Web-based"],
        "speedNote": "Web-based — responsive for normal-sized ontologies. Simpler than desktop Protege",
        "scaleNote": "Designed for collaborative ontology development, not large data"
    },
    "TopBraid Composer": {
        "focusAreas": ["Ontology IDE", "SHACL", "SPARQL editing", "Enterprise modeling"],
        "speedNote": "Full-featured IDE with good performance for modeling tasks",
        "scaleNote": "Desktop tool — suited for ontology engineering, not large-scale data processing"
    },
    "TopBraid EDG": {
        "focusAreas": ["Data governance", "Metadata management", "Vocabularies", "Business glossaries", "Enterprise"],
        "speedNote": "Enterprise platform — performance tuned for governance workflows, not raw RDF processing",
        "scaleNote": "Enterprise-grade with support for large organizational vocabularies and metadata"
    },
    "YASGUI": {
        "focusAreas": ["SPARQL editor", "Autocomplete", "Result visualization", "Embeddable"],
        "speedNote": "Browser-based editor — query speed depends entirely on the SPARQL endpoint, not YASGUI itself",
        "scaleNote": "Client-side tool — no data storage"
    },
    "WebVOWL": {
        "focusAreas": ["Ontology visualization", "VOWL notation", "Force-directed layout", "Interactive"],
        "speedNote": "Responsive for small-to-medium ontologies. Force-directed layout slows with many classes (>500)",
        "scaleNote": "Browser-based visualization — best for ontologies under a few hundred classes"
    },
    "OOPS!": {
        "focusAreas": ["Ontology quality", "Pitfall detection", "Best practices", "Modeling errors"],
        "speedNote": "Web service — analysis typically completes in seconds for normal ontologies",
        "scaleNote": "Designed for ontology auditing, not data-scale operations"
    },
    "PoolParty": {
        "focusAreas": ["Taxonomy management", "Text mining", "Knowledge modeling", "Enterprise semantic AI"],
        "speedNote": "Enterprise platform — optimized for taxonomy workflows, NLP enrichment, and content classification",
        "scaleNote": "Cloud-native enterprise platform. Handles large organizational taxonomies and content volumes"
    },
    "Ontopic Studio": {
        "focusAreas": ["R2RML mapping", "Virtual knowledge graphs", "Low-code", "Database integration"],
        "speedNote": "Visual mapping tool — performance depends on the underlying database and Ontop engine",
        "scaleNote": "Scales with the relational source — no separate RDF storage"
    },
    "SHACL Playground": {
        "focusAreas": ["SHACL validation", "Interactive testing", "Shape debugging"],
        "speedNote": "Browser-based — instant validation for small shapes and data graphs",
        "scaleNote": "Designed for testing, not production validation"
    },
    "TopBraid SHACL API": {
        "focusAreas": ["SHACL validation", "SHACL rules", "Java API", "Jena integration"],
        "speedNote": "Good Java performance for validation. Efficient for programmatic SHACL checking in pipelines",
        "scaleNote": "Scales with Jena — suitable for production validation workloads"
    },
    "Pellet / Openllet": {
        "focusAreas": ["OWL 2 DL reasoning", "Consistency checking", "Classification", "Explanation"],
        "speedNote": "Comprehensive reasoner but can be slow on large, complex ontologies. Explanation support is unique",
        "scaleNote": "In-memory reasoning — bounded by ontology complexity more than triple count"
    },
    "HermiT": {
        "focusAreas": ["OWL 2 reasoning", "Hypertableau calculus", "Classification", "Consistency checking"],
        "speedNote": "Often faster than Pellet for classification. Hypertableau algorithm handles complex ontologies well",
        "scaleNote": "In-memory — performs well on complex ontologies but bounded by available RAM"
    },
    "Zazuko Trifid": {
        "focusAreas": ["Linked Data publishing", "URI dereferencing", "SPARQL proxy", "Content negotiation"],
        "speedNote": "Lightweight Node.js server — fast for serving individual resources. Proxies to backend SPARQL store",
        "scaleNote": "Proxy architecture — scales with the backing triple store"
    },
    "Zazuko Ontology Editor": {
        "focusAreas": ["Collaborative editing", "GitHub-backed", "Version control", "Turtle output"],
        "speedNote": "Web-based editor — responsive for typical ontologies",
        "scaleNote": "Designed for ontology editing, not data processing"
    },
    "isSemantic RDF Visualizer": {
        "focusAreas": ["RDF visualization", "Validation", "Format conversion", "RDF-star support"],
        "speedNote": "Browser-based — handles small to medium RDF documents for visualization and validation",
        "scaleNote": "Client-side tool — suitable for individual documents, not large datasets"
    },
    "RMLMapper": {
        "focusAreas": ["RML mapping", "Data transformation", "CSV/JSON/XML to RDF", "R2RML compatible"],
        "speedNote": "Moderate throughput for mapping. Java-based with room for optimization on large sources",
        "scaleNote": "Handles moderate-sized mapping jobs. For very large sources, consider streaming alternatives"
    },
    "Matey": {
        "focusAreas": ["YARRRML editing", "Live preview", "RML export", "Beginner-friendly"],
        "speedNote": "Browser-based editor — instant preview for small mappings",
        "scaleNote": "Designed for writing and testing mappings, not production execution"
    },
    "JSON-LD Playground": {
        "focusAreas": ["JSON-LD testing", "Expansion/compaction", "Framing", "RDF conversion"],
        "speedNote": "Browser-based — instant processing for individual JSON-LD documents",
        "scaleNote": "Testing tool — not for bulk processing"
    },
    "Linked Data Fragments Server": {
        "focusAreas": ["Triple Pattern Fragments", "Low-cost publishing", "Client-side querying", "Decentralized"],
        "speedNote": "Server is lightweight by design — pushes query work to the client. Low server resource usage",
        "scaleNote": "Designed for scalable publishing — minimal server load even with many concurrent clients"
    },
    "Gruff": {
        "focusAreas": ["Graph visualization", "Query builder", "AllegroGraph integration", "Exploration"],
        "speedNote": "Desktop visualization tool — performance tied to AllegroGraph backend",
        "scaleNote": "Visualizes subsets of larger graphs — not designed to render millions of nodes"
    },
    "W3C RDF Validator": {
        "focusAreas": ["RDF/XML validation", "Triple listing", "Graph visualization"],
        "speedNote": "Simple web service — validates small RDF/XML documents quickly",
        "scaleNote": "Testing tool — paste or URL input only"
    },
    "Turtle Web Editor": {
        "focusAreas": ["Turtle editing", "Syntax highlighting", "Validation", "Prefix autocompletion"],
        "speedNote": "Browser-based editor — responsive for typical Turtle files",
        "scaleNote": "Designed for editing, not processing large files"
    },
    "RDF4J Workbench": {
        "focusAreas": ["Repository management", "SPARQL queries", "Data exploration", "RDF4J administration"],
        "speedNote": "Web UI — query performance depends on the RDF4J repository backend",
        "scaleNote": "Admin tool — scales with the underlying RDF4J server"
    },
}

# Apply enrichment
for v in vendors:
    name = v["name"]
    if name in enrichment:
        v["focusAreas"] = enrichment[name]["focusAreas"]
        v["speedNote"] = enrichment[name]["speedNote"]
        v["scaleNote"] = enrichment[name]["scaleNote"]
    else:
        print(f"WARNING: No enrichment for '{name}'")

with open("/sessions/zen-gracious-shannon/mnt/rdf vendor landscape/vendors.json", "w") as f:
    json.dump(vendors, f, indent=2)

enriched = sum(1 for v in vendors if v.get("focusAreas"))
print(f"\nEnriched: {enriched}/{len(vendors)} vendors")
