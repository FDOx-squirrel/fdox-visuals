"""Captions, credits and status of every graphic shown on the site (S14).

One entry per file stem, in display order inside its category. The site
generator refuses to run when a graphic has no entry here or an entry has
no graphic: captions are never invented by the generator (figure-pages-site:
missing data gets a placeholder, not a guess).

Captions are in British English and say what the picture shows, not how it
was drawn.
"""

from __future__ import annotations

# Status shown on the card. Only graphics of planned work carry a badge; all
# others are built from released tools and registry data (their source line
# names the release or commit).
CONCEPT_NOTICE = "Concept: planned, not implemented yet"
CONCEPT_STEMS = {"fdox-story-two-roads-unicorn"}   # the git-packager set is added by category below
CONCEPT_CATEGORIES = {"git-packager", "git-packager-pictograms"}

CREDIT_BASE = "FDOx-squirrel, fdox-visuals (Florian Thiery, Research Squirrel Engineers Network / LEIZA). Code: MIT licence."

CAPTIONS: dict[str, list[tuple[str, str, str]]] = {
    # (file stem, caption, source line or "")
    "pattern": [
        ("fdox-four-step-pattern",
         "The four-step FDOx pattern: FDO encapsulation, semantic metadata and paradata modelling, linking to community hubs, federated knowledge graph integration.",
         ""),
        ("fdox-purpose-pattern",
         "What FDOx does: four outcomes of the pattern, FAIR and citable, semantically queryable, interoperable, integrable.",
         ""),
    ],
    "pictograms": [
        ("fdox-step-1-fdo-encapsulation",
         "Pictogram for step 1: FDO encapsulation (persistent identifier, structured metadata and provenance).",
         ""),
        ("fdox-step-2-semantic-paradata-modelling",
         "Pictogram for step 2: semantic metadata and paradata modelling (acquisition, spatial anchoring, CIDOC CRM alignment).",
         ""),
        ("fdox-step-3-linking-community-hubs",
         "Pictogram for step 3: linking to community hubs (Wikidata, OpenStreetMap).",
         ""),
        ("fdox-step-4-federated-kg-integration",
         "Pictogram for step 4: federated knowledge graph integration across research infrastructures.",
         ""),
        ("fdox-purpose-1-fair-citable",
         "Pictogram for outcome 1: FAIR and citable.",
         ""),
        ("fdox-purpose-2-semantically-queryable",
         "Pictogram for outcome 2: semantically queryable.",
         ""),
        ("fdox-purpose-3-interoperable",
         "Pictogram for outcome 3: interoperable.",
         ""),
        ("fdox-purpose-4-integrable",
         "Pictogram for outcome 4: integrable.",
         ""),
    ],
    "schemas": [
        ("fdox-fair-digital-object-meta-graphic",
         "The FAIR Digital Object as data, metadata and persistent identifier, in the FDOx palette.",
         ""),
        ("fdox-fdo-sphere",
         "The FDO sphere on its own, for use in presentations, posters and papers.",
         ""),
        ("fdox-fdo-squirrel-architecture",
         "How fdo-squirrel turns an FDO ZIP package into RDF, an RO-Crate and a Signposting landing page, including validation, the overview image and bundle finalisation.",
         "Source: fdo-squirrel v1.2.0, main.py."),
        ("fdox-bundle-three-views",
         "One finished bundle, three views of the same FDO: the lossless RDF description, the RO-Crate 1.2 view (the Webby FDO) and the FAIR Signposting landing page.",
         "Source: fdo-squirrel v1.2.0, docs/ro-crate-mapping.md and docs/signposting.md. RO-Crate logo: RO-Crate Community, CC BY 4.0. RDF logo: Bill Schwappacher / W3C, CC BY 4.0."),
        ("fdox-md-cff-schema",
         "Class diagram of the MD.cff metadata schema.",
         "Source: fdo-squirrel-spec, data/raw/MD.cff-schema.yaml."),
        ("fdox-citation-cff-schema",
         "The CITATION.cff fields fdo-squirrel reads: those its crosswalk forwards to RDF and those it maps but drops.",
         "Source: fdo-squirrel crosswalk."),
    ],
    "sphere": [
        ("fdox-sphere-badges",
         "The FDO sphere, variant A: the eight badges as a ring around the FDO sphere.",
         ""),
        ("fdox-sphere-hubs",
         "The FDO sphere, variant B: the same ring, with dotted links to the community hubs NFDI4Objects, Wikidata and OpenStreetMap.",
         ""),
    ],
    "steps": [
        ("fdox-steps-1-fdo-encapsulation",
         "Step 1: FDO encapsulation. A 3D model (Freshford, St Lachtain’s Well, via Sketchfab) is converted and packaged with fdo-3d-packager.",
         ""),
        ("fdox-steps-1-fdo-encapsulation-ciic81",
         "Step 1 with CIIC 81: the Sketchfab model of an Ogham stone is converted and packaged with fdo-3d-packager (50 files in the registry).",
         "Model: b-unicycling, via Sketchfab (screenshot of the model page). Registry 253aee9."),
        ("fdox-steps-2-semantic-metadata",
         "Step 2: semantic metadata and paradata modelling, with the real MD.cff and Turtle values of CIIC 81 and its CIDOC CRM anchor.",
         ""),
        ("fdox-steps-3-linking-hubs",
         "Step 3: linking to community hubs. CIIC 81 points to the Wikidata items Q2016147 (Inscribed Ogham stone) and Q22731 (Stone).",
         ""),
        ("fdox-steps-4-federated-kg",
         "Step 4: federated knowledge graph integration. The FDOx registry (release 2026-09-03, 8 sources, 7,793 triples) feeds the NFDI4Objects knowledge graph.",
         ""),
    ],
    "outcomes": [
        ("fdox-outcomes-1-fair-citable",
         "Outcome 1: FAIR and citable, shown with the real CITATION.cff of CIIC 81.",
         ""),
        ("fdox-outcomes-2-semantically-queryable",
         "Outcome 2: semantically queryable, shown with a real query on the registry’s SPARQL page.",
         ""),
        ("fdox-outcomes-3-interoperable",
         "Outcome 3: interoperable. Six real registry objects share three real hubs.",
         ""),
        ("fdox-outcomes-4-integrable",
         "Outcome 4: integrable. Bundles in Turtle and JSON enter the registry through a crosswalk.",
         ""),
    ],
    "3d-packager-pictograms": [
        ("fdox-3d-packager-step-1-fetch",
         "Pictogram for fdo-3d-packager step 1: fetch the model (Sketchfab API or local files).",
         "Source: step names of the fdo-3d-packager CLI."),
        ("fdox-3d-packager-step-2-convert",
         "Pictogram for fdo-3d-packager step 2: convert the model (Blender to OBJ and textures).",
         "Source: step names of the fdo-3d-packager CLI."),
        ("fdox-3d-packager-step-3-nexus",
         "Pictogram for fdo-3d-packager step 3: build the multiresolution model (Nexus).",
         "Source: step names of the fdo-3d-packager CLI."),
        ("fdox-3d-packager-step-4-mdcff",
         "Pictogram for fdo-3d-packager step 4: write the metadata (MD.cff and CITATION.cff).",
         "Source: step names of the fdo-3d-packager CLI."),
        ("fdox-3d-packager-step-5-bundle",
         "Pictogram for fdo-3d-packager step 5: bundle the 3DHOP viewer and the files into one ZIP.",
         "Source: step names of the fdo-3d-packager CLI."),
        ("fdox-3d-packager-step-6-build-fdo",
         "Pictogram for fdo-3d-packager step 6: build the FDO with fdo-squirrel (build_fdo).",
         "Source: step names of the fdo-3d-packager CLI."),
    ],
    "git-packager": [
        ("fdox-git-packager-four-steps",
         "Concept for fdo-git-packager: pin, inspect, package, build and publish. Dashed outlines mark what is planned.",
         "Example: SPARQLing Unicorn QGIS plugin, tag v0.17.4 (ba8af4c). fdo-git-packager is a skeleton; no step is implemented yet."),
        ("fdox-git-packager-1-fetch",
         "git-packager step 1: pin the commit. A tag is resolved to one commit, so the package can be rebuilt.",
         "Example: SPARQLing Unicorn QGIS plugin, tag v0.17.4 (ba8af4c)."),
        ("fdox-git-packager-2-inspect",
         "git-packager step 2: read what the repository already says about itself, such as its CITATION.cff.",
         "Example: SPARQLing Unicorn QGIS plugin, tag v0.17.4 (ba8af4c)."),
        ("fdox-git-packager-3-package",
         "git-packager step 3: one ZIP with the working tree flat at its root; the repository’s own CITATION.cff is kept as it is.",
         "Example: SPARQLing Unicorn QGIS plugin, tag v0.17.4 (ba8af4c)."),
        ("fdox-git-packager-4-build",
         "git-packager step 4: let fdo-squirrel build the FDO, then publish it.",
         "Example: SPARQLing Unicorn QGIS plugin, tag v0.17.4 (ba8af4c)."),
        ("fdox-git-packager-actions",
         "Swimlane: what happens on GitHub, in GitHub Actions (planned), at Zenodo and in the FDOx registry and the N4O KG.",
         "Example: SPARQLing Unicorn QGIS plugin, tag v0.17.4 (ba8af4c)."),
    ],
    "git-packager-pictograms": [
        ("fdox-git-packager-step-1-pin",
         "Pictogram for git-packager step 1: pin the repository to a commit.",
         ""),
        ("fdox-git-packager-step-2-inspect",
         "Pictogram for git-packager step 2: inspect the working tree.",
         ""),
        ("fdox-git-packager-step-3-package",
         "Pictogram for git-packager step 3: package metadata and files.",
         ""),
        ("fdox-git-packager-step-4-build",
         "Pictogram for git-packager step 4: build and publish.",
         ""),
    ],
    "story": [
        ("fdox-story-fkge-map",
         "From the federated KG ecosystem to FDOx: the FDO-driven and the LOD-driven way into the graph, with the four FDOx steps (the FDOx four-step pattern) as the bridge for 3D models and software.",
         "Simplified from the FKGE diagram of Thiery & Noback (CC BY 4.0)."),
        ("fdox-story-two-roads-unicorn",
         "Two roads, one bundle: CIIC 81 (3D) and the SPARQLing Unicorn plugin (software, planned) meet in the same fdo-squirrel engine. What differs: the type tag (3DDataFDO or SoftwareFDO) and the roles of the files (model and textures; for software the code, scripts and documentation). What does not: the MD.cff schema, fdo-squirrel, the DOI, the registry record and the way both are queried.",
         "CIIC 81: registry 253aee9. SPARQLing Unicorn: tag v0.17.4 (ba8af4c), read 2026-11-05. fdo-git-packager is a skeleton (S1); the software FDO is not built yet."),
        ("fdox-story-two-roads-extractor",
         "Two roads, one bundle: CIIC 81 (3D) and the finished Ogham 3D EpiDoc Extractor (software) end up as the same kind of FDO. What differs: the type tag (3DDataFDO or SoftwareFDO) and the roles of the files (model and textures; for the extractor software 222, script 30, documentation 2). What does not: the MD.cff schema, fdo-squirrel, the DOI, the registry record and the way both are queried.",
         "Registry 253aee9 (release 2026-09-03), registry-index.json. fdo-git-packager is a skeleton (S1); how the extractor was packaged is not recorded here."),
        ("fdox-story-squilly-graph",
         "From Squilly’s nut-and-string graph to a real one: eight FDOs, the concepts and people that connect them. Freshford shares nothing with the others. Dashed: free text, or an agent the registry minted.",
         "Left: drawn sketch, not data. Right: registry 253aee9 (release 2026-09-03), dist/fdo-registry.ttl, 7,793 triples; graph facts as in the Ogham graphs."),
    ],
    "federation": [
        ("fdox-federation-path",
         "From packaged FDOs to the federated KG: 3D models and software take the same road. Six 3D and two software FDOs are in the registry; jupyter-nb-lod is planned, via fdo-git-packager. Both kinds of FDO pass the same gates: the registry reads a 3DDataFDO and a SoftwareFDO with one pipeline, and the KG only ever sees the registry’s CRM-anchored bundle.",
         "Read 2026-11-05: fdo-squirrel-registry 253aee9 (release 2026-09-03); fdox-squirrel-n4o-collection 882a5f7 (README status 2026-09-04)."),
        ("fdox-federation-catalogue",
         "One catalogue, two kinds of FDO: the registry’s overview query lists 3D data and software side by side. Every row is a dcat:Dataset with a licence and distributions, whatever it describes, so a model of a stone and the code that extracts its inscription are found, filtered and counted the same way.",
         "Registry query “Every FDO with its type, licence and file count” (queries.yaml); values from registry-index.json, release 2026-09-03. A ninth pinned record has no fdo-metadata.ttl."),
        ("fdox-federation-shared-concepts",
         "What the graph links, and what it does not: Wikidata concepts that more than one FDO points at. 3D models and software share concepts, so a query from one finds the other: the extractor, the analysis and two stones. CHUIS/1 says “Ogham Stone” as text only and is missing from Q2016147; the Beuys stele and the Freshford well share no concept with another FDO. Also shared: both software FDOs carry OSM relation 62273 as dct:spatial.",
         "Registry query “Wikidata concepts that more than one FDO points at” (queries.yaml, shared-concepts), run on dist/fdo-registry.ttl (7,793 triples), 2026-11-05."),
    ],
    "ogham-graph": [
        ("fdox-ogham-graph-cluster",
         "Ogham in the graph: stones, 3D models and software around the Wikidata item Q2016147, drawn from real registry triples. All five FDOs share dct:publisher wd:Q73901970 and one fdo:context, “Ogham Stones in the Wild and in Museums in Ireland”. Dashed: free text, or a second node for the same person; CHUIS/1 is missing from Q2016147.",
         "Data: FDOx registry 253aee9 (release 2026-09-03), dist/fdo-registry.ttl. Labels are those of the bundles."),
        ("fdox-ogham-graph-object",
         "One Ogham stone, its 3D FDO and the software: one hop around each FDO. The link between them is the open point (not modelled yet): both FDOs are typed with the same concept and share fdo:context and publisher, but that software works on that kind of object is not an edge. The dashed arc is a proposal (e.g. prov:used), not part of the data.",
         "Data: FDOx registry 253aee9 (release 2026-09-03), dist/fdo-registry.ttl and registry-index.json. Labels are those of the bundles."),
        ("fdox-ogham-graph-registry",
         "The whole registry as one graph: eight FDOs, the concepts and people that connect them, and the ones that do not. The Freshford well shares no concept, place or person with another FDO (publisher only). Thiery appears as two nodes, as ORCID and as a registry-minted agent; the registry never merges on a name. wd:Q22731 (“Stone”, 6 FDOs) is left out for legibility; all eight share dct:publisher wd:Q73901970.",
         "Data: FDOx registry 253aee9 (release 2026-09-03), dist/fdo-registry.ttl (7,793 triples). Labels are those of the bundles."),
    ],
}

# Short label prefix per category, numbered by position: PA.1, SC.2, ...
LABELS = {
    "pattern": "PA", "pictograms": "PI", "schemas": "SC", "sphere": "SH", "steps": "ST", "outcomes": "OU", "3d-packager-pictograms": "DP",
    "git-packager": "GP", "git-packager-pictograms": "GI", "story": "SY", "federation": "FE", "ogham-graph": "OG",
}

# Short names for the navigation rows.
SHORT = {
    "pattern": "Pattern", "pictograms": "Pictograms", "schemas": "Schemas", "sphere": "Sphere and hubs",
    "steps": "Steps", "outcomes": "Outcomes", "3d-packager-pictograms": "Pictograms", "git-packager": "Git packager", "git-packager-pictograms": "Pictograms",
    "story": "Story", "federation": "Federation", "ogham-graph": "Ogham graphs",
}
