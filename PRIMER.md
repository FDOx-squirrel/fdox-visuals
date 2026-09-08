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
| Transparenter Rand | **maximal 10px** um jede Grafik, für alle sechs PNGs einheitlich — per `trim_transparent_border()` auf Pixelebene zugeschnitten (Alphakanal-Bounding-Box + fester Rand), nicht per geschätztem Design-Koordinaten-Abstand. Grund für den Pixel-Ansatz statt Geometrie-Rechnung: Schritt 4s Titeltext reicht nachweislich über den Icon-Kreis hinaus (siehe A1, neuer Befund) — eine Design-Koordinaten-Schätzung hätte das riskiert abzuschneiden | 2026-09-08 |

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

---

# Teil D — Offene Punkte

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
- **Große Idee, noch nicht mal skizziert, geschweige denn Schritt:**
  CIIC 81 (und eine Holy Well, z. B. `freshford-st-lachtains-well-low-poly`)
  echt durch `fdo-3d-packager` → `fdo-squirrel` schicken, und die
  *Instanz*-Diagramme (Flos Folien 27–29: "MD.cff ausgefüllt",
  "Files and Roles", "FDO Overview") direkt aus diesem echten Lauf
  erzeugen statt wie S2–S6 als generische Schema-/Architektur-Grafiken.
  Gehört, wenn umgesetzt, eher zu `fdo-squirrel`/`fdo-3d-packager` als zu
  `fdox-visuals` — S6 (`Overview diagram`) tut das für die "FDO Overview"-
  Variante bereits (`fdo_mermaid.py` + `render_mermaid_to_jpg`). "Files and
  Roles" und "MD.cff ausgefüllt" haben noch keinen Generator. Separat
  diskutiert, hier nur vermerkt, damit es nicht verloren geht.
- **RDF-Triple-Visualisierungen (Flos Folien 30/31)** — ausdrücklich nicht
  für `fdox-visuals` vorgesehen (Flos eigene Einschätzung), separates
  Thema.
