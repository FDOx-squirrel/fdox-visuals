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

## A2. Zielbild

```
py/step_*.py  (reine Geometrie + Text, keine Rasterlogik)
     │
     ▼  main.py orchestriert
img/*.svg     (Quelle, versioniert)
     │
     ▼  cairosvg (S2/S3, in-process)
img/*.png     (Zwischenstufe bei Bedarf, oder Endprodukt bei Transparenz)
     │
     ▼  Pillow, auf Weiß geflattet
img/*.jpg     (Endprodukt für Folien/Druck)
```

Eigenschaften, an denen sich ein Rebuild messen lassen muss:

- **Kein externes CLI-Tool.** `pip install -r requirements.txt` genügt;
  kein `rsvg-convert`, kein ImageMagick, kein Node.
- **Deterministisch.** Zwei Läufe hintereinander erzeugen bytegleiche
  `.svg`/`.jpg`/`.png` (geprüft per `md5sum`, S1).
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

**Ziel:** `python main.py --list`/`--dry-run` laufen ohne `cairosvg`/`Pillow`
zu importieren; `python main.py` erzeugt beide Grafiken; zwei Läufe
hintereinander sind bytegleich.

**Uploads:** Standardbundle (A5).

`py/visuals_utils.py` hält `STEPS` (die Familienpalette, Step 1 = `#004473`),
`INK`/`MUTED`/`BG`, `font_face_css()`, `render_svg_to_png()`,
`flatten_to_jpg()`. Jeder `step_*.py` importiert von dort, trägt selbst
keinen Hex-Code für Ink/Muted/Background.

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

## S2 — Vier-Schritte-Muster-Banner + Icon-Badges

**Ziel:** `img/fdox-four-step-pattern.svg`/`.jpg` (nur die vier Schritte,
kein Header/Footer — Beschluss aus dem Ursprungschat) sowie vier
freistehende `img/fdox-step-<n>-<slug>.svg`/`.png` mit transparentem
Hintergrund.

**Uploads:** —

Geometrie 1:1 aus dem Ursprungschat übernommen (wachsendes Graph-Icon-
System: 1 Knoten → Knoten+2 Satelliten → Hub+2 externe Ringe → 5-Knoten-
Netz; Zahlen-Tag oben links am Badge). Einzige Änderung: Schrift jetzt
Fira Sans, Step-1-Farbe jetzt `#004473` statt der zunächst probeweise
verwendeten `#2451D6`.

**Abnahme:** ✅ erledigt — alle fünf Dateipaare erzeugt, PNGs mit Alphakanal
(`PIL.Image.mode == "RGBA"` geprüft), Banner-Titel/Footer tatsächlich
abwesend (Beschluss aus dem vorherigen Chat, hier nur reproduziert).

## S3 — FAIR-Digital-Object-Meta-Grafik

**Ziel:** `img/fdox-fair-digital-object-meta-graphic.svg`/`.jpg` — dieselbe
Komposition wie das hochgeladene Referenzbild (Titel links, verschachtelte
Kreise rechts, drei Leader-Lines zu Data/Metadata/PID), umgefärbt auf
`#004473` (Kern) und eine 65-%-Aufhellung davon (Ring, ersetzt das
ursprüngliche Grau).

**Uploads:** —

Zielpunkte der drei Leader-Lines sind geometrisch berechnet, nicht
abgepaust: Data landet per Konstruktion innerhalb des inneren Kreises,
Metadata im Ring-Band, PID exakt auf dem äusseren Rand (Radius = `OUTER_R`).

**Abnahme:** ✅ erledigt — Sichtprüfung (Crop-Zoom) bestätigt, dass alle drei
Linien in der beabsichtigten Zone landen; Akzentfarbe im Log bestätigt
(`accent #004473`).

---

# Teil D — Offene Punkte

- **`img/*.png` der vier Icon-Badges bleiben Endprodukt** (transparenter
  Hintergrund lässt sich nicht verlustfrei nach JPG konvertieren) — anders
  als beim Banner, wo das PNG nur Zwischenstufe zum JPG ist und gelöscht
  wird. Wenn eine transparente Variante des Banners selbst gebraucht wird,
  ist das ein neuer Schritt (`.png` behalten statt löschen), nicht Teil von
  S2.
- **CI (`--strict` bei jedem Push)** noch nicht eingerichtet — analog zu
  `fdo-architecture`s offenem Punkt, hier aber noch nicht mal vorgeschlagen.
- **Weitere Grafiken für den Vortrag** (z. B. eine reduzierte Fassung des
  `fdo-architecture`-Architekturdiagramms für Folie 8 des Talk-Konzepts)
  sind angekündigt ("Darein werden dann auch noch andere Skripte kommen"),
  aber noch kein eigener Schritt — wird S4, sobald konkret.
