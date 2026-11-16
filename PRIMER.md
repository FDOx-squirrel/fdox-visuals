# PRIMER — fdox-visuals

Arbeitsplan für `fdox-visuals`: die Grafik-Werkstatt der FDOx-Squirrel-Familie.
Ein `main.py`, das reine Python-Skripte fährt und PNG/JPG/SVG für Vorträge,
Paper-Abbildungen und READMEs erzeugt — deterministisch, ohne externe
CLI-Tools (kein `rsvg-convert`, kein ImageMagick), damit `pip install -r
requirements.txt` auf Flos Windows-Maschine reicht.

**Ort.** `https://github.com/FDOx-squirrel/fdox-visuals/blob/main/PRIMER.md`

**So wird es benutzt.** Wird vollständig zu Beginn jedes Chats hochgeladen.
Danach genügt "wir machen S4". Teil A gilt immer, Teil B ist die Übersicht,
Teil C beschreibt den einzelnen Schritt.

---

# Teil A — Immer gültig

## A1. Ausgangslage

Entstanden aus zwei Chat-Auslieferungen (siehe unten) für den 10-Minuten-
Vortrag "From Smartphone 3D to Federated Knowledge Graphs" auf der FAIR 3D
Heritage Conference (Mainz, 14.–16.09.2026): das Vier-Schritte-Muster-Schema
und die FAIR-Digital-Object-Meta-Grafik. Beide waren zunächst lose Dateien in
einem ZIP, keine eigene Codebasis. Dieses Repo macht sie reproduzierbar und
ist der Ort, an dem künftige Vortrags-/Paper-Grafiken der Familie entstehen.

**Befunde (geprüft 2026-09-08):**

1. **Rendering ohne Systemabhängigkeit ist möglich.** `cairosvg` (reines
   Python-Paket) rendert SVG → PNG identisch zu `rsvg-convert`, einschließlich
   `linearGradient` mit `gradientUnits="userSpaceOnUse"` und lokal
   eingebetteten `@font-face`-Schriften. Getestet an allen drei bereits
   bestehenden Grafiken, Pixel-für-Pixel-Vergleich per Auge, keine
   Abweichung gefunden.
2. **`linearGradient` mit `objectBoundingBox` (Default) auf einem
   waagerechten `<line>` rendert in `rsvg-convert` gar nicht** — die
   Bounding-Box einer waagerechten Linie hat Höhe 0, das degeneriert die
   Koordinaten. Fix: immer `gradientUnits="userSpaceOnUse"` mit expliziten
   Pixel-Koordinaten setzen, nicht die 0–1-Kurzschreibweise. Gilt vermutlich
   für jeden SVG-Renderer, nicht nur `rsvg-convert` — also so übernommen,
   nicht nur als Workaround für ein Tool.
3. **Fira Sans ist nicht über `apt` verfügbar** (nur `fonts-firacode`, die
   Monospace-Variante). Bezogen aus dem offiziellen
   `github.com/mozilla/Fira`-Repo (SIL Open Font License 1.1, frei
   vendorbar). Nur `FiraSans-Regular.ttf` und `FiraSans-Bold.ttf` werden
   gebraucht (keine Kursive, keine weiteren Schnitte) — hält das Repo klein.
4. **Die Blaufrage ist entschieden:** `#004473` ist die tatsächliche Farbe
   aus dem ursprünglichen "FAIR Digital Object"-Referenzbild (per Pixel-
   Sampling verifiziert, `PIL.Image.getpixel`), nicht die zunächst
   probeweise verwendete `#2451D6`. Das gilt jetzt als **die** FDOx-Blau-
   Referenz für die ganze Familie: Step 1 im Vier-Schritte-Schema und der
   Akzent der Meta-Grafik sind identisch `#004473`, damit beide Grafiken
   sichtbar zusammengehören.
5. **`cairosvg` ist trotz `pip install` keine reine Python-Lösung —
   Falschannahme aus S0/S1, korrigiert 2026-09-08.** `cairosvg` bindet an
   eine System-`libcairo`; im Sandkasten war die zufällig vorhanden (kam
   transitiv mit `librsvg2-bin` über `apt`, das für einen früheren,
   unabhängigen Render-Versuch installiert worden war), auf Flos
   Windows-Rechner fehlt sie komplett. Echter Fehlertext beim ersten Lauf
   nach dem Commit: `no library called "cairo-2" was found` /
   `cannot load library 'libcairo-2.dll'`. Ersetzt durch **`resvg-py`**
   (Rust, `abi3`-Wheel, Renderer statisch mit einkompiliert — auch für
   `win_amd64` auf PyPI vorhanden). Geprüft: identischer Bildinhalt zu
   `cairosvg` bei allen drei bestehenden Grafiken (Sichtprüfung,
   Gradient/Pattern/Font alle korrekt), Icon-Transparenz weiterhin
   `RGBA`-Alpha `0` in der Ecke. `resvg-py` lädt die Schrift über den
   expliziten `font_files=`-Parameter (nicht über das `@font-face`-CSS im
   SVG, das bleibt trotzdem drin — hilft beim Öffnen der `.svg`-Dateien in
   Inkscape/Browser, auch wenn der Python-Renderpfad nicht mehr darauf
   angewiesen ist).
6. **Google Slides komprimiert eingefügte Bilder oberhalb von 25
   Megapixeln zwangsweise** (offizielle Grenze laut Googles eigener
   Slides-API-Dokumentation, `developers.google.com/workspace/slides/api`)
   und degradiert nach Erfahrungsberichten (Google-Docs-Editors-Community)
   auch deutlich darunter schon sichtbar — ein 16-MP-Testbild wurde dort
   beim Einfügen auf ~3,2 MP heruntergerechnet. Flos ursprünglicher Banner
   war 11520×3252 ≈ 37,5 MP, also klar über der harten Grenze — das war die
   Ursache der gemeldeten Unschärfe, nicht ein Fehler in der Datei selbst.
7. **Schritt 4s Titeltext reicht über den Icon-Kreis hinaus.** Am
   Original-Banner (vor dem Auflösungs-Rückbau) per `PIL`-Bounding-Box
   nachgemessen: der rechte Rand des sichtbaren Inhalts liegt näher am
   Canvas-Rand, als es allein der Kreis von Step 4 erwarten ließe —
   "Federated Knowledge"/"research infrastructures" ist breiter als der
   Badge-Kreis. Deshalb schneidet `trim_transparent_border()` (S1) anhand
   der tatsächlich gerenderten Pixel zu, nicht anhand einer geschätzten
   Design-Koordinate.

7. **Schritt 4s Titeltext reicht über den Icon-Kreis hinaus.** Am
   Original-Banner (vor dem Auflösungs-Rückbau) per `PIL`-Bounding-Box
   nachgemessen: der rechte Rand des sichtbaren Inhalts liegt näher am
   Canvas-Rand, als es allein der Kreis von Step 4 erwarten ließe —
   "Federated Knowledge"/"research infrastructures" ist breiter als der
   Badge-Kreis. Deshalb schneidet `trim_transparent_border()` (S1) anhand
   der tatsächlich gerenderten Pixel zu, nicht anhand einer geschätzten
   Design-Koordinate.
8. **`fdo-squirrel/architecture.mermaid` (+ `architecture.png`) existiert,
   ist aber veraltet — geprüft 2026-09-08 gegen den echten `main.py`.**
   Deckt drei Pipeline-Stufen nicht ab, die im aktuellen Code laufen:
   Schema-Validierung (`validate_against_schema`, direkt nach dem Laden),
   die Mermaid→JPG-Übersichtsgrafik (`FDOMermaidGenerator` +
   `render_mermaid_to_jpg`, schreibt `fdo_overview.mermaid`/`.jpg`), und
   die Bundle-Finalisierung (`build_finished_bundle`, schreibt
   `<slug>-fdo-bundle.zip`). Das Diagramm zeigt nur Ingest → Crosswalk →
   Provenance → TTL/Report, wie es offenbar vor Einführung dieser drei
   Stufen aussah. Kein anderes Repo der Familie hat eine aktuellere
   Fassung (`fdo-3d-packager`, `fdo-architecture`,
   `fdo-squirrel-registry`, `fdo-git-packager` durchsucht — nichts
   gefunden).
9. **Kein Generator-Skript für ein MD.cff-Klassendiagramm irgendwo in der
   Familie gefunden** (gleiche Suche wie Befund 8). Das von Flo
   hochgeladene Referenzbild ist zudem **inhaltlich veraltet** gegen das
   echte, aktuelle `fdo-squirrel-spec/data/raw/MD.cff-schema.yaml`
   (geprüft 2026-09-08): `md_cff_version` fehlt als Attribut komplett
   (ist aber `required`); `version` und `date_created` sind im Bild als
   `required` markiert, im echten Schema aber optional; `publishers` hat
   `minItems: 1`, müsste also 1..\* statt 0..\* sein; `Technique` ist im
   Bild `method`/`hardware`/`images_count`/`software`/`steps` (flach),
   im echten Schema aber `acquisition{method,hardware,images_count}` +
   `processing` + `programming_languages[]` + `repository{type,url,
   development_status}` — eine andere Struktur, nicht nur andere Felder.
   Drei Top-Level-Felder fehlen im Bild ganz: `contributors`,
   `related_resources`, `distributions`.
10. **"Kacheln" am unteren Rand von `fdox-fdo-squirrel-architecture.png`
    (gemeldet von Flo, 2026-09-08) — Rechenfehler in S4, nicht im
    Rendering.** Die Panel-Hintergrundboxen wurden mit einer `panel_h`
    berechnet, die den zusätzlichen `yoff`-Versatz der eigentlichen
    Prozess-Boxen nicht mit einbezog — die letzte Box ("Bundle
    finalisation") reichte dadurch rechnerisch 16 Design-Einheiten (≈ 29px
    bei `1.8`-facher Renderauflösung) über den unteren Panel-Rand hinaus,
    sichtbar als abgeschnittene Ecke/zweite Kontur unter dem eigentlichen
    Panel. Fix: `row_y()` liefert jetzt direkt absolute Canvas-Koordinaten
    (inkl. `PANEL_TOP`/Titel-Abstand), `panel_h` wird aus derselben
    Funktion abgeleitet statt aus einer zweiten, leicht abweichenden
    Rechnung — beide können dadurch nicht mehr auseinanderlaufen.
11. **CITATION.cff ("minimum CFF") ist der externe CFF-1.2.0-Standard,
    keine FDOx-eigene Erfindung — `fdo-squirrel` liest nur einen Ausschnitt
    davon, und zwar einen kleineren, als die eigene Crosswalk-YAML nahelegt.**
    `crosswalks/crosswalk.fdo-metadata.yaml` bildet 22 CFF-Felder auf RDF-
    Prädikate ab. Aber `crosswalks/citation_crosswalk_engine.py`s
    `_normalize_citation()` liest den echten `CITATION.cff`-Dict vorher auf
    eine feste Allow-Liste herunter: nur `abstract`, `url`,
    `repository-code`, `repository`, `license`, `keywords`, `identifiers`
    (als `identifier_<scheme>`) und `authors` (aufgespalten in
    `author_orcid[]`/`author_name[]`) kommen durch. Die übrigen 14
    kartierten Felder — u. a. `title`, `version`, `date-released`, `doi`,
    `contributors`, `cff-version` — werden von der Crosswalk-Schleife nie
    gefunden (`citation.get(source_field)` liefert `None`) und erzeugen
    **keine** Tripel, obwohl sie in der YAML stehen und im Beispiel-
    `CITATION.cff` sogar ausgefüllt sind. Vermutlich unschädlich in der
    Praxis (Titel/Version/Datum kommen fürs FDO ohnehin aus `MD.cff`), aber
    ein `CITATION.cff`, das nur diese Felder ausfüllt, sieht im RDF nichts
    davon. Nicht selbst gefixt (anderes Repo, A3) — nur im neuen Diagramm
    sichtbar gemacht (S6), damit es nicht implizit als "funktioniert"
    dargestellt wird.
12. **"Role classification" und "Crosswalk & Mapping Rules" sind
    parallele, unabhängige Zweige — kein Nacheinander.** Am echten
    `main.py` abgelesen: `DATA --> ROLES` (Rollenklassifikation kommt
    direkt aus den ZIP-Rohdaten) und `INGEST --> CROSSWALK` (Crosswalk
    kommt aus dem schema-validierten `MD.cff`) sind zwei getrennte
    Startpunkte, die beide unabhängig in `fdo-metadata.ttl` und
    `Provenance tracking` münden. Die einspaltige Darstellung in S4s
    erster Fassung erzwang eine Reihenfolge, die es im Code nicht gibt —
    und zwang genau deshalb eine der beiden Verbindungslinien (Crosswalk
    → Provenance), diagonal **durch** die jeweils andere Box zu laufen,
    weil die eine physisch zwischen Quelle und Ziel der anderen lag
    (gemeldet von Flo als "Kacheln in der Mitte", 2026-09-08). Fix: echte
    Gabelung, zwei Boxen nebeneinander statt gestapelt — löst das Problem
    strukturell, nicht nur durch eine andere Linienführung.
13. **Die erste `fdox-citation-cff-schema.svg`-Fassung (S6) hatte zwei
    Boxen mit demselben Klassennamen "CITATION_cff"** (eine für
    "forwarded to RDF", eine für "not forwarded") — von Flo direkt als
    "verstehe ich nicht" zurückgemeldet, zu Recht: zwei gleichnamige
    Klassenboxen lesen sich wie ein Diagrammfehler, nicht wie eine
    bewusste Aufteilung nach Laufzeitverhalten, und die Verbindungslinien
    zu `Author`/`Identifier` mussten dadurch weit kreuzen. Fix: eine
    Klasse, Felder nach Bedeutung gruppiert (nicht nach RDF-Status),
    RDF-Status als `[not in RDF]`-Tag pro Feld — dieselbe
    Klammer-Konvention, die S5 schon für `[required]` benutzt.
    `authors`/`contributors`/`identifiers` bewusst benachbart platziert,
    damit `Author`/`Identifier` direkt danebenstehen können und die
    Linien nicht mehr durchs ganze Diagramm laufen müssen.

## A2. Zielbild

```
py/step_*.py  (reine Geometrie + Text, keine Rasterlogik)
     │
     ▼  main.py orchestriert
img/*.svg     (Quelle, versioniert)
     │
     ▼  resvg-py, in-process, vendorte Fira-Sans-Dateien als font_files=
img/*.png     (Endprodukt, transparenter Hintergrund, für Folien/Druck/Web)
```

Eigenschaften, an denen sich ein Rebuild messen lassen muss:

- **Kein externes CLI-Tool.** `pip install -r requirements.txt` genügt;
  kein `rsvg-convert`, kein ImageMagick, kein Node.
- **Deterministisch.** Zwei Läufe hintereinander erzeugen bytegleiche
  `.svg`/`.png` (geprüft per `md5sum`, S1).
- **Eine Palette, eine Quelle.** Farben und Schrift stehen einmal in
  `py/visuals_utils.py`; kein Skript trägt einen Hex-Code, der nicht von
  dort importiert ist.
- **Schrift vendored, nicht referenziert.** `fonts/*.ttf` liegt im Repo,
  `@font-face` zeigt relativ dorthin — ein frischer Klon rendert identisch,
  ohne dass Fira Sans auf der Maschine installiert sein muss.

## A3. Querschnittsregeln

- Reuse heisst kopieren, nicht referenzieren (Fira-Sans-Dateien liegen im
  Repo, keine Google-Fonts-URL zur Laufzeit).
- Kein `datetime.now()`, kein `random` in den Generatoren — beide Regeln
  sind hier trivial erfüllt, da keine Zeit- oder Zufallswerte je gebraucht
  wurden (nicht nur vermieden, sondern kommt im Code gar nicht vor).
- Zwei Läufe hintereinander, `git status` sauber (A1, Befund geprüft).
- Diese Familienregel: **die Palette lebt in `py/visuals_utils.py`**, nicht
  in jedem `step_*.py` einzeln — vermeidet genau die "welches Blau war das
  nochmal"-Situation, die diesen Chat ausgelöst hat.
- Windows/cmd ist die Referenzplattform; alle Befehle unten sind
  Einzeiler.

## A4. Beschlusslage

| Frage | Beschluss | seit |
|---|---|---|
| Rendering-Weg | **`resvg-py`** (Rust-Wheel, Renderer statisch enthalten) — ersetzt `cairosvg`, das trotz `pip install` eine System-`libcairo` brauchte und auf Windows real fehlschlug (Befund A1.5) | 2026-09-08, ersetzt Beschluss vom selben Tag |
| Schriftart | Fira Sans (Regular 400, Bold 700), vendored aus `github.com/mozilla/Fira`, SIL OFL 1.1 | 2026-09-08 |
| FDOx-Blau | `#004473` (Pixel-Wert aus dem Referenzbild), Step 1 **und** FDO-Meta-Grafik teilen sich diesen Wert | 2026-09-08 |
| Repo-Name | `fdox-visuals`, **Vorschlag** — Flo legt das eigentliche GitHub-Repo an, Name kann beim Anlegen noch geändert werden | 2026-09-08, Vorschlag |
| Ordner für Produkte | `img/` (nicht `dist/`) — Familienkonvention für Repos, deren Hauptprodukt Abbildungen sind | 2026-09-08 |
| `img/` in Git? | ja, versioniert (wie `dist/` bei den anderen Repos) — die Bilder sind das citierbare Produkt, nicht nur Baustellenabfall | 2026-09-08, Vorschlag |
| Ausgabeformat | **`.png`, transparenter Hintergrund** — ersetzt `.jpg` auf weißem Grund mit dezentem Dot-Grid-Muster; das Muster war auf Weiß gedacht, wurde beim Reinzoomen (Flos Screenshot) aber als sichtbare Punkte im Hintergrund wahrgenommen. Dot-Grid komplett entfernt statt nur den Hintergrund transparent zu machen — es hätte ohne definierten Untergrund keinen Sinn ergeben | 2026-09-08, ersetzt Beschluss vom selben Tag |
| Auflösung | **Zurückgenommen** von "so hoch wie möglich" auf einen Zielbereich von ~2–6 Megapixel *Inhalt* (nach dem Trim) je Grafik — Google Slides komprimiert eingefügte Bilder oberhalb von 25 Megapixel zwangsweise (offizielle API-Grenze) und beginnt in der Praxis schon deutlich darunter sichtbar zu degradieren. `OVERSAMPLE`/`ICON_SCALE` entsprechend gesenkt (Banner 3→1,5; Icons 6→4; FDO-Meta-Grafik 3,5→2,5) | 2026-09-08, ersetzt Beschluss vom selben Tag |
| Ordner in `img/` | **acht Themenordner**: `pattern`, `schemas`, `talk-process`, `talk-purpose`, `talk-closing`, `git-packager`, `federation`, `ogham-graph`; Zuordnung über den Dateinamen (`CATEGORIES` in `visuals_utils.py`); SVGs verweisen deshalb mit `../../fonts` auf die Schrift. `img/source/` bleibt | 2026-11-05 |
| Website | GitHub Pages aus `main`/`docs`, statisches HTML (kein Jekyll-Build, `.nojekyll`), Layout des Skills `figure-pages-site` mit Akzent FDOx-Blau; S11–S13 öffentlich mit Hinweis "Draft, as of 2026-11-05" (seit S17 ersetzt: nur Planungsgrafiken tragen das Etikett "Concept", siehe unten) | 2026-11-05 |
| Transparenter Rand | **maximal 10px** um jede Grafik, für alle sechs PNGs einheitlich — per `trim_transparent_border()` auf Pixelebene zugeschnitten (Alphakanal-Bounding-Box + fester Rand), nicht per geschätztem Design-Koordinaten-Abstand. Grund für den Pixel-Ansatz statt Geometrie-Rechnung: Schritt 4s Titeltext reicht nachweislich über den Icon-Kreis hinaus (siehe A1, neuer Befund) — eine Design-Koordinaten-Schätzung hätte das riskiert abzuschneiden | 2026-09-08 |
| RO-Crate und Signposting in den Grafiken (S16) | Architekturdiagramm (S4) um die Zeile "Signposting & RO-Crate" und eine Ausgabebox ergänzt; dabei die veraltete Angabe "Mermaid → JPG" auf PNG korrigiert (`fdo-squirrel` S19). Neue Grafik `fdox-bundle-three-views` (Kategorie `schemas`, Schritt `bundle-views`): ein Bundle, drei Sichten (TTL verlustfrei, RO-Crate, Landing Page). Flos Entscheidung im Dialog | 2026-11-16 |
| RO-Crate-Logo (S16) | Eingebunden ist das Logo der RO-Crate Community (Lizenz CC BY 4.0, laut Flo), Datei `img/source/ro-crate-logo.png` (auf 400 × 400 Pixel verkleinert, sonst unverändert; Original 1920 × 1920). Quelle, Lizenz und Änderung stehen in `img/source/NOTICE.md`. CC BY verlangt Namensnennung: die Grafik trägt sie selbst ("RO-Crate logo: RO-Crate Community, CC BY 4.0"), ebenso ihre Bildunterschrift auf der Seite. `ro_crate_logo()` nimmt zuerst eine `ro-crate-logo.svg`, falls jemand eine ablegt, sonst das PNG; fehlt beides, steht ein Textpill "RO-Crate" an der Stelle und der Lauf bleibt auch unter `--strict` ohne Fehler | 2026-11-16 |
| Bilder-Pool-Seite (S17) | Die Site ist ein Bilder-Pool für Vorträge, Poster und Papers. Navigation und Startseite nach Gruppen (Concept; 3D models; Software; 3D and software, d. h. Story, Federation, Ogham-Graphen; Flos Wunsch, 3D und Software stärker zu trennen); Titel und Bildunterschriften ohne "Talk", "Slide" und "Closing" (die Kategorien beschreiben den Inhalt, nicht den Verwendungszweck; Flos Wunsch, Vortrag und Software selbst auszuwählen; Slugs, Dateinamen und Kürzel TP/TU/TC/ST bleiben, damit Links und Verweise halten). Das Etikett "Draft, as of 2026-11-05" entfällt; nur Grafiken über Geplantes tragen "Concept: planned, not implemented yet" (alle `git-packager`-Grafiken und `fdox-talk-story-two-roads-unicorn`), die Kategorie `git-packager` zusätzlich einen Hinweis. Alles andere gilt als gebaut aus veröffentlichten Werkzeugen und Registry-Daten; die Quellzeile nennt den Stand. Flos Auftrag; die Wahl, was "Concept" ist, ist Claudes Vorschlag, von Flo noch zu bestätigen | 2026-11-16 |
| Kreuzungsfreie Graphen (S17) | In Graphen und Fächern werden Reihenfolgen so gewählt, dass sich Kanten nicht kreuzen: `purpose3` (Zeilen- und Hubreihenfolge per Brute-Force, eine Kreuzung statt elf), `shared-concepts` (je Konzept ein vertikaler Bus mit Punkten, Zeilen nach Zugehörigkeit sortiert), Registry-Graph (CHUIS/1 unter Q2016147, Beuys und Freshford getauscht). Neue Graphen: erst Reihenfolge prüfen, dann zeichnen | 2026-11-16 |
| RO-Crate in Schritt 1 (S17) | Die beiden Schritt-1-Folien nennen `fdo-3d-packager` v1.1.0 (statt v1.0.0), unter dem Bündel "RDF · RO-Crate · landing page" und zeigen dort das RDF- und das RO-Crate-Logo (Nennung unten links in der Folie, `logo()`/`logo_credits()`). Schritte 2 bis 4 bleiben: sie zeigen Werte, nicht Ausgabeformate | 2026-11-16 |
| Entwurfsfolien S11/S12 bleiben unverändert (S16; S17 ändert nur `shared-concepts` im Layout) | `fdox-talk-federation-*` und `fdox-talk-git-packager-*` nennen `fdo-metadata.ttl` als Beleg bzw. als Inhalt der bestehenden Zenodo-Records; diese Records (`fdo-squirrel` v1.0.x) haben kein Crate. RO-Crate dort erst aufnehmen, wenn die Registry Crate-Bundles führt. Claude-Vorschlag, von Flo noch zu bestätigen | 2026-11-16, Vorschlag |

## A5. Was in welchem Chat hochgeladen wird

Das ganze Repo als ZIP (robocopy-Bundle unten), **ohne** `img/*.png`
(Zwischenstufen, werden von `.gitignore` sowieso nicht committet — siehe
dort) und ohne `.git/`.

```cmd
robocopy fdox-visuals fdox-visuals-bundle /E /XD .git __pycache__
```

---

# Teil B — Schrittübersicht

| ID | Schritt | Repo | hängt ab von | Status |
|---|---|---|---|---|
| S0 | Festlegungen: Rendering-Weg, Schrift, Blau, Repo-Layout | fdox-visuals | — | erledigt 2026-09-08 |
| S1 | Skeleton: `main.py`, `py/visuals_utils.py`, `requirements.txt`, Lizenz | fdox-visuals | S0 | erledigt 2026-09-08 |
| S2 | Vier-Schritte-Muster-Banner + 4 Icon-Badges | fdox-visuals | S1 | erledigt 2026-09-08 |
| S3 | FAIR-Digital-Object-Meta-Grafik | fdox-visuals | S1 | erledigt 2026-09-08 |
| S4 | fdo-squirrel-Architekturdiagramm (korrigiert) | fdox-visuals | S1 | erledigt 2026-09-08 |
| S5 | MD.cff-Schema-Klassendiagramm (neu, kein Vorbild-Skript) | fdox-visuals | S1 | erledigt 2026-09-08 |
| S6 | CITATION.cff-Schema-Diagramm ("minimum CFF", neu) | fdox-visuals | S1 | erledigt 2026-09-08 |
| S7 | FDOx-Zweck-Banner ("What does FDOx do?") + 4 Icon-Badges | fdox-visuals | S1 | erledigt 2026-09-09 |
| S8 | Talk-Prozess-Folien: die vier Schritte, je eine reale Folie | fdox-visuals | S1, S2 | erledigt 2026-09-09 |
| S9 | Talk-Zweck-Folien: die vier Ergebnisse, je eine reale Folie | fdox-visuals | S1, S7 | erledigt 2026-09-09 |
| S10 | Abschlussfolie: acht Badges als Ring um die FDO-Kugel, 2 Varianten | fdox-visuals | S1, S2, S3, S7 | erledigt 2026-09-10 |
| S11 | `fdo-git-packager` (Konzept): Banner, vier Schritt-Folien, vier Badges, GitHub-Actions-Swimlane (reales Beispiel SPARQLing Unicorn) | fdox-visuals | S1, S2, S8 | Entwurf 2026-11-05, wartet auf Abnahme |
| S12 | Fertige 3D-/Software-FDOs im Federated-KG-Ökosystem: drei Folien (Weg, Katalog, geteilte Konzepte) | fdox-visuals | S1, S11 | Entwurf 2026-11-05, wartet auf Abnahme |
| S13 | Echte Graphbilder: Ogham-3D-FDOs, Software, Registry als Graph (drei Folien) | fdox-visuals | S1, S12 | Entwurf 2026-11-05, wartet auf Abnahme |
| S14 | Themenordner `img/<kategorie>/` und GitHub-Pages-Seite `docs/` (Skill figure-pages-site, FDOx-Blau) | fdox-visuals | S1–S13 | Entwurf 2026-11-05, wartet auf Abnahme |
| S15 | Story-Folien: FKGE-Landkarte, "Zwei Straßen, ein Bündel" (CIIC 81 + Unicorn / + Extractor), Squilly-Graph; Schritt 1 zusätzlich mit CIIC 81 | fdox-visuals | S1, S8, S11–S14 | Entwurf 2026-11-05, wartet auf Abnahme |
| S16 | RO-Crate und Signposting in den Grafiken: Architekturdiagramm (S4) erweitert, neue Grafik "ein Bundle, drei Sichten", RO-Crate- und RDF-Logo | fdox-visuals | S4, `fdo-squirrel` v1.1.0 | fertig, committet 2026-11-16 (2e573e6) |
| S17 | Bilder-Pool: Seitenstruktur (Gruppen, Titel ohne "Talk:", "Concept" statt "Draft"), Kreuzungen in Graphen beseitigt, RO-Crate in Schritt 1 | fdox-visuals | S11–S16 | fertig, committet 2026-11-16 (ca3f1f0) |
| S18 | Lebendige Galerie: neutrale Namen ohne "talk", Piktogramme auf eigene Unterseiten, kein Nutzungshinweis | fdox-visuals | S14, S17 | fertig, committet 2026-11-16 (1b8928b) |
| S19 | Graph-Bilder ohne Header/Footer, transparent und eng beschnitten; sechs Piktogramme für fdo-3d-packager | fdox-visuals | S13, S15, S18 | fertig, committet 2026-11-16 (f857e27) |
| S20 | 3D-Packager-Piktogramme in Step 1 und in den "two roads"-Bildern eingebunden statt Textboxen | fdox-visuals | S8, S15, S19 | fertig, committet 2026-11-16 |
| S21 | Keine Versionsangabe des fdo-3d-packager mehr in den Grafiken | fdox-visuals | S20 | fertig, committet 2026-11-16 (9e65a72) |
| S22 | Urheberzeile der Doku: "Florian Thiery, Research Squirrel Engineers Network / LEIZA" | fdox-visuals | S14 | fertig, committet 2026-11-16 (67bfc23) |
| S23 | Affiliation in `CITATION.cff` angeglichen | fdox-visuals | S22 | Entwurf 2026-11-16, wartet auf Abnahme |

S2–S5 sind alle unabhängig voneinander (hängen nur von S1 ab) und können
in beliebiger Reihenfolge laufen — `main.py --only fdo-meta` läuft ohne
dass `pattern` vorher gelaufen sein muss.

---

# Teil C — Die Schritte

## S1 — Skeleton

**Ziel:** `python main.py --list`/`--dry-run` laufen ohne `resvg-py`/`Pillow`
zu importieren; `python main.py` erzeugt beide Grafiken; zwei Läufe
hintereinander sind bytegleich.

**Uploads:** Standardbundle (A5).

`py/visuals_utils.py` hält `STEPS` (die Familienpalette, Step 1 = `#004473`),
`INK`/`MUTED`/`BG`, `font_face_css()`, `render_svg_to_png()` sowie
`flatten_to_jpg()` (aktuell von keinem Schritt genutzt, seit beide Grafiken
transparent bleiben — bewusst nicht entfernt, für den Tag, an dem ein
künftiges Skript wirklich ein flaches JPG braucht). Jeder `step_*.py`
importiert von dort, trägt selbst keinen Hex-Code für Ink/Muted/Background.

**Abnahme:** ✅ erledigt — `--list` und `--dry-run` unter 0,1 s (kein
schweren Renderer-Import), `python main.py` erzeugt alle sieben Dateien,
zweiter Lauf `md5sum`-identisch zum ersten (siehe A1 Befund 1).

### Nachtrag 2026-09-08 — cairosvg auf Flos Windows-Rechner gescheitert, ersetzt durch resvg-py

Erster echter Lauf nach `git commit`/`push` auf Windows:

```
ERROR: no library called "cairo-2" was found
...
cannot load library 'libcairo-2.dll': error 0x7e. [...] did not manage to
locate a library called 'libcairo-2.dll'
```

Ursache: `cairosvg` ist zwar ein `pip`-Paket, bindet zur Laufzeit aber an
eine System-`libcairo` (`ctypes.util.find_library`). Im Sandkasten lief es
nur, weil `librsvg2-bin` (für einen früheren, unabhängigen Versuch per
`apt` installiert) `libcairo2` als transitive Abhängigkeit mitgebracht
hatte — auf einer sauberen Windows-Installation ist davon nichts vorhanden.
Die A2-Eigenschaft "kein externes CLI-Tool nötig" war damit nur zufällig
erfüllt, nicht durch `cairosvg` selbst.

Fix: `resvg-py` (siehe A1 Befund 5). Verifiziert per `ldd` gegen die
kompilierte Erweiterung (`resvg_py.abi3.so`): sie linkt ausschließlich
gegen `libc`/`libgcc_s`/`libpthread`/`libm` — keine `libcairo`, kein
`pango`, kein `fontconfig`, nichts Grafikbezogenes. Der Renderer ist
tatsächlich vollständig einkompiliert, nicht nur zufällig lauffähig wie
`cairosvg` im Sandkasten. Alle sieben Dateien erneut erzeugt, bytegleich
zu den vorher mit `cairosvg` erzeugten.

### Nachtrag 2026-09-08 (2) — `trim_transparent_border()` ergänzt, Auflösung zurückgenommen

Zwei Meldungen von Flo, ein gemeinsamer Fix: (a) Google Slides zeigte die
Grafiken unscharf an (Ursache: 25-MP-Grenze der Slides-API, siehe A1
Befund 6 — der alte Banner lag bei ~37,5 MP), (b) `fdox-fair-digital-object-meta-graphic.png`
und `fdox-four-step-pattern.png` hatten deutlich mehr transparenten
Rand als die vier Icon-Badges.

`trim_transparent_border(png_path, margin_px=10)` neu in
`visuals_utils.py`: öffnet das gerenderte PNG, ermittelt die Bounding-Box
des Alphakanals (`Image.split()[-1].getbbox()`), schneidet zu, packt exakt
`margin_px` transparente Pixel drumherum. Bewusst pixelbasiert statt über
Design-Koordinaten geschätzt — siehe A1 Befund 7 (Schritt 4s Text reicht
über den Icon-Kreis hinaus, eine geschätzte Marge hätte das riskiert
abgeschnitten). Wird nach jedem `render_svg_to_png()`-Aufruf in S2 und S3
aufgerufen.

Gleichzeitig `OVERSAMPLE`/`ICON_SCALE` gesenkt (Details: A4-Zeile
"Auflösung"), da nach dem Trim der *Inhalt* zählt, nicht die vorher große,
leere Canvas — bei gleicher `OVERSAMPLE` wäre allein der Inhalt der
Banner-Grafik schon bei ~21 MP gelegen.

**Verifiziert:** `PIL`-Bounding-Box-Kontrolle auf allen sechs PNGs ergibt
exakt `(10, 10, 10, 10)` (links/oben/rechts/unten); Pixel-genaue
Alphakanal-Prüfung an allen vier Rändern der FDO-Meta-Grafik (nicht nur
Sichtprüfung — eine erste Sichtprüfung auf einer herunterskalierten
Vorschau sah fälschlich nach Beschnitt aus, siehe unten) zeigt einen
sauberen Übergang von Inhalt zu vollständig transparent genau bei Pixel
10. Alle sechs Dateien liegen zwischen 1,8 MP (Icons) und 5,7 MP (die
beiden großen Grafiken) — weit unter der 25-MP-Grenze. Zwei Läufe
hintereinander bytegleich, `git status --short` danach leer.

**Nebenbefund:** eine herunterskalierte Vorschau (z. B. das
`view`-Werkzeug beim Betrachten eines 3293×1728-Bildes) macht einen
10px-Rand gegen fetten Text optisch fast unsichtbar — das sah beim ersten
Hinsehen nach Beschnitt aus, war aber keiner. Bei so kleinen Rand-Werten
lohnt sich die Pixel-Prüfung (`numpy`-Array auf die letzten/ersten N
Zeilen/Spalten), nicht nur der visuelle Eindruck einer Vorschau.

## S2 — Vier-Schritte-Muster-Banner + Icon-Badges

**Ziel:** `img/fdox-four-step-pattern.svg`/`.png` (nur die vier Schritte,
kein Header/Footer — Beschluss aus dem Ursprungschat; transparenter
Hintergrund) sowie vier freistehende `img/fdox-step-<n>-<slug>.svg`/`.png`
mit transparentem Hintergrund.

**Uploads:** —

Geometrie 1:1 aus dem Ursprungschat übernommen (wachsendes Graph-Icon-
System: 1 Knoten → Knoten+2 Satelliten → Hub+2 externe Ringe → 5-Knoten-
Netz; Zahlen-Tag oben links am Badge). Einzige Änderung: Schrift jetzt
Fira Sans, Step-1-Farbe jetzt `#004473` statt der zunächst probeweise
verwendeten `#2451D6`.

**Abnahme:** ✅ erledigt — alle fünf Dateipaare erzeugt, PNGs mit Alphakanal
(`PIL.Image.mode == "RGBA"` geprüft), Banner-Titel/Footer tatsächlich
abwesend (Beschluss aus dem vorherigen Chat, hier nur reproduziert).

### Nachtrag 2026-09-08 — Dot-Grid-Hintergrund entfernt, Banner jetzt auch transparentes PNG

Flo meldete (Screenshot, Zoom auf Step 2/3): das dezente Dot-Grid-Muster
hinter dem Banner (5 % Deckkraft, für den weissen JPG-Hintergrund gedacht)
war beim Reinzoomen als sichtbare Punkte wahrnehmbar. Statt nur den
Hintergrund transparent zu machen (die Punkte hätten dann lose auf jeder
beliebigen Folienfarbe geschwommen — ergibt ohne definierten Untergrund
keinen Sinn), das `<pattern id="dotgrid">` komplett aus
`_build_content_svg()` entfernt. Banner erzeugt jetzt `.png` statt `.jpg`
(kein `flatten_to_jpg()`-Aufruf mehr für diesen Schritt), Auflösung dabei
von `OVERSAMPLE=2` auf `3` angehoben (jetzt 11520×3252). Icon-Badges
unverändert in der Struktur, nur `ICON_SCALE` von `4` auf `6` angehoben
(jetzt 2436×2436 je Badge). Geprüft: Komposit auf Schachbrett-Muster
(Pillow) zeigt sauberen Alphakanal, keine Restpunkte; zwei Läufe
hintereinander weiterhin bytegleich, `git status --short` danach leer.

## S3 — FAIR-Digital-Object-Meta-Grafik

**Ziel:** `img/fdox-fair-digital-object-meta-graphic.svg`/`.png`
(transparenter Hintergrund) — dieselbe Komposition wie das hochgeladene
Referenzbild (Titel links, verschachtelte Kreise rechts, drei Leader-Lines
zu Data/Metadata/PID), umgefärbt auf `#004473` (Kern) und eine
65-%-Aufhellung davon (Ring, ersetzt das ursprüngliche Grau).

**Uploads:** —

Zielpunkte der drei Leader-Lines sind geometrisch berechnet, nicht
abgepaust: Data landet per Konstruktion innerhalb des inneren Kreises,
Metadata im Ring-Band, PID exakt auf dem äusseren Rand (Radius = `OUTER_R`).

**Abnahme:** ✅ erledigt — Sichtprüfung (Crop-Zoom) bestätigt, dass alle drei
Linien in der beabsichtigten Zone landen; Akzentfarbe im Log bestätigt
(`accent #004473`).

### Nachtrag 2026-09-08 — ebenfalls auf transparentes PNG umgestellt

Gleicher Anlass wie bei S2 (Flos "alles als PNG mit transparentem
Hintergrund"), auch wenn diese Grafik nie ein Dot-Grid hatte — nur der
weisse `<rect>`-Hintergrund entfernt, `OVERSAMPLE` von `2.5` auf `3.5`
angehoben (jetzt 5600×3500). `flatten_to_jpg()` bleibt ungenutzt in
`visuals_utils.py` (siehe A2).

### Nachtrag 2026-09-10 — `img/fdox-fdo-sphere.svg`/`.png`: die Kugel allein

Flo: "kannst du aus `fdox-fair-digital-object-meta-graphic` noch die
'FDOx Kugel' rechts ohne den Text links als alleinige Symbolgrafik
erstellen?" — `_build_sphere_svg()` zeichnet dieselben zwei Kreise mit
denselben Modulkonstanten (`OUTER_R`, `INNER_R`, `ACCENT`,
`ACCENT_STROKE`, `RING_FILL`) noch einmal auf ein eigenes, quadratisches
`viewBox`, ohne Titeltext und ohne die drei Leader-Lines/Labels — kein
zweiter Satz Radien/Farben daneben (A3). `run()` schreibt jetzt zwei
Dateipaare statt eines; das bestehende
`fdox-fair-digital-object-meta-graphic.png` bleibt dabei unverändert
(gegen einen frischen Klon bytegleich geprüft).

**Abnahme:** ✅ erledigt — `python main.py --only fdo-meta --strict` läuft
fehlerfrei und schreibt beide Paare; zwei Läufe hintereinander bytegleich
(`md5sum`); `fdox-fair-digital-object-meta-graphic.png` gegen einen
frischen Klon per `cmp` als unverändert bestätigt. Kugel-PNG 1636×1636
nach Trim, transparenter Hintergrund, `PIL.Image.mode == "RGBA"` geprüft.

---

## S4 — fdo-squirrel-Architekturdiagramm (korrigiert)

**Ziel:** `img/fdox-fdo-squirrel-architecture.svg`/`.png` — dieselbe
3-Panel-Struktur wie `fdo-squirrel/architecture.mermaid`
(FDO-ZIP-Package → fdo-squirrel → Derived Outputs), im Familienstil neu
gezeichnet und um die drei fehlenden Pipeline-Stufen ergänzt (siehe A1
Befund 8): Schema-Validierung, Mermaid→JPG-Übersichtsgrafik,
Bundle-Finalisierung.

**Uploads:** die beiden von Flo hochgeladenen Referenzbilder (Architektur
+ MD.cff-Klassendiagramm); `fdo-squirrel` frisch geklont für die
Gegenprüfung gegen `main.py`.

Panel-Akzente aus der Vier-Schritte-Familie wiederverwendet statt neue
Farben erfunden: Eingabe = Step-1-Blau, Verarbeitung = Step-2-Teal,
Ausgabe = Step-4-Violett (Step-3-Gold bewusst ausgelassen, das ist
"Linking to Community Hubs" vorbehalten). Sieben Verarbeitungsschritte
statt vorher vier, in der tatsächlichen Reihenfolge aus `main()`:
Metadata ingest → Schema validation → Crosswalk & Mapping Rules →
Provenance tracking (zusammen mit Role classification) → Overview
diagram → Bundle finalisation. Vier Ausgaben statt vorher zwei:
`fdo-metadata.ttl`, `rdf_modelling_report`, `fdo_overview`,
`<slug>-fdo-bundle.zip`.

**Abnahme:** ✅ erledigt — jede Box/jeder Pfeil entspricht einem realen
`import`/Funktionsaufruf in `fdo-squirrel/main.py` (nicht nur eine
Vermutung); Sichtprüfung zeigt keine überlappenden Boxen oder
abgeschnittenen Text; 3188×1841 vor Trim, danach exakt 10px Rand,
5,87 MP (Slides-sicher).

### Nachtrag 2026-09-08 (2) — "Kacheln" am unteren Rand behoben

Siehe A1 Befund 10 für die Ursache. Fix bestätigt: unterer Rand der
"Bundle finalisation"-Box liegt jetzt vollständig innerhalb ihres Panels
(Crop-Zoom auf den unteren Bildstreifen vor/nach dem Fix verglichen).
Nebenwirkung des Fixes: Canvas ist jetzt 1913 statt 1841px hoch (der Fix
schafft mehr Bodenabstand, nicht weniger — die alte Zahl war zu knapp
bemessen, nicht zu großzügig). Erneut deterministisch, `git status`
danach leer.

### Nachtrag 2026-09-08 (3) — echte Gabelung statt gestapelter Boxen

Siehe A1 Befund 12. "Role classification" und "Crosswalk & Mapping
Rules" sind jetzt zwei halbbreite Boxen nebeneinander (`FORK_LEFT`/
`FORK_RIGHT`) statt zwei gestapelte Zeilen. `PROCESS_BOX_W` dafür auf
760 angehoben (vorher 480) — bei der alten Breite überlappte sich der
Text der beiden halbbreiten Boxen. Verbindung zu `fdo-metadata.ttl`:
Crosswalk (rechte Hälfte) geht direkt nach rechts raus; Role
classification (linke Hälfte) kann das nicht ohne Crosswalk zu kreuzen,
läuft daher über eine Ecken-Route (`_elbow_arrow`, rechtwinklig) durch
die leere Lücke oberhalb der Gabel-Zeile — offener Raum, keine Box im
Weg. Verbindung zu Provenance tracking: beide Hälften fallen einfach
senkrecht nach unten, treffen an zwei verschiedenen x-Positionen auf
Provenance' Oberkante — sauberer Trichter, keine Diagonale durch eine
Box mehr. Canvas jetzt 3692×1672 (breiter wegen der Gabel, aber flacher,
da eine Zeile weniger als vorher: 6 statt 7). Zoom-Vergleich vor/nach
bestätigt: keine Linie läuft mehr durch eine Box. 6,17 MP, weiterhin
Slides-sicher, 10px Rand, deterministisch, `git status` danach leer.

## S5 — MD.cff-Schema-Klassendiagramm (neu)

**Ziel:** `img/fdox-md-cff-schema.svg`/`.png` — UML-artiges
Klassendiagramm der zentralen `MD_cff`-Klasse mit allen 13 verwandten
Strukturen aus `fdo-squirrel-spec/data/raw/MD.cff-schema.yaml`, korrekt
gegen das Schema geprüft (siehe A1 Befund 9 für die konkreten Abweichungen
zum alten, hochgeladenen Bild).

**Uploads:** `fdo-squirrel-spec` frisch geklont, `data/raw/MD.cff-schema.yaml`
Feld für Feld gelesen (nicht nur die `required`-Liste, auch jedes `$defs`-
Unterschema).

Zwei Spalten links/rechts der zentralen `MD_cff`-Box (7 links, 6 rechts),
Kardinalität als Label an der Linie, `FDO_Class_Vocab` weiterhin mit
gestrichelter Linie (Typ-Constraint statt Enthält-Beziehung — das war im
Originalbild schon richtig und wurde beibehalten). Verschachtelte
Unterobjekte (z. B. `HeritageObject.object_type`, `Technique.acquisition`)
werden als einzelne `object`-Attribute gelistet statt weiter aufgeklappt —
gleiche Abstraktionstiefe wie im ursprünglichen Referenzbild, damit das
Diagramm lesbar bleibt.

**Abnahme:** ✅ erledigt — alle 13 Satelliten-Klassen samt Feldern und
Pflicht-Markierungen stammen wörtlich aus dem Schema (kein Feld erfunden,
keins ausgelassen außer den bewusst nicht aufgeklappten Unterobjekten);
`1..*` bei Publishers per `grep` auf die SVG-Quelle bestätigt (nicht nur
Sichtprüfung — bei 19px Schriftgröße rücken zwei Punkte optisch
zusammen und sahen im ersten Screenshot wie ein einzelner Punkt aus).
2394×2401 vor Trim, danach exakt 10px Rand, 5,75 MP.

## S6 — CITATION.cff-Schema-Diagramm ("minimum CFF")

**Ziel:** `img/fdox-citation-cff-schema.svg`/`.png` — anders als S5 keine
FDOx-eigene Schema-Definition, sondern der externe CFF-1.2.0-Standard,
so wie `fdo-squirrel` ihn tatsächlich liest (siehe A1 Befund 11).

**Uploads:** Flos drittes Referenzbild ("CITATION_cff"-Klassendiagramm,
ohne `md_cff_version`-Analogon, da CITATION.cff kein FDOx-Format ist);
`fdo-squirrel` erneut geklont, diesmal `crosswalks/crosswalk.fdo-metadata.yaml`
und `crosswalks/citation_crosswalk_engine.py` gegeneinander gelesen statt
nur die YAML.

**Eine** zentrale `CITATION_cff`-Box (nicht zwei — siehe A1 Befund 13 und
den Nachtrag unten), 22 Felder nach Bedeutung gruppiert (Identität,
Personen, Provenienz/Links, Lizenz, Repository), RDF-Status als
`[not in RDF]¹`-Tag pro Feld in gedämpftem Grau, dieselbe
Klammer-Konvention wie `[required]` in S5. `authors`/`contributors`/
`identifiers` bewusst benachbart platziert, `Author`- und
`Identifier`-Satelliten rechts daneben, direkt auf Höhe dieser drei
Zeilen. Fußnote im Bild selbst benennt Datei und Funktion
(`_normalize_citation()`), damit die Aussage überprüfbar bleibt, ohne
dass man diese PRIMER.md dafür lesen muss.

**Abnahme:** ✅ erledigt — alle 22 Felder stammen aus `grep "from_term:
cff:" crosswalks/crosswalk.fdo-metadata.yaml`, die Forwarded/Dropped-
Markierung aus `_normalize_citation()`s tatsächlichem Rückgabe-Dict
gegengeprüft (nicht geraten); 2507×1403 vor Trim, danach exakt 10px
Rand, 3,52 MP.

### Nachtrag 2026-09-08 — von zwei gleichnamigen Boxen auf eine Klasse umgestellt

Erste Fassung hatte zwei separate Boxen, beide betitelt "CITATION_cff"
(eine "forwarded to RDF", eine "mapped … not forwarded"). Flos Feedback:
"ich verstehe diese Grafik nicht" — zu Recht, siehe A1 Befund 13. Zwei
gleichnamige Klassenboxen lesen sich wie ein Fehler im Diagramm, nicht
wie eine bewusste Aufteilung nach Laufzeitverhalten, und die
Verbindungslinien zu `Author`/`Identifier` mussten dadurch weit über das
Bild kreuzen (Flo: "es überkreuzen sich nur Linien zwischen den Boxen").
Umgebaut auf eine einzelne Klasse mit Feldern in natürlicher Reihenfolge
(nicht nach RDF-Status sortiert) und dem `[not in RDF]`-Tag als
Attribut-Eigenschaft statt als Box-Trennkriterium — dieselbe Änderung,
die A1 Befund 13 beschreibt. Verifiziert: `authors`/`contributors` laufen
jetzt in einem gemeinsamen Punkt auf `Author` zusammen (keine Kreuzung
mehr, nur ein gemeinsamer Endpunkt), `identifiers`→`Identifier` läuft
separat und kreuzt nichts. 2507×1403, 10px Rand, 3,52 MP, deterministisch.

## S7 — FDOx-Zweck-Banner ("What does FDOx do?")

**Ziel:** `img/fdox-purpose-pattern.svg`/`.png` (nur die vier Eigenschaften,
kein Header/Footer, transparenter Hintergrund — dieselbe A4-Konvention wie
S2) sowie vier freistehende `img/fdox-purpose-<n>-<slug>.svg`/`.png`,
ebenfalls transparent.

**Uploads:** —, aus einer separaten Konversation übernommen (Flo hatte dort
bereits eine erste Fassung inkl. Header/Footer als Vorlage abgenommen —
"top!" — und danach die Kopfzeile/Fußzeile entfernt sowie die vier Icons
zusätzlich einzeln angefordert).

Bewusste Ergänzung zu S2, nicht dessen Ersatz: S2 benennt die vier
*Pipeline-Schritte* (Encapsulation → … → Federation), S7 die vier
resultierenden *Eigenschaften* eines veröffentlichten FDOx-Artefakts
(FAIR & Citable → Semantically Queryable → Interoperable → Integrable) —
dieselbe Geschichte, einmal als Prozess, einmal als Ergebnis. Deshalb
bewusst **eine** Farbe (`FDO_ACCENT`, geteilt mit Step 1) statt S2s
Vier-Farben-Regenbogen: S7 ist eine durchgehende Aussage über eine Art von
Objekt, keine vier verschiedenen Stationen. Zwei Aufhellungen davon
(`FDO_ACCENT_LIGHT` fürs Icon-Kreis-Gradient, `FDO_ACCENT_SOFT` für die
Pfeil-Chevrons zwischen den Spalten) wurden dafür einmalig in
`py/visuals_utils.py` ergänzt statt als Literal in `step_purpose.py` zu
stehen (A3).

Icon-Vokabular bewusst eigenständig (Dokument-Häkchen / RDF-Dreieck /
Hub-mit-vier-Speichen / drei verlinkte Cluster) statt S2s Knoten-Graph-
Icons wiederzuverwenden — die beiden Banner erzählen zwar dieselbe
Geschichte, sollen aber nicht wie zwei Varianten *derselben* Grafik
aussehen. Beschreibungstexte laufen durch dasselbe `wrap_text()` wie in
S2, keine Zeilenumbrüche von Hand gesetzt.

**Abnahme:** ✅ erledigt — frischer Klon, `python main.py --only purpose
--strict` läuft fehlerfrei, danach vollständiger `python main.py --strict`
(alle sieben Schritte) ebenfalls fehlerfrei und die fünf bereits
bestehenden Grafiken unverändert in Auflösung/Größe. Zwei Läufe
hintereinander bytegleich (`md5sum` aller zehn neuen Dateien), `git status
--short` zeigt danach nur die erwarteten neuen/geänderten Pfade. Banner
5000×1220 vor Trim (`OVERSAMPLE=2.5`) → 4355×1009 nach 10px Rand, 4,39 MP;
jedes Icon 1170×1170 nach Trim (`ICON_SCALE=5.6`), 1,37 MP,
`PIL.Image.mode == "RGBA"` geprüft.

---

## S8 — Talk-Prozess-Folien (die vier Schritte, je eine reale Folie)

**Ziel:** `img/fdox-talk-step{1..4}-*.png`/`.svg` — Begleiter zu S2s Banner,
aber pro Schritt eine volle 7:4-Foliengrafik statt Icon+Kurzbeschreibung,
mit echten Daten aus der Familie statt Abstraktion. Entstanden für den
10-Minuten-Vortrag "From Smartphone 3D to Federated Knowledge Graphs"
(FAIR 3D Heritage Conference, Mainz, 14.–16.09.2026), dort Teil "Part 5"
des Foliensatzes — konkret die Antwort auf Reviewer 4401s Kritik ("semantic
modelling zu generisch beschrieben, am Fallbeispiel konkretisieren").

**Uploads/Quelle:** aus einer separaten Konversation übernommen (mehrere
Iterationsrunden dort, "top!"/"besser"/"passt" als jeweilige Abnahme pro
Folie). Reale Werte stammen aus CIIC 81s echter `fdo-metadata.ttl`
(Zenodo-DOI `10.5281/zenodo.18724635`), aus einem echten Screenshot der
`fdo-squirrel-registry`-SPARQL-Seite (Query 3) und aus einem echten
Screenshot der Registry-Startseite (Release 2026-09-03, 8 Quellen, 7.793
Tripel) — keine dieser Zahlen ist erfunden oder geschätzt.

**Drei der vier Folien komponieren einen echten Screenshot/ein echtes
Foto** unter `img/source/` (Sketchfab-Seite von "Freshford: St Lachtain's
Well", die Registry-Startseite, CIIC 81s Vorschau-Render) **auf ein
gerendertes SVG-Grundbild** statt sie zu zeichnen — der eine Fall, den
`patch-zip-delivery`s eigene "Generated files"-Regel vorsieht: ein
Artefakt, das ein Skript grundsätzlich nicht selbst herstellen kann (kein
Browser, keine Kamera), wird als Daten mitgeliefert statt regeneriert.
Schritt 2s Folie ist reines SVG, kein Composite.

**Weißer statt transparenter Hintergrund, bewusst gegen A4.** Diese vier
Grafiken sind als *einziges* Bild auf einer Google-Slides-Folie gedacht,
nicht als Baustein, der auf anderem Inhalt sitzt — ein transparenter
Hintergrund hätte hier keinen Zweck, und ein Composite aus einem
gerenderten SVG und einem eingefügten Foto kann ohnehin nicht sauber
transparent bleiben. `visuals_utils.BG` (`#FFFFFF`) existierte als
Konstante bereits, war aber bislang ungenutzt (kein Schritt vor S8 wollte
einen weißen Hintergrund) — hier zum ersten Mal tatsächlich gebraucht.

**Icon-Badge fix, Inhalt zentriert sich darum — nicht umgekehrt.** Erste
Fassungen positionierten die Icon-Badge und den Inhalt getrennt von Hand;
zwei Nachträge in der Ursprungskonversation ("die Symbole ragen in die
Grafik"/"da sind die Symbole im Bild") zeigten, dass von Hand gewählte
Ränder bei unterschiedlich hohem Inhalt (mal ein Foto, mal ein Baum aus
Boxen) unterschiedlich knapp ausfallen. Fix, hier von Anfang an eingebaut:
`_render_balanced()` rendert einmal bei Verschiebung (0,0), misst per
`visuals_utils.measure_content_margins()` die tatsächlichen Pixelränder
**mit ausgespartem Badge-Bereich**, rechnet daraus die Verschiebung aus,
die Links/Rechts- bzw. Oben/Unten-Rand angleicht, und rendert damit final
neu — dieselbe Disziplin, die `trim_transparent_border()` schon für S2/S7
anwendet (A1 Befund 7: am echten gerenderten Alphakanal messen, nicht an
einer geschätzten Design-Koordinate), nur hier auf einem opaken statt
transparenten Bild und ohne zuzuschneiden, nur zu verschieben.

**Icon-Glyphen wiederverwendet, nicht neu gezeichnet.** `_node_icon()` wird
direkt aus `step_pattern` importiert (`from step_pattern import
_node_icon`) statt die SVG-Pfade der vier Schritt-Icons ein zweites Mal
abzutippen — A3 ("ein Palette, eine Quelle") gilt für Zeichenfunktionen
genauso wie für Farbwerte. Badge-Kreis, Eckfähnchen und Nummer sind hier
lokal nachgebaut (`_icon_svg()`), weil S8s Badges oben links statt
mittig sitzen und einen anderen Kreisradius/Eckfähnchen-Versatz brauchen
als S2s Banner-Badges — nur der Icon-*Inhalt* (die Linien/Punkte
innerhalb des Kreises) ist geteilt, nicht die ganze Badge-Komposition.

**Neue generische Zeichenhelfer in `visuals_utils.py`** (`arrow_line`,
`elbow_path`, `edge_label`, `label_box`, `paste_raster`,
`measure_content_margins`): reine String-Formatierer bzw. (bei
`paste_raster`) ein schlanker PIL-Aufruf, kein zusätzlicher schwerer
Import auf Modulebene — `--list`/`--dry-run` bleiben so schnell wie A2 es
verlangt. `edge_label()` dreht ein fett unterlegtes Label passend zum
Linienwinkel und legt einen weißen Rahmen dahinter, `label_box()` ist eine
verallgemeinerte Fassung der Boxen aus S4/S5/S6, `paste_raster()` fasst
das Skalieren+Einfügen eines Quellbilds in eine Zeile.

**Abnahme:** ✅ erledigt — frischer Klon, `python main.py --only
talk-process --strict` läuft fehlerfrei, danach vollständiger `python
main.py --strict` (alle acht Schritte) ebenfalls fehlerfrei und alle
zuvor bestehenden Grafiken laut `git status --short` unverändert. Zwei
Läufe von `step_talk_process.py` hintereinander bytegleich (`md5sum`
aller vier PNGs). Alle vier Folien mit den zuvor in der separaten
Konversation ausgelieferten Referenzbildern verglichen (Sichtprüfung,
Layout/Werte/Beschriftungen identisch). 3500×2000 pro Folie (7:4 bei
`OVERSAMPLE=2`), weißer Hintergrund, `PIL.Image.mode == "RGB"` geprüft.

## S9 — Talk-Zweck-Folien (die vier Ergebnisse, je eine reale Folie)

**Ziel:** `img/fdox-talk-purpose{1..4}-*.png`/`.svg` — Begleiter zu S7s
Banner, analog zu S8: eine volle 7:4-Foliengrafik pro Ergebnis
("FAIR & Citable" … "Integrable"), mit echten Zahlen aus der Registry statt
Icon+Kurzbeschreibung. Gleicher Vortrag, gleiche Foliensatz-"Part 5" wie
S8, die zweite Hälfte davon.

**Uploads/Quelle:** dieselbe separate Konversation wie S8, direkt im
Anschluss. Reale Werte: die echten Lizenz-Zählungen aus dem
Registry-Filter (`CC-BY-4.0` ×3, `CC-BY-SA-4.0` ×2, `CC-BY-NC-SA-4.0` ×1),
CIIC 81s echte `CITATION.cff`-Felder, die echte SPARQL-Query 3 samt 16
echten Ergebniszeilen (hier auf 4 Objekte × 2 Dateien verdichtet), sechs
reale Registry-Objekte mit ihren echten OSM-/Wikidata-/SquirrelBase-Links
samt der tatsächlich verwendeten RDF-Prädikate (`dct:spatial`,
`dct:subject`/`dct:type`) — bei SquirrelBase bewusst **nur** die reale
Item-ID ohne Prädikat-Behauptung, weil dieses Prädikat aus der TTL nicht
bestätigt werden konnte (kein Raten, A1-Geist).

**Anders als S8: komplett screenshot-frei.** Zwei frühe Fassungen (Folie
"F"/"H" der Ursprungskonversation) komponierten wie S8 einen SPARQL- bzw.
Registry-Screenshot; Flos Feedback ("da müssen wir uns insgesamt was
anderes überlegen… vielleicht doch eine eigene Grafik, die den Reviewern
gerecht wird" bzw. "lieber die abstrakte Grafik der Registry") ersetzte
beide durch reines SVG — die Query-Box ist hier handgezeichneter,
syntax-eingefärbter Code (`CODE_BG`/`CODE_TEXT`/`CODE_KEYWORD`, lokal in
diesem Modul, da nirgendwo sonst in der Familie gebraucht), die Registry
ist ein abstraktes DCAT-Zylinder-Icon statt eines Fotos der echten Seite.
Damit hat `img/source/` für S9 keinen Bedarf — nur S8 braucht es.

**Sechs statt vier Schritt-Icons: das Zweck-Badge ist hier lokal
nachgebaut, nicht importiert.** `step_purpose.py`s `_badge_markup()`
positioniert das Eckfähnchen oben *rechts* vom Icon-Kreis (Banner-Layout:
Icon zuerst, Fähnchen ragt in die Lücke zum nächsten Icon); S9 braucht es
oben *links* (Ecke der Folie). Die vier Icon-*Inhalte* (`_badge_icon_1..4`)
sind trotzdem wörtlich dieselben Pfade/Linien wie in `step_purpose.py`s
`_icon_document`/`_icon_triples`/`_icon_hub`/`_icon_network` — kopiert statt
importiert, weil `step_purpose.py`s Fassungen fest an `ICON_S = ICON_R/78`
gekoppelt sind (Modul-Konstante, nicht Parameter) und ein Import hier eine
zweite, abweichende `ICON_R` erzwungen hätte. Vermerkt als Nachtrag statt
stillschweigend belassen: eine spätere Aufräum-Runde könnte `ICON_S` als
Parameter statt Modulkonstante in `step_purpose.py` führen, dann ließe
sich auch dieser Rest echter Duplikation auflösen (siehe Teil D).

**Baum-Konnektoren rechtwinklig, nicht diagonal** (Zweck 2 und 4, Flo:
"die linien überkreuzen sich"/"lieber die edges senkrecht… sonst überdeckt
das alles"): jeweils ein senkrechter Stamm von der Wurzel zu einem
horizontalen Bus, dann senkrechte Stiche in jedes Kind. Bei Zweck 4s
zweistöckigem Katalogbaum liegt der Stamm zur zweiten Reihe exakt in der
realen horizontalen Lücke zwischen den Boxen der ersten Reihe (860–920px
im Entwurfsraster) statt durch eine Box hindurch.

**Kanten-Beschriftungen fett, am Linienwinkel ausgerichtet, mit weißem
Rahmen** (Zweck 3, Flo: "größer und… mit weißem Puffer drumherum und
fett"): lokale `_edge_label()`, ausnahmsweise nicht aus `visuals_utils`
importiert — die Version dort (`edge_label()`, aus S8 hervorgegangen) ist
seitengültig identisch, aber S9 war fertig gebaut, bevor der Wert dieser
Wiederverwendung klar war; als offener Aufräumpunkt vermerkt (Teil D).

**Abnahme:** ✅ erledigt — frischer Klon, `python main.py --only
talk-purpose --strict` läuft fehlerfrei, vollständiger `python main.py
--strict` (alle acht Schritte) ebenfalls fehlerfrei, keine zuvor
bestehende Grafik verändert. Zwei Läufe hintereinander bytegleich
(`md5sum` aller vier PNGs). Mit den in der Ursprungskonversation
ausgelieferten Referenzbildern verglichen (Sichtprüfung). Ein
Layout-Fehler dabei gefunden und gefixt, der im Referenzbild nicht
auffiel, weil dort andere Zeilenumbrüche zufällig genug Abstand ließen:
"Freshford: St Lachtain's Well"s zweizeiliger Name kollidierte mit der
"dcat:Dataset"-Bildunterschrift direkt darunter (nur 2px Abstand bei
ursprünglicher Boxhöhe 62) — Boxhöhe auf 70 angehoben, Zeilenabstand bei
mehrzeiligen Namen auf 21 statt 26 verkürzt. 3500×2000 pro Folie, weißer
Hintergrund, `PIL.Image.mode == "RGB"` geprüft.

### Nachtrag 2026-09-09 — Abnahme oben war zu früh: Abweichung von den freigegebenen Referenzbildern

Flo hatte die Referenzbilder (die dieser Chat portiert) schon vorher aus
einem separaten Sandkasten-Chat freigegeben ("top!"/"besser"/"passt", S8-
Eintrag). Ein lokaler Lauf gegen den echten Klon zeigte danach zwei
Abweichungen, die die obige Abnahme nicht abgedeckt hatte:

1. **S8, Step 1/2/4:** die Icon-Badge saß spürbar näher am Inhalt als in
   den freigegebenen Bildern. Ursache: `_render_balanced()` (beide Module)
   maß den tatsächlichen Inhalt und zentrierte ihn *symmetrisch* um die
   Badge — bei drei der vier Prozess-Folien war die freigegebene Position
   aber bewusst *nicht* symmetrisch (Step 1 explizit: "muss weiter runter…
   das ist zu sehr am Symbol"). Eine automatische Rand-Balance kann eine
   subjektive Korrektur dieser Art nicht treffen, sie rechnet ja gerade das
   Gegenteil aus. Fix: `_render_balanced()` durch `_render_fixed()`
   ersetzt, das die acht `(hshift, vshift)`-Werte aus den noch vorhandenen
   Sandkasten-Bau-Skripten übernimmt (nicht neu berechnet) — siehe
   `PATCH-README.md` des entsprechenden Korrektur-Patches für die exakten
   Zahlen. `visuals_utils.measure_content_margins()` bleibt als Werkzeug
   liegen (bislang ungenutzt seit diesem Nachtrag, analog zu
   `flatten_to_jpg()`, Teil D) für eine künftige Folie ohne bereits
   freigegebenes Referenzbild.
2. **S9, Zweck 2:** Die oben stehende Abnahme beschreibt einen "gefundenen
   und gefixten" Layout-Fehler (zweizeiliger Name kollidierte mit
   `dcat:Dataset`) — die Korrektur war aber selbst die Abweichung. Das
   freigegebene Referenzbild schneidet lange Namen auf eine Zeile ab
   (`"Freshford: St Lac..."`), zeigt sie nicht zweizeilig. Der zweizeilige
   Umbau wurde beim Portieren eingeführt, ohne dass Flo danach gefragt
   hatte, und erst dadurch entstand der eng wirkende Abstand zu
   `dcat:Dataset`, den Flo dann zu Recht bemängelte. Fix: zurückgebaut auf
   Ein-Zeilen-Kürzung, Boxhöhe zurück auf 62.

Nach dem Fix: `fdox-talk-purpose2-semantically-queryable.png` ist
bytegleich mit Flos freigegebenem Referenzbild; die anderen sieben Folien
weichen um unter 1 % der Pixel ab (Sub-Pixel-Kantenglättung an
Text/Kreisen, geprüft mit `PIL.ImageChops.difference` + Schwellwert 10/255
pro Kanal, keine Inhalts-/Layout-Differenz). Determinismus erneut geprüft
(zwei Läufe, `md5sum` identisch), volle Pipeline weiterhin fehlerfrei,
keine der sechs bestehenden Grafiken (S0–S7) verändert.

---

## S10 — Abschlussfolie ("All in All — Best Documentation Practice")

**Ziel:** `img/fdox-talk-closing-a-sphere.svg`/`.png` und
`img/fdox-talk-closing-b-hubs.svg`/`.png` — die letzte Folie des Vortrags
(Motto von Flo vorgegeben, nicht im Bild selbst gesetzt, siehe S8s
Titel-Konvention). Zwei Varianten zur Auswahl, beide alle acht Step-/
Zweck-Badges aus S2/S7 als Ring um S3s FDO-Kugel, abwechselnd
Step→Zweck→Step→Zweck (Nachbarn sind Ursache→Wirkung) statt als
4×4-Tabelle — Flo: "ist das nicht ein bisschen langweilig? es geht ja um
das Knowledge Graph Ecosystem" — die Folie selbst ist jetzt ein kleiner
Graph, keine Tabelle über einen.

**Uploads:** —, aus einer separaten Konversation übernommen, dort beide
Varianten nebeneinander gezeigt und freigegeben ("beide Bilder").

**Variante A:** Ring + Kugel, sonst nichts — schließt den Bogen zurück zu
Folie A (die erste FDO-Kugel im ganzen Vortrag).

**Variante B:** derselbe Ring (um 140px nach rechts verschoben, damit links
Platz frei bleibt), plus drei reale externe Hubs (Wikidata, OpenStreetMap,
NFDI4Objects) außerhalb des Rings, mit echten Ziel-Knoten verdrahtet:
OpenStreetMap → "Linking to Hubs", Wikidata → "Interoperable",
NFDI4Objects → "Integrable" — dieselben drei Systeme, die Folien C/D/G des
Vortrags bereits real verwendet haben (`dct:spatial`/`dct:subject`,
Registry-Harvest), hier als Aussage "das ist schon Teil der echten
LOD-Cloud" statt nur behauptet.

**Icon-Wiederverwendung:** Die vier Step-Glyphen sind `_node_icon()`,
direkt aus `step_pattern` importiert (`BADGE_R` ebenfalls, für den
korrekten Skalierungsfaktor — der erste Entwurf hatte hier eine falsche
Konstante und verzerrte die Icons deutlich zu groß, siehe unten). Die vier
Zweck-Glyphen sind, wie schon bei S9 dokumentiert, lokal nachgebaut statt
importiert (`step_purpose.py`s `ICON_S` ist eine Modul- keine
Funktionskonstante, siehe S9-Eintrag und Teil D) — derselbe offene
Aufräumpunkt, jetzt an drei Stellen (S9, S10) relevant statt an einer.
Die Kugel selbst liest `OUTER_R`/`INNER_R`/`ACCENT_STROKE`/`RING_FILL`
direkt aus `step_fdo_meta` und skaliert sie proportional herunter — kein
zweiter Satz Radien.

**Titel gekürzt, aus S2/S7s eigenen Daten abgeleitet, nicht neu erfunden:**
`_STEP_TITLE_OVERRIDE`/`_PURPOSE_TITLE_OVERRIDE` kürzen S2s zweizeilige
Titel bzw. S7s "Semantically Queryable" auf je eine kurze Zeile (Platzgrund:
~150px Bogenlänge pro Knoten statt einer ganzen Banner-Spalte) — derselbe
Wortlaut, nur kürzer, keine neuen Bezeichnungen.

**Abnahme:** ✅ erledigt — frischer Klon, `python main.py --only
talk-closing --strict` läuft fehlerfrei, danach vollständiger `python
main.py --strict` (alle neun Schritte) ebenfalls fehlerfrei, keine zuvor
bestehende Grafik verändert. Zwei Läufe hintereinander bytegleich
(`md5sum` beider PNGs). Beide Varianten mit den in der Ursprungskonversation
freigegebenen Referenzbildern verglichen (Sichtprüfung). Ein Skalierungs-
Fehler dabei gefunden und gefixt: die Step-Icons wurden zunächst mit
`scale(node_r/72)` statt `scale(node_r/BADGE_R)` gezeichnet — `_node_icon()`
ist für `BADGE_R=150` (S2s volle Badge-Größe) gezeichnet, nicht für den
72px-Ring-Radius dieser Folie; mit dem falschen Faktor kamen die Glyphen
über 2× zu groß aus dem Knoten heraus. 3500×2000 pro Folie, weißer
Hintergrund, `PIL.Image.mode == "RGB"` geprüft.

---

## S11 — `fdo-git-packager` (Konzept)

**Ziel:** Grafiken für den ArcheoFOSS-2026-Talk ("From Fragmented Objects
to Federated Knowledge"), die zeigen, wie ein GitHub-Repository zu einem
FDOx wird — das Gegenstück zu S8s Folie 1 (`fdo-3d-packager`). Der Talk
nennt einen "forthcoming Git-based packager".

**Stand des Repos (geprüft 2026-11-05).** `FDOx-squirrel/fdo-git-packager`
existiert bereits als **S1-Skelett** (Commit `c7dc35c`, 2026-09-03): fünf
Schritte `fetch`, `inspect`, `mdcff`, `bundle`, `build_fdo`, alle noch
Stubs ("nothing to do"). Festgelegt im dortigen PRIMER: `--ref` = Commit-SHA
Pflicht, Arbeitsbaum ohne `.git` flach in ein ZIP, `fdo-squirrel` als
Motor, Aufruf von `fdo-squirrel` noch offen. Die Grafiken folgen diesem
Entwurf. **CoMET-RS** steht nicht im Skelett; das Abstract sagt aber, der
Packager baue auf COMET-Extraktion auf — daher als *geplant* bei `inspect`
gezeichnet. Eine frühere Fassung dieses Schritts (Pin/Extract/Package/
Register mit "PROV-O from git log" und "SHACL check") wich vom Skelett ab
und ist ersetzt.

**Reales Beispiel (wie chublets-visuals S18).** SPARQLing Unicorn QGIS
Plugin, `sparqlunicorn/sparqlunicornGoesGIS`, gelesen 2026-11-05 am Tag
`v0.17.4` = `ba8af4cd0e3f95b862bd7562f0315b058124ab34` (2025-12-17).
Reihenfolge der Tags geprüft: v0.17.2 `736ec92` → v0.17.3 `4a5ab67` →
v0.17.4 `ba8af4c` → master `a519707` (2026-03-11, 7 Commits später).
Arbeitsbaum 690 Dateien (die Ausschlüsse des Packagers — `.git`,
`node_modules`, `build`, `dist`, `__pycache__`, `.venv` — greifen hier
nicht). Eigene `CITATION.cff`: Version **0.17.2** (hinkt dem Tag
hinterher), 15 DOI-Einträge, kein `license:`-Schlüssel. CoMET-RS-Review
(`examples/unicorn`, Tag `v0.4.3-chublets.2`): "version 0.17.2 differs
from release tag 0.17.4", "several DOIs, not linked to versions",
"person needs reconciliation". Keine erfundene MD.cff und keine
erfundene `fdo-metadata.ttl` im Bild.

**Vier Schritte, fünf Skelett-Schritte.** 1 Pin = `fetch`; 2 Inspect =
`inspect` (+ CoMET-RS, geplant); 3 Package = `mdcff` + `bundle`;
4 Build & Publish = `build_fdo`, danach (außerhalb des Repos) Zenodo-
Deposit → DOI, FDOx-Registry, N4O-KG.

**Dateien (alle neu).** Banner `fdox-git-packager-four-steps` (transparent,
A4); vier Badges `fdox-git-packager-step-{1-pin,2-inspect,3-package,
4-build}` (transparent, A4); vier Folien `fdox-talk-git-packager-step{1-fetch,
2-inspect,3-package,4-build}` (weiß, 7:4, S8); Swimlane
`fdox-talk-git-packager-actions` (weiß, 7:4; Lanes GitHub / GitHub Actions /
Zenodo / FDOx-Registry → N4O-KG, Tags 1–4 wie im Banner).

**Konzept sichtbar.** Gestrichelt = geplant (alles aus dem Skelett, Zenodo-
Deposit, Registry-Eintrag), durchgezogen = existiert (GitHub-Release,
Repo-`CITATION.cff`, Registry, N4O-KG). Jede Folie trägt die Legende "S1
skeleton, no step is implemented yet".

**Eine Farbe (S7-Präzedenz).** S2s vier Farben bedeuten andere Schritte;
daher durchgehend `FDO_ACCENT` (+ `_LIGHT`/`_SOFT`/Tint) aus
`visuals_utils.py`, kein neuer Hex-Code.

**Zenodo-Befund.** Die GitHub-Integration archiviert nur den
Quellcode-Zipball eines Releases, nicht Assets (`zenodo/zenodo#1235`,
offene Feature-Anfrage; Workaround: Upload per Zenodo-API aus GitHub
Actions). Beleg ist der Issue-Thread, keine offizielle Dokumentation —
vor "das ist so" im Vortrag gegenprüfen.

**Abnahme:** Entwurf — `python main.py --only git-packager --strict`
läuft, zwei Läufe bytegleich, `git status --short` zeigt nur die
erwarteten Pfade. **Offen:** Flos Sichtabnahme.

---

## S12 — Fertige 3D- und Software-FDOs im Federated-KG-Ökosystem

**Ziel:** drei 7:4-Folien (weiß, S8-Konvention, Badge links oben ohne
Nummer, weil es keine Schritte sind) für den ArcheoFOSS-2026-Talk:
was mit den *fertigen* FDOs passiert, wenn sie die Packager verlassen.
Dateien (alle neu): `fdox-talk-federation-path`, `-catalogue`,
`-shared-concepts` (je `.svg`/`.png`, 3500×2000, RGB).

**Echte Daten, gelesen 2026-11-05** (flache Klone):
`fdo-squirrel-registry` `253aee9` (Release 2026-09-03): 8 FDOs im Katalog
(6 × `3DDataFDO`, 2 × `SoftwareFDO`: *Ogham 3D EpiDoc Extractor*,
*Ogham Analysis*), 599 Dateien, 7.793 Tripel; ein neunter gepinnter
Datensatz ("Heinz Eau") hat keine `fdo-metadata.ttl` und fehlt im
Katalog. `crm_bridge.ttl`: `3DDataFDO ⊑ crmdig:D1_Digital_Object`,
`SoftwareFDO ⊑ crmdig:D14_Software`. `fdox-squirrel-n4o-collection`
`882a5f7` (2026-09-04): VoID zählt 5 × 3DDataFDO und 2 × SoftwareFDO
(älterer Bundle-Stand als die Registry).

**Folie 3 beruht auf der echten Registry-Abfrage** `shared-concepts`
(`queries.yaml`), mit rdflib auf `dist/fdo-registry.ttl` ausgeführt:
`wd:Q2016147` ist `dct:subject` von 4 FDOs (Extractor, Analysis, GEARS/1,
CO074-148---- = CIIC 81), `wd:Q22731` von 6 (im Bundle als "Stone"
beschriftet). CHUIS/1 trägt "Ogham Stone" nur als Freitext und fehlt bei
Q2016147; Beuys-Stele und Freshford teilen kein Konzept. OSM-Relation
62273 ist `dct:spatial` beider Software-FDOs. Die Folie zeigt das ehrlich
als Befund, nicht als Erfolgsmeldung.

**Durchgezogen = in den Repos geprüft, gestrichelt = offen oder geplant:**
N4O-Onboarding durch VZG (README-Stand 2026-09-04; echte Collection-URI
noch Platzhalter) und `jupyter-nb-lod` (zweites Software-Repo aus dem
Abstract, noch nicht in der Registry; soll über `fdo-git-packager` laufen).

**Abnahme:** Entwurf; `python main.py --only federation --strict` läuft,
zwei Läufe bytegleich. **Offen:** Flos Sichtabnahme.

---

## S13 — Echte Graphbilder: Ogham-Objekte, 3D-FDOs und Software

**Ziel:** drei 7:4-Folien (weiß, S8) mit *echten Triples* der Registry als
Knoten-Kanten-Graph statt Konzeptkästen: `fdox-talk-ogham-graph-cluster`
(3 × 3DDataFDO + 2 × SoftwareFDO um `wd:Q2016147`), `-object` (CIIC 81 und
`o3d-epidoc-extractor`, je ein Hop) und `-registry` (alle acht FDOs als
ein Graph). Quelle: `dist/fdo-registry.ttl` von `fdo-squirrel-registry`
`253aee9` (7.793 Tripel), mit rdflib gelesen am 2026-11-05; Knoten und
Kanten stehen im Docstring von `py/step_ogham_graph.py` einzeln belegt.

**Befunde, die die Folien zeigen (nicht beschönigen):**
- `wd:Q2016147` ("Inscribed Ogham stone" im Bundle) ist `dct:subject`/
  `dct:type` von Extractor, Ogham Analysis, GEARS/1 und CIIC 81; CHUIS/1
  führt "Ogham Stone" nur als Freitext.
- **Es gibt kein Triple "Software X nutzt 3D-FDO Y".** Software und Objekte
  treffen sich über Konzept, `fdo:context` und Publisher. Folie 2 zeichnet
  die explizite Kante gestrichelt als Vorschlag (z. B. `prov:used`), mit dem
  Hinweis "not modelled yet".
- Florian Thiery erscheint als ORCID-Knoten (Extractor, GEARS/1) **und** als
  Registry-Agent `8e916ce55425de21` (CHUIS/1, CIIC 81, Antholzer See,
  Beuys-Stele); die Registry führt nicht nach Namen zusammen (Quality-Report).
- Freshford teilt kein Konzept, keinen Ort und keine Person mit anderen FDOs.

**Grenze:** Wikidata war aus der Sandbox nicht erreichbar. Gezeigt werden nur
die Labels, die das Bundle selbst trägt ("Inscribed Ogham stone", "Cork
Public Museum", "EpiDoc", "Linked Open Data"); `wd:Q121592049` bleibt ohne
Label, nichts wurde ergänzt. `wd:Q22731` ("Stone", 6 FDOs) ist auf Folie 3
aus Gründen der Lesbarkeit weggelassen und in der Fußzeile genannt.

**Abnahme:** Entwurf; `python main.py --only ogham-graph --strict` läuft.
**Offen:** Flos Sichtabnahme; Entscheidung, ob eine explizite Kante
Software→Objekt in `fdo-squirrel` modelliert werden soll.

## S14 — Themenordner und GitHub-Pages-Seite

**Ziel:** die Grafiken nach Thema in `img/<kategorie>/` sortieren und als
Seite veröffentlichen (Wunsch von Flo, 2026-11-05; Antworten: 8 Ordner nach
Thema, FDOx-Blau, S11–S13 öffentlich mit Entwurf-Hinweis).

**Umbau.** `visuals_utils.py` führt `CATEGORIES` (Slug, Titel, Beschreibung,
Dateinamen-Präfixe), `category_of(stem)` und `img_path(filename)`; alle
Steps schreiben über `img_path(...)`. `_FONT_REL_PREFIX` ist jetzt
`../../fonts`. Geprüft: Neubau liefert PNGs byte-gleich zum Altstand
(Sandbox-Vergleich), SVGs unterscheiden sich nur im Font-Pfad.

**Seite.** `py/site_kit.py` (Stylesheet, Navigation, Seitenrahmen, Schrift
nach `docs/assets/`), `py/site_meta.py` (Bildunterschriften, Quellenzeilen,
Entwurf-Status, Kurznamen), `py/step_site.py` (läuft als letzter Schritt
`site`). Erzeugt `docs/index.html`, `docs/visuals/<kategorie>.html` und
kopiert PNG/SVG nach `docs/visuals/img/` (SVG mit Font-Pfad auf
`docs/assets/fonts`). Ein Bild ohne Bildunterschrift oder umgekehrt bricht
den Schritt ab.

**Regeln.** Neue Grafik = Präfix in `CATEGORIES` (falls neu) + Eintrag in
`CAPTIONS`. Die Seiten-Tokens (Grau, Karten) stehen in `site_kit.py`, nur
die Markenfarben kommen aus `visuals_utils.py`. `docs/` ist erzeugt und
wird committet, nicht von Hand bearbeitet.

**Abnahme:** Entwurf; Seiten in Desktop- und Handybreite gerendert und
angesehen. **Offen:** Flos Sichtabnahme; Pages einschalten (Settings →
Pages → Branch `main`, Ordner `/docs`).

## S15 — Story-Folien: vom FKGE zu FDOx, für 3D und Software

**Ziel:** die Geschichte der alten 3D-Präsentation ("From Smartphone 3D to
Federated Knowledge Graphs") mit der Software-Geschichte des ArcheoFOSS-
Talks verbinden. Neue Kategorie `story` (Präfix `fdox-talk-story-`), Schritt
`story` in `main.py`, Modul `py/step_story.py`. Antworten von Flo: CIIC 81
ist der rote Faden; Squilly nur gezeichnet (kein Bild eingebettet);
FKGE-Karte als vereinfachter Neubau.

**Folien (alle 7:4, weiß, S8-Konvention).**
- `fdox-talk-story-fkge-map`: FDO-driven links, LOD-driven rechts,
  Federated Knowledge Graph in der Mitte, die vier FDOx-Schritte als Brücke.
  Begriffe aus Flos FKGE-Diagramm (Thiery & Noback, CC BY 4.0), vereinfacht.
- `fdox-talk-story-two-roads-unicorn` und `-extractor`: zwei Spuren in dieselbe
  `fdo-squirrel`-Maschine. 3D-Spur: CIIC 81 (DOI 10.5281/zenodo.18724635, 50
  Dateien, CC-BY-NC-SA-4.0). Software-Spur A: SPARQLing Unicorn (v0.17.4,
  ba8af4c), alles gestrichelt (fdo-git-packager ist S1-Skelett). Software-Spur
  B: Ogham 3D EpiDoc Extractor (DOI 10.5281/zenodo.18369125, 254 Dateien, MIT),
  Ergebnis durchgezogen, Packager gestrichelt.
- `fdox-talk-story-squilly-graph`: gezeichneter Nuss-Faden-Graph neben dem
  Registry-Graphen (Fakten wie S13).
- `fdox-talk-step1-fdo-encapsulation-ciic81` (Kategorie `talk-process`):
  Schritt 1 mit CIIC 81 statt Freshford (50 Dateien laut Registry);
  Screenshot aus Flos Folie 12 nach `img/source/talk-sketchfab-ciic81.png`.
  Die Freshford-Fassung bleibt unverändert.

**Grenzen.** Wie der Extractor tatsächlich verpackt wurde, steht in keinem
gelesenen Repo; die Folie sagt das offen. Die Sketchfab-Quellenzeile
("by b-unicycling") folgt Flos Folie 12; Folie 24 nennt A.-K. Distel für das
Vorschaubild, vor Veröffentlichung klären.

**Abnahme:** Entwurf; Folien angesehen, Seite gerendert. **Offen:** Flos
Sichtabnahme; Entscheidung, ob eine Paradata-Kette (Foto → Modell → Software →
Analyse mit `prov:used`) modelliert wird (siehe S13).

## S16 — RO-Crate und Signposting in den Grafiken

**Ziel:** die Grafiken zeigen RO-Crate und die Landing Page als Teil dessen,
was `fdo-squirrel` ab v1.1.0 standardmäßig ausgibt. Antworten von Flo: das
Architekturdiagramm erweitern, eine neue Grafik "ein Bundle, drei Sichten"
bauen, das offizielle Logo einbinden; wo RO-Crate Standardausgabe ist, bestehende
Grafiken ergänzen, sonst neu.

**Substanz.**
- `py/step_architecture.py`: neue Prozesszeile `ROW_CRATE` ("Signposting &
  RO-Crate", zwischen Overview und Bundle, wie in `fdo-squirrel`s `main.py`),
  neue Ausgabebox (`ro-crate-metadata.json`, `fdo-landing-page.html`); "Mermaid →
  JPG" korrigiert auf PNG. `OUTPUT_BOXES` hat jetzt fünf Einträge, die Kanten
  verwenden deren Index.
- `py/step_bundle_views.py` (Schritt `bundle-views`, Kategorie `schemas`):
  `fdox-bundle-three-views.svg/.png`. Ein hohes Bundle-Kästchen, drei Karten (RDF:
  `fdo-metadata.ttl`; RO-Crate: `ro-crate-metadata.json`; Signposting:
  `fdo-landing-page.html`). Farben aus `STEPS`/`FDO_ACCENT`, kein eigenes Hex.
- `py/visuals_utils.py`: Tabelle `LOGOS` (Schlüssel `rdf`, `ro-crate`; Dateistamm und
  Nennungstext), `logo(key, ...)` bettet `img/source/<stem>.svg` (sonst `.png`) als
  `data:`-URI ein, `logo_path(key)` sagt, ob eines da ist, `logo_credits()` liefert die
  Nennungszeile der vorhandenen Logos; `ro_crate_logo*()` bleiben als Kurzformen;
  `CATEGORIES` um das neue Präfix.
- `img/source/ro-crate-logo.png`, `img/source/rdf-logo.svg`, `img/source/NOTICE.md`: die
  Logos und ihr Hinweis (Autor, Lizenz, Änderung).
- `py/site_meta.py`: Bildunterschriften für beide Grafiken; Architektur-
  unterschrift nennt `fdo-squirrel` v1.2.0.

**Abnahme:** `python main.py --only architecture`, `--only bundle-views` und
`--only site` laufen; zwei Läufe liefern identische Dateien; die Seite zeigt
beide Grafiken in der Kategorie "Schemas, architecture and meta graphic". Ohne
Logo-Datei steht ein Textpill, mit Logo-Datei das Logo samt Nennung unter dem
rechten Panel.

### Entwurf 2026-11-16

Wie oben, in der Sandbox gerendert und angesehen, jetzt mit dem echten RO-Crate-Logo
und dem RDF-Logo (Flo hat beide Dateien geliefert; RDF: Bill Schwappacher / W3C,
CC BY 4.0, laut Flo, unverändert als SVG). **Offen:** Flos Sichtabnahme.


---

## S17 — Bilder-Pool: Seitenstruktur, Kreuzungen, RO-Crate in Schritt 1

**Ziel:** das Repository dient als Bilder-Pool für Präsentationen und Papers. Flos
Auftrag: weniger "Draft", "Talk:" in den Seitentiteln ersetzen, umsortieren,
RO-Crate in die Prozessfolien (Schritt 1 ist der Packager), Linienüberschneidungen
in den Grafiken prüfen.

**Umfang:**
- `py/visuals_utils.py` (`CATEGORIES` mit `group`, neue Titel), `py/site_meta.py`
  (`CONCEPT_*` statt `DRAFT_*`, Bildunterschriften "Slide, ..." statt "Talk slide, ..."),
  `py/site_kit.py` (Navigation nach Gruppen), `py/step_site.py` (Startseite nach Gruppen,
  Hinweis "How to use them").
- `py/step_talk_purpose.py` (purpose3), `py/step_federation.py` (shared-concepts),
  `py/step_ogham_graph.py` (Registry-Graph), `py/step_talk_process.py` (Schritt 1).

**Abnahme:** `--only talk-purpose`, `talk-process`, `federation`, `ogham-graph`,
`site` laufen; die vier Grafiken zeigen keine Kreuzungen mehr (purpose3: eine);
Navigation zeigt Gruppen; nur `git-packager` und `two-roads-unicorn` tragen "Concept".

### Entwurf 2026-11-16

Gerendert und angesehen. **Offen:** Flos Sichtabnahme; ob "Concept" für genau
diese Grafiken stimmt; die Squilly-Grafik (CIIC 81 und Thiery laufen auf einen
Punkt zu, kreuzen sich aber nicht) blieb unverändert.

---

## S18 — Lebendige Galerie: neutrale Namen, Piktogramme eigene Seiten

**Ziel:** das Repository ist eine lebendige Galerie, aus der man sich für Vorträge,
Papers und Software-Dokumentation bedient; Namen und Kategorien beschreiben den Inhalt,
nicht den Verwendungszweck. Flos Auftrag: "talk" aus Namen, Ordnern und Seiten entfernen
(nirgends aktiv eingebunden, also frei umbenennbar), "How to use" von der Startseite
entfernen, die Piktogramme je in eine eigene Unterseite.

**Umfang:**
- Umbenennung nach der Tabelle unten (Dateien, Ordner, Kategorien, Seiten, Skripte,
  Schritt-Schlüssel); Quell-Screenshots `img/source/talk-*` heißen jetzt ohne Präfix.
- Neue Kategorien `pictograms` (acht Piktogramme der Schritte und Outcomes) und
  `git-packager-pictograms` (vier Piktogramme); `pattern` enthält nur noch die zwei Banner,
  `git-packager` die Walkthrough-Grafiken und den Swimlane.
- `category_of()` nimmt das längste passende Präfix (vorher das erste).
- Startseite ohne Nutzungshinweis; Navigation und Startseite haben dieselbe Reihenfolge
  (Gruppen und Kategorien aus `CATEGORIES`); `step_site` löscht nicht mehr gebaute
  Seiten in `docs/visuals/`.
- `migrate_names.py` (einmalig, nicht ins Repository): verschiebt per `git mv`, damit die
  Historie mitgeht und kein PNG neu gerendert werden muss.

**Abnahme:** nach `python migrate_names.py && python main.py --only site` zeigen alle
Seiten dieselbe Navigation, das Menü der Unterseiten stimmt mit der Startseite überein, und
`git status` zeigt nur Umbenennungen (Dateiinhalt unverändert) plus die geänderten Seiten.

### Entwurf 2026-11-16

Auf der Sandbox-Kopie ausgeführt: die SVGs aller umbenannten Grafiken sind nach dem
Verschieben bytegleich zu einem Neuaufbau (Ausnahme: zwei Story-SVGs unterscheiden sich nur
in Gleitkommastellen, `422.27` statt `422.27000000000004`). **Offen:** Flos Sichtabnahme.

**Umbenennungen** (ältere Abschnitte dieses Dokuments nennen noch die alten Namen; die Tabelle übersetzt):

| alt | neu |
|---|---|
| `img/talk-closing/fdox-talk-closing-a-sphere` | `img/sphere/fdox-sphere-badges` |
| `img/talk-closing/fdox-talk-closing-b-hubs` | `img/sphere/fdox-sphere-hubs` |
| `img/talk-process/fdox-talk-step1-fdo-encapsulation` | `img/steps/fdox-steps-1-fdo-encapsulation` |
| `img/talk-process/fdox-talk-step1-fdo-encapsulation-ciic81` | `img/steps/fdox-steps-1-fdo-encapsulation-ciic81` |
| `img/talk-process/fdox-talk-step2-semantic-metadata` | `img/steps/fdox-steps-2-semantic-metadata` |
| `img/talk-process/fdox-talk-step3-linking-hubs` | `img/steps/fdox-steps-3-linking-hubs` |
| `img/talk-process/fdox-talk-step4-federated-kg` | `img/steps/fdox-steps-4-federated-kg` |
| `img/talk-purpose/fdox-talk-purpose1-fair-citable` | `img/outcomes/fdox-outcomes-1-fair-citable` |
| `img/talk-purpose/fdox-talk-purpose2-semantically-queryable` | `img/outcomes/fdox-outcomes-2-semantically-queryable` |
| `img/talk-purpose/fdox-talk-purpose3-interoperable` | `img/outcomes/fdox-outcomes-3-interoperable` |
| `img/talk-purpose/fdox-talk-purpose4-integrable` | `img/outcomes/fdox-outcomes-4-integrable` |
| `img/story/fdox-talk-story-fkge-map` | `img/story/fdox-story-fkge-map` |
| `img/story/fdox-talk-story-two-roads-unicorn` | `img/story/fdox-story-two-roads-unicorn` |
| `img/story/fdox-talk-story-two-roads-extractor` | `img/story/fdox-story-two-roads-extractor` |
| `img/story/fdox-talk-story-squilly-graph` | `img/story/fdox-story-squilly-graph` |
| `img/git-packager/fdox-talk-git-packager-step1-fetch` | `img/git-packager/fdox-git-packager-1-fetch` |
| `img/git-packager/fdox-talk-git-packager-step2-inspect` | `img/git-packager/fdox-git-packager-2-inspect` |
| `img/git-packager/fdox-talk-git-packager-step3-package` | `img/git-packager/fdox-git-packager-3-package` |
| `img/git-packager/fdox-talk-git-packager-step4-build` | `img/git-packager/fdox-git-packager-4-build` |
| `img/git-packager/fdox-talk-git-packager-actions` | `img/git-packager/fdox-git-packager-actions` |
| `img/federation/fdox-talk-federation-path` | `img/federation/fdox-federation-path` |
| `img/federation/fdox-talk-federation-catalogue` | `img/federation/fdox-federation-catalogue` |
| `img/federation/fdox-talk-federation-shared-concepts` | `img/federation/fdox-federation-shared-concepts` |
| `img/ogham-graph/fdox-talk-ogham-graph-cluster` | `img/ogham-graph/fdox-ogham-graph-cluster` |
| `img/ogham-graph/fdox-talk-ogham-graph-object` | `img/ogham-graph/fdox-ogham-graph-object` |
| `img/ogham-graph/fdox-talk-ogham-graph-registry` | `img/ogham-graph/fdox-ogham-graph-registry` |
| `img/pattern/fdox-step-1-fdo-encapsulation` | `img/pictograms/fdox-step-1-fdo-encapsulation` |
| `img/pattern/fdox-step-2-semantic-paradata-modelling` | `img/pictograms/fdox-step-2-semantic-paradata-modelling` |
| `img/pattern/fdox-step-3-linking-community-hubs` | `img/pictograms/fdox-step-3-linking-community-hubs` |
| `img/pattern/fdox-step-4-federated-kg-integration` | `img/pictograms/fdox-step-4-federated-kg-integration` |
| `img/pattern/fdox-purpose-1-fair-citable` | `img/pictograms/fdox-purpose-1-fair-citable` |
| `img/pattern/fdox-purpose-2-semantically-queryable` | `img/pictograms/fdox-purpose-2-semantically-queryable` |
| `img/pattern/fdox-purpose-3-interoperable` | `img/pictograms/fdox-purpose-3-interoperable` |
| `img/pattern/fdox-purpose-4-integrable` | `img/pictograms/fdox-purpose-4-integrable` |
| `img/git-packager/fdox-git-packager-step-1-pin` | `img/git-packager-pictograms/fdox-git-packager-step-1-pin` |
| `img/git-packager/fdox-git-packager-step-2-inspect` | `img/git-packager-pictograms/fdox-git-packager-step-2-inspect` |
| `img/git-packager/fdox-git-packager-step-3-package` | `img/git-packager-pictograms/fdox-git-packager-step-3-package` |
| `img/git-packager/fdox-git-packager-step-4-build` | `img/git-packager-pictograms/fdox-git-packager-step-4-build` |
| `img/source/talk-sketchfab-freshford.png` | `img/source/sketchfab-freshford.png` |
| `img/source/talk-sketchfab-ciic81.png` | `img/source/sketchfab-ciic81.png` |
| `img/source/talk-registry-screenshot.png` | `img/source/registry-screenshot.png` |
| `img/source/talk-ciic81-preview.png` | `img/source/ciic81-preview.png` |
| `py/step_talk_process.py`, Schritt `talk-process` | `py/step_steps.py`, Schritt `steps` |
| `py/step_talk_purpose.py`, Schritt `talk-purpose` | `py/step_outcomes.py`, Schritt `outcomes` |
| `py/step_talk_closing.py`, Schritt `talk-closing` | `py/step_sphere.py`, Schritt `sphere` |
| `docs/visuals/talk-process.html`, `talk-purpose.html`, `talk-closing.html` | `steps.html`, `outcomes.html`, `sphere.html` |
---

# Teil D — Offene Punkte

- **S11: Annahmen ohne Bestätigung.** (a) Slug `sparqlunicornGoesGIS-ba8af4c`
  ist meine Illustration der Ableitung, nicht aus dem Skelett-Code geprüft;
  (b) CoMET-RS in `inspect` ist geplant, steht nicht im Skelett; (c) wie
  `build_fdo` `fdo-squirrel` aufruft, ist im Repo selbst offen; (d)
  Zenodo-Deposit per API und "registry entry — DOI + bundle link" sind
  Konzept, nicht geprüft; (e) die Repo-README von `fdo-git-packager` nennt
  schon "S1 skeleton" — Grafiken und README stimmen damit überein.
- **S12: Registry-Stand und N4O-Stand weichen ab.** Die Folien nennen
  Registry 2026-09-03 (8 FDOs) und N4O-Bundle 2026-09-04 (7 FDOs); vor dem
  Vortrag Zahlen und den VZG-Onboarding-Status neu prüfen.
- **S12: CHUIS/1 und `Q22731`.** Die Abfrage zeigt, dass CHUIS/1 "Ogham
  Stone" nur als Text führt und `Q22731` im Bundle "Stone" heißt — Befunde
  für die Pakete, nicht für die Grafik; Korrektur nur über neue Zenodo-Version.
- **S14: Seitenumfang.** `docs/` verdoppelt die Bildgröße im Repo (rund
  12 MB zusätzlich). Wird das zu viel, PNGs der Seite verkleinern oder nur
  die Folien als PNG, Rest als SVG ausliefern.
- **S14: Bildunterschriften** der S1–S10-Grafiken sind aus Dateinamen und
  Folientiteln abgeleitet; vor dem Veröffentlichen gegenlesen.

- **CI (`--strict` bei jedem Push)** noch nicht eingerichtet — analog zu
  `fdo-architecture`s offenem Punkt, hier aber noch nicht mal vorgeschlagen.
- **Reduzierte Fassung des `fdo-architecture`-Familiendiagramms für Folie 8
  des Talk-Konzepts** — anderes Vorhaben als S4 (das hier ist
  `fdo-squirrel`s interne Pipeline, Folie 8 braucht die Repo-Familie
  `fdo-squirrel → fdo-squirrel-registry → fdox-squirrel-n4o-collection`)
  — weiterhin offen, noch kein Schritt.
- **`flatten_to_jpg()` ungenutzt seit S2/S3-Nachtrag 2026-09-08** — bleibt
  als Werkzeug liegen statt entfernt zu werden; wird real erst, wenn ein
  künftiger Schritt tatsächlich ein flaches JPG braucht (z. B. für ein
  Zielsystem ohne Alphakanal-Unterstützung).
- **`fdo-squirrel/architecture.mermaid` selbst bleibt veraltet** — S4 hat
  nur eine korrigierte Kopie in `fdox-visuals` erzeugt, nicht die
  Originaldatei in `fdo-squirrel` gepatcht. Das wäre ein eigener Chat in
  jenem Repo (anderes Repo pro Chat, A3).
- **Große Idee, ursprünglich hier vermerkt, inzwischen anderswo passiert
  und von S8/S9 konsumiert, nicht produziert:** CIIC 81 und eine Holy Well
  (`freshford-st-lachtains-well-low-poly`) echt durch `fdo-3d-packager` →
  `fdo-squirrel` schicken. Das ist zwischenzeitlich in separaten Chats in
  jenen beiden Repos tatsächlich passiert (CIIC 81s echte DOI
  `10.5281/zenodo.18724635`, echte Registry-Aufnahme); S8/S9 lesen die
  Ergebnisse davon (Screenshots, TTL-Werte), erzeugen sie aber nicht
  selbst — die *Instanz*-Diagramme selbst ("MD.cff ausgefüllt", "Files and
  Roles", "FDO Overview", Flos Folien 27–29) haben weiterhin keinen
  Generator hier oder in `fdo-squirrel`, das bleibt offen, nur nicht mehr
  "noch nicht mal skizziert".
- **RDF-Triple-Visualisierungen (Flos Folien 30/31) weiterhin nicht
  vorgesehen — S9 Zweck 2 ist kein Gegenbeispiel.** S9s SPARQL-Ergebnis-
  Baum zeigt die vier/acht Knoten *einer konkreten, live gestellten*
  Query, nicht Tripel aus dem Graphen allgemein; kein RDF-Browser, kein
  Ersatz für Folie 30/31s eigentliches Thema. Hier nur vermerkt, damit die
  Abgrenzung beim nächsten Chat nicht neu hergeleitet werden muss.
- **`step_purpose.py`s `ICON_S = ICON_R/78` ist eine Modulkonstante, kein
  Parameter** — S9 musste deshalb die vier Zweck-Icon-Zeichenfunktionen
  kopieren statt zu importieren (siehe S9-Eintrag). Cleanup, kein Bug: hier
  vermerkt, damit ein künftiger `step_purpose.py`-Umbau (`ICON_S` als
  Funktionsparameter statt Modulkonstante) das erledigen kann und S9 dann
  auf den Import umgestellt werden kann.
- **S9s `_edge_label()` dupliziert `visuals_utils.edge_label()` seitengleich**
  — S8 hat die Version in `visuals_utils.py` verallgemeinert, S9 war zu dem
  Zeitpunkt schon fertig und wurde nicht mehr nachgezogen. Nächster Anlass
  zum Anfassen von `step_talk_purpose.py`: `_edge_label()` entfernen, Import
  aus `visuals_utils` stattdessen.
- **S16: Logo-Lizenz.** Beide Logos sind laut Flo CC BY 4.0 (RO-Crate Community; RDF: Bill Schwappacher / W3C). Beim RDF-Logo ist `W3C` im Namen: die W3C-Logo-Regeln (nicht verändern, keine Billigung andeuten) werden eingehalten, aber die Lizenzangabe ist nicht aus einer Quelle belegt. **Von Flo am 2026-11-16 geprüft: die Lizenzangaben stimmen.**
  Die Lizenz steht nicht in der Datei selbst; Flo prüft sie bei Gelegenheit
  auf der RO-Crate-Seite gegen und korrigiert `img/source/NOTICE.md`, falls sie
  abweicht. Die Spezifikation steht unter Apache 2.0, das sagt nichts über das
  Logo.
- **S16: Volllauf ändert viele PNGs.** Ein `python main.py` ohne `--only` mit
  einer anderen `resvg-py`-Version als der, mit der die committeten PNGs
  entstanden, schreibt fast alle PNGs neu (in der Sandbox mit `resvg-py` 0.5.0
  rund 90 Dateien). Für diesen Patch deshalb nur `--only architecture`,
  `--only bundle-views`, `--only site`.
- **S16: `fdo-squirrel/architecture.mermaid`** bleibt, wie schon nach S4,
  unverändert (anderes Repo pro Chat, A3).

## S19 — Graph-Bilder wie die Schemas, Piktogramme für den 3D-Packager

**Ziel:** die zehn Graph-Bilder (`ogham-graph` ×3, `federation` ×3, `story` ×4) sehen aus wie die
übrigen Schemas: ohne Header (Icon, Titel, Untertitel), ohne Quellenzeile, ohne weißen
7:4-Hintergrund, transparent und eng beschnitten (höchstens 10 px Rand). Flos Vorgabe: im Bild
bleibt nur eine Legende, wenn sie sinnvoll ist; alle Notizen und Erklärungen gehören in die
Bildunterschrift der Seite. Außerdem bekommt der 3D-Packager wie der Git-Packager Piktogramme.

**Umfang:**
- `visuals_utils.write_tight_graphic()`: rendert einmal, liest die Alpha-Hülle und schreibt SVG
  (`viewBox`) und PNG auf denselben Inhaltsrahmen zu; die drei Schritte nutzen sie.
- Notizboxen und Fußzeilen aus den Bildern entfernt (z. B. "What differs, what does not",
  "What this shows"); ihr Wortlaut steht jetzt in `site_meta.CAPTIONS` (Bildunterschrift bzw.
  Quellenzeile). Die Legende (Knotenarten, Linienstile, durchgezogen/gestrichelt) bleibt.
- Neue Kategorie `3d-packager-pictograms` (Gruppe "3D models", Kürzel DP) mit sechs Piktogrammen
  `fdox-3d-packager-step-{1-fetch,2-convert,3-nexus,4-mdcff,5-bundle,6-build-fdo}`; durchgezogener
  Kreis (das Werkzeug existiert), Git-Packager bleibt gestrichelt (Skelett). Schritt `3d-packager`.

**Bewusste Entscheidung:** der Katalog (`federation-catalogue`) behält die Klassenbox
(`fdo:3DDataFDO` / `fdo:SoftwareFDO` mit CRMdig-Oberklasse) und die Summenzeile, weil sie Teil der
Tabelle sind; nur die erklärende Box wanderte in die Bildunterschrift.

**Abnahme:** `python main.py --only federation && ... ogham-graph && ... story && ... 3d-packager && ... site`;
die zehn Bilder zeigen keinen Titel und keine Quellenzeile, PNG-Hintergrund ist transparent.

## S20 — 3D-Packager-Piktogramme in den Grafiken

**Ziel:** die sechs Piktogramme (S19) sind Bausteine des Pools und kommen dort vor, wo die
sechs Schritte des fdo-3d-packager gezeigt werden, statt als Textboxen.

**Umfang:**
- `step_3d_packager_pictograms.badge_group(idx, cx, cy, scale)`: ein Badge als SVG-Gruppe;
  die Piktogramm-Dateien nutzen dieselbe Funktion.
- Step 1 (`fdox-steps-1-fdo-encapsulation`, `…-ciic81`): sechs Badges mit Schrittname und
  Kurzbeschreibung statt sechs Boxen.
- "Two roads" (`fdox-story-two-roads-unicorn`, `…-extractor`): die Packager-Box des 3D-Zweigs
  zeigt die sechs Badges in einer Reihe.
- Quellenzeilen der Piktogramm-Seite ohne Versionsangabe.

**Version des fdo-3d-packager:** Step 1 sagte v1.1.0, die Story-Bilder v1.0.0; seit S21 nennt keine Grafik mehr eine Version. **Abnahme:** `python main.py --only steps && ...
--only story && ... --only 3d-packager`, danach `git checkout` der unveränderten PNGs
(`fdox-steps-3-linking-hubs.png`, `fdox-steps-4-federated-kg.png`), dann `--only site`.

## S21 — Keine Versionsangabe des fdo-3d-packager in den Grafiken

Flo: die Version soll überall raus. Entfernt: die Zeile "fdo-3d-packager v1.1.0" in Step 1
(`fdox-steps-1-fdo-encapsulation` und `…-ciic81`); in den Story-Bildern und Captions stand sie
seit S20 nicht mehr; in Docstrings ohne Version. **Abnahme:** `python main.py --only steps`,
danach `git checkout` der unveränderten PNGs (Steps 2 bis 4), dann `--only site`.

## S22 — Urheberzeile der Doku

Flo: in der Doku (GitHub Pages) soll überall "Florian Thiery, Research Squirrel Engineers
Network / LEIZA" stehen statt "Florian Thiery, LEIZA". Geändert: `site_meta.CREDIT_BASE`, die
einzige Stelle, die die Zeile unter jeder Grafik erzeugt. **Abnahme:** `python main.py --only site`;
jede Karte endet auf "(Florian Thiery, Research Squirrel Engineers Network / LEIZA). Code: MIT licence."

## S23 — Affiliation in CITATION.cff

Flo: wie die Urheberzeile der Doku (S22). `CITATION.cff` nennt jetzt "Research Squirrel Engineers
Network / Leibniz-Zentrum für Archäologie (LEIZA)" als Affiliation (CFF kennt dafür ein einzelnes
Textfeld). **Abnahme:** die Datei ist gültiges CFF 1.2.0 (z. B. `cffconvert --validate`, falls
installiert); GitHub zeigt unter "Cite this repository" die neue Affiliation.
