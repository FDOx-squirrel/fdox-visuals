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

S2 und S3 sind unabhängig voneinander (beide hängen nur von S1 ab) und
können in beliebiger Reihenfolge laufen — `main.py --only fdo-meta` läuft
ohne dass `pattern` vorher gelaufen sein muss.

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

# Teil D — Offene Punkte

- **CI (`--strict` bei jedem Push)** noch nicht eingerichtet — analog zu
  `fdo-architecture`s offenem Punkt, hier aber noch nicht mal vorgeschlagen.
- **Weitere Grafiken für den Vortrag** (z. B. eine reduzierte Fassung des
  `fdo-architecture`-Architekturdiagramms für Folie 8 des Talk-Konzepts)
  sind angekündigt ("Darein werden dann auch noch andere Skripte kommen"),
  aber noch kein eigener Schritt — wird S4, sobald konkret.
- **`flatten_to_jpg()` ungenutzt seit S2/S3-Nachtrag 2026-09-08** — bleibt
  als Werkzeug liegen statt entfernt zu werden; wird real erst, wenn ein
  künftiger Schritt tatsächlich ein flaches JPG braucht (z. B. für ein
  Zielsystem ohne Alphakanal-Unterstützung).
