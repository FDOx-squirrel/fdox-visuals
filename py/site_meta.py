"""Captions, credits and status of every graphic shown on the site (S14).

One entry per file stem, in display order inside its category. The site
generator refuses to run when a graphic has no entry here or an entry has
no graphic: captions are never invented by the generator (figure-pages-site:
missing data gets a placeholder, not a guess).

Captions are in British English and say what the picture shows, not how it
was drawn.
"""

from __future__ import annotations

# Status shown on the card. "draft" graphics carry the notice below.
DRAFT_NOTICE = "Draft, as of 2026-11-05"
DRAFT_CATEGORIES = {"git-packager", "federation", "ogham-graph"}

CREDIT_BASE = "FDOx-squirrel, fdox-visuals (Florian Thiery, LEIZA). Code: MIT licence."

CAPTIONS: dict[str, list[tuple[str, str, str]]] = {
    # (file stem, caption, source line or "")
    "pattern": [
        ("fdox-four-step-pattern",
         "The four-step FDOx pattern: FDO encapsulation, semantic metadata and paradata modelling, linking to community hubs, federated knowledge graph integration.", ""),
        ("fdox-step-1-fdo-encapsulation", "Badge for step 1: FDO encapsulation (persistent identifier, structured metadata and provenance).", ""),
        ("fdox-step-2-semantic-paradata-modelling", "Badge for step 2: semantic metadata and paradata modelling (acquisition, spatial anchoring, CIDOC CRM alignment).", ""),
        ("fdox-step-3-linking-community-hubs", "Badge for step 3: linking to community hubs (Wikidata, OpenStreetMap).", ""),
        ("fdox-step-4-federated-kg-integration", "Badge for step 4: federated knowledge graph integration across research infrastructures.", ""),
        ("fdox-purpose-pattern",
         "What FDOx does: four outcomes of the pattern, FAIR and citable, semantically queryable, interoperable, integrable.", ""),
        ("fdox-purpose-1-fair-citable", "Badge for outcome 1: FAIR and citable.", ""),
        ("fdox-purpose-2-semantically-queryable", "Badge for outcome 2: semantically queryable.", ""),
        ("fdox-purpose-3-interoperable", "Badge for outcome 3: interoperable.", ""),
        ("fdox-purpose-4-integrable", "Badge for outcome 4: integrable.", ""),
    ],
    "schemas": [
        ("fdox-fair-digital-object-meta-graphic",
         "The FAIR Digital Object as data, metadata and persistent identifier, in the FDOx palette.", ""),
        ("fdox-fdo-sphere", "The FDO sphere on its own, for use in slides and posters.", ""),
        ("fdox-fdo-squirrel-architecture",
         "How fdo-squirrel turns an FDO ZIP package into RDF, including validation, the overview image and bundle finalisation.",
         "Source: fdo-squirrel, main.py."),
        ("fdox-md-cff-schema", "Class diagram of the MD.cff metadata schema.",
         "Source: fdo-squirrel-spec, data/raw/MD.cff-schema.yaml."),
        ("fdox-citation-cff-schema",
         "The CITATION.cff fields fdo-squirrel reads: those its crosswalk forwards to RDF and those it maps but drops.",
         "Source: fdo-squirrel crosswalk."),
    ],
    "talk-process": [
        ("fdox-talk-step1-fdo-encapsulation", "Talk slide, step 1: FDO encapsulation. A 3D model (Freshford, St Lachtain’s Well, via Sketchfab) is converted and packaged with fdo-3d-packager.", ""),
        ("fdox-talk-step2-semantic-metadata", "Talk slide, step 2: semantic metadata and paradata modelling, with the real MD.cff and Turtle values of CIIC 81 and its CIDOC CRM anchor.", ""),
        ("fdox-talk-step3-linking-hubs", "Talk slide, step 3: linking to community hubs. CIIC 81 points to the Wikidata items Q2016147 (Inscribed Ogham stone) and Q22731 (Stone).", ""),
        ("fdox-talk-step4-federated-kg", "Talk slide, step 4: federated knowledge graph integration. The FDOx registry (release 2026-09-03, 8 sources, 7,793 triples) feeds the NFDI4Objects knowledge graph.", ""),
    ],
    "talk-purpose": [
        ("fdox-talk-purpose1-fair-citable", "Talk slide, outcome 1: FAIR and citable, shown with the real CITATION.cff of CIIC 81.", ""),
        ("fdox-talk-purpose2-semantically-queryable", "Talk slide, outcome 2: semantically queryable, shown with a real query on the registry’s SPARQL page.", ""),
        ("fdox-talk-purpose3-interoperable", "Talk slide, outcome 3: interoperable. Six real registry objects share three real hubs.", ""),
        ("fdox-talk-purpose4-integrable", "Talk slide, outcome 4: integrable. Bundles in Turtle and JSON enter the registry through a crosswalk.", ""),
    ],
    "talk-closing": [
        ("fdox-talk-closing-a-sphere", "Closing slide, variant A: the eight badges as a ring around the FDO sphere.", ""),
        ("fdox-talk-closing-b-hubs", "Closing slide, variant B: the same ring, with dotted links to the community hubs NFDI4Objects, Wikidata and OpenStreetMap.", ""),
    ],
    "git-packager": [
        ("fdox-git-packager-four-steps",
         "Concept for fdo-git-packager: pin, inspect, package, build and publish. Dashed outlines mark what is planned.",
         "Example: SPARQLing Unicorn QGIS plugin, tag v0.17.4 (ba8af4c). fdo-git-packager is a skeleton; no step is implemented yet."),
        ("fdox-git-packager-step-1-pin", "Badge for git-packager step 1: pin the repository to a commit.", ""),
        ("fdox-git-packager-step-2-inspect", "Badge for git-packager step 2: inspect the working tree.", ""),
        ("fdox-git-packager-step-3-package", "Badge for git-packager step 3: package metadata and files.", ""),
        ("fdox-git-packager-step-4-build", "Badge for git-packager step 4: build and publish.", ""),
        ("fdox-talk-git-packager-step1-fetch", "Talk slide, git-packager step 1: pin the commit. A tag is resolved to one commit, so the package can be rebuilt.",
         "Example: SPARQLing Unicorn QGIS plugin, tag v0.17.4 (ba8af4c)."),
        ("fdox-talk-git-packager-step2-inspect", "Talk slide, git-packager step 2: read what the repository already says about itself, such as its CITATION.cff.",
         "Example: SPARQLing Unicorn QGIS plugin, tag v0.17.4 (ba8af4c)."),
        ("fdox-talk-git-packager-step3-package", "Talk slide, git-packager step 3: one ZIP with the working tree flat at its root; the repository’s own CITATION.cff is kept as it is.",
         "Example: SPARQLing Unicorn QGIS plugin, tag v0.17.4 (ba8af4c)."),
        ("fdox-talk-git-packager-step4-build", "Talk slide, git-packager step 4: let fdo-squirrel build the FDO, then publish it.",
         "Example: SPARQLing Unicorn QGIS plugin, tag v0.17.4 (ba8af4c)."),
        ("fdox-talk-git-packager-actions", "Swimlane: what happens on GitHub, in GitHub Actions (planned), at Zenodo and in the FDOx registry and the N4O KG.",
         "Example: SPARQLing Unicorn QGIS plugin, tag v0.17.4 (ba8af4c)."),
    ],
    "federation": [
        ("fdox-talk-federation-path", "From packaged FDOs to the federated KG: 3D models and software take the same road.",
         "Data: FDOx registry 253aee9 (release 2026-09-03); N4O collection 882a5f7 (2026-09-04)."),
        ("fdox-talk-federation-catalogue", "One catalogue, two kinds of FDO: the registry’s overview query lists 3D data and software side by side.",
         "Data: FDOx registry 253aee9 (release 2026-09-03); N4O collection 882a5f7 (2026-09-04)."),
        ("fdox-talk-federation-shared-concepts", "What the graph links, and what it does not: Wikidata concepts that more than one FDO points at.",
         "Data: FDOx registry 253aee9 (release 2026-09-03); N4O collection 882a5f7 (2026-09-04)."),
    ],
    "ogham-graph": [
        ("fdox-talk-ogham-graph-cluster", "Ogham in the graph: stones, 3D models and software around the Wikidata item Q2016147, drawn from real registry triples.",
         "Data: FDOx registry 253aee9 (release 2026-09-03). Labels are those of the bundles."),
        ("fdox-talk-ogham-graph-object", "One Ogham stone, its 3D FDO and the software: one hop around each FDO. The link between them is the open point (not modelled yet).",
         "Data: FDOx registry 253aee9 (release 2026-09-03). Labels are those of the bundles."),
        ("fdox-talk-ogham-graph-registry", "The whole registry as one graph: eight FDOs, the concepts and people that connect them, and the ones that do not.",
         "Data: FDOx registry 253aee9 (release 2026-09-03). Labels are those of the bundles."),
    ],
}

# Short label prefix per category, numbered by position: PA.1, SC.2, ...
LABELS = {
    "pattern": "PA", "schemas": "SC", "talk-process": "TP", "talk-purpose": "TU",
    "talk-closing": "TC", "git-packager": "GP", "federation": "FE", "ogham-graph": "OG",
}

# Short names for the navigation row.
SHORT = {
    "pattern": "Pattern", "schemas": "Schemas", "talk-process": "Talk: process", "talk-purpose": "Talk: purpose",
    "talk-closing": "Talk: closing", "git-packager": "Git packager", "federation": "Federation", "ogham-graph": "Ogham graphs",
}
