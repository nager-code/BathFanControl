# Übergabe: Lüftersteuerung Bad (KN2 UP) – Stand 24.11.2026, Platine v1.5 (von oben bestückt, SMD mit bedrahtetem Netzteil und bedrahteter Klemme, Form für den Lüfterkasten)

Fortsetzung der Übergabe vom selben Tag. Neu: Pinbelegungen gegen Datenblätter geprüft, Umstellung auf KiCad 10 und auf SMD-Bauteile, Platinenform und Gehäuse für den Einbau unten links im Lüfterkasten, einseitige Bestückung, RGB-LED, geroutetes Layout, Bestellpaket. Netzteil und Netzklemme sind bedrahtet, weil es bei JLCPCB kein lagerndes SMD-Netzteil gibt; alle Bauteile der Stückliste waren am 24.11.2026 dort am Lager.

## 1. Ergebnis

| | |
|---|---|
| Platine | Umriss 76 x 63 mm (unterer Teil 76 mm breit mit Ausschnitt 14 x 30 mm für die Leitungen, Arm oben 68 x 18 mm), 2 Lagen, FR4 1,6 mm, 35 µm, nur von oben bestückt (31 SMD-Bauteile, Netzteil und Klemme bedrahtet) |
| KiCad | 10.0.8, Projekt in `kicad/` |
| Schaltplanprüfung (ERC) | 0 Meldungen |
| Regelprüfung (DRC) mit Schaltplanabgleich | 0 Verletzungen, 0 offene Verbindungen, Bericht in `doku/drc_bericht.txt` |
| Abstand zwischen Netzpotentialen | Regel 2,5 mm, eingehalten (Ausnahmen an Bauteilen: Teiler R1/R2, Snubber, Zünd- und Gate-Widerstand, Substrat-Pin des Optotriacs) |
| Abstand Netz zu 3,3 V | Regel 6 mm, eingehalten; dazu 2 mm breite Frässchlitze unter dem Netzteil und unter U2/U3 |
| Bauhöhe | ca. 20 mm (Netzteil 15,1 mm über der Platine, seine Lötstifte bis 3,4 mm darunter) |
| Gehäuse | 80,6 x 67,6 x 25,7 mm (oben rechts 8 mm schmaler), Entwurf für den 3D-Druck in `gehaeuse/` |

Nichts davon ist gebaut oder elektrisch getestet. Geprüft wurde nur in KiCad und rechnerisch am 3D-Modell.

## 2. Datenblattprüfung der Pinbelegungen

| Bauteil | Ergebnis | Folge |
|---|---|---|
| ESP32-C3-MINI-1 | alle Annahmen stimmen | Typ auf -H4X geändert, weil -N4 abgekündigt ist (gleicher Footprint) |
| SHT40-AD1B | stimmt, I2C-Adresse 0x44 | – |
| LTV-814S | stimmt | – |
| MOC3052S (Optotriac, ersetzt den AQH3223A) | 1 = Anode, 2 = Kathode, 3 frei, 4 und 6 = Ausgang (gleichwertig), 5 = Substrat, nicht anschließen; 600 V, Zündstrom max. 10 mA, 5 kV Isolation, kein Nullspannungsschalter | Pin 6 ans Gate, Pin 4 über R16 an OUT; Pin 5 auf eigenem, unverbundenem Pad, als Netzpotential behandelt. Footprint SMDIP-6 (Anschlussbreite 10,16 mm) |
| MOC3052S, LED-Strom | Zündstrom max. 10 mA, UF typ. 1,15 V / max. 1,5 V | R3 = 100 Ω (statt 150 Ω): rechnerisch 18 bis 21 mA an 3,3 V |
| ACST410-8B (Triac, DPAK) | 1 = COM, Kühlfahne = OUT, 3 = G; 800 V, 4 A (1 A bei 60 °C mit 0,5 cm² Kupfer), IGT max. 10 mA in den Quadranten I bis III, IH max. 20 mA, überspannungsfest (klemmt bei 850 V) | COM an L hinter der Sicherung, OUT zur Klemme „Lüfter“. Footprint nach ST-Datenblatt (Fahne 6,7 x 6,7 mm, 3,0 mm Abstand zu den Anschlussflächen) |
| Zündkreis | Spitzenstrom des Optotriacs max. 1 A | R16 = 390 Ω (1206): höchstens 0,92 A bei 253 V Netzspannung. R17 = 390 Ω vom Gate nach COM |
| HLK-PM03 (Netzteil, bedrahtet) | 1 und 2 = AC (gleichwertig), 3 = −Vo, 4 = +Vo; AC-Stifte 5,0 mm, Ausgangsstifte 15,0 mm auseinander, Reihenabstand 29,08 mm, Stifte 0,8 mm | KiCad-Footprint `Converter_ACDC_Hi-Link_HLK-PMxx` stimmt damit überein. Im Schaltplan AC/N = 1, AC/L = 2 |
| HLK-PM03, Beschaltung | Datenblatt verlangt Sicherung 1 A träge und Varistor am Eingang; X-Kondensator und Drossel nur für die EMV-Zulassung | F1 (T1A) und RV1 sind vorhanden. RV1 ist ein 275-VAC-Typ, das Datenblatt nennt 10D561K (350 VAC) |
| MKDS 1,5/4-5,08 (Klemme, bedrahtet) | Raster 5,08 mm, Stifte 1,0 mm (Bohrung 1,3 mm), Stiftreihe 4,6 mm hinter der Leitereinführung, 250 V / 17,5 A, 0,14–1,5 mm² | Footprint vom KiCad-Original abgeleitet, Lötaugen 2,4 statt 2,6 mm (2,68 mm Kupferabstand zwischen den Polen) |
| LTV-814S, Eingang | die beiden Eingangspins sind gleichwertig (antiparallele LEDs) | Pins 1 und 2 im Schaltplan getauscht, damit das einseitige Layout ohne Kreuzung auskommt |
| FM-B2020RGBA-HG (RGB-LED) | gemeinsame Anode an Pin 3; Pin 1 rot (Eckmarke), Pin 4 grün, Pin 2 blau; UF typ. 2,0 / 2,7 / 2,8 V | eigener Footprint nach Datenblatt (Pads 0,8 x 0,7 mm) |

Hinweis zum Snubber: ST gibt an, dass der ACST4 induktive Lasten bis 4 A ohne Snubber abschaltet. Geblieben sind trotzdem 10 nF und 100 Ω parallel zum Triac wie in der ersten Übergabe, als Reserve und gegen Störungen; als SMD mit X2-Zulassung gibt es höchstens 56 nF (Murata GA355XR7GB563KW06L, gleicher Footprint).

## 3. Bauteilwahl gegenüber der ersten Übergabe

| Ref | vorher | jetzt | JLCPCB/LCSC |
|---|---|---|---|
| X1 | Phoenix MKDS 4-polig | bleibt bedrahtet: Phoenix MKDS 1,5/4-5,08 (1715747), Schraubklemme mit waagrechter Leitereinführung | C5443561 |
| F1 | TR5 T1A | Littelfuse 0443001.DR, T1A 250 V, 10 x 3 mm (Pads passen auch für Schurter UMT 250) | C95352 |
| RV1 | S07K275 | TDK CU3225K275G2, 275 VAC, 8,0 x 6,3 mm | C211106 |
| PS1 | IRM-02-3.3 | bedrahtet: Hi-Link HLK-PM03, 3,3 V / 1 A, 34,8 x 20,5 x 15 mm, vergossen. Mean Well IRM-02-3.3 und -3.3S hatten bei JLCPCB Bestand 0 | C209904 |
| C1 | Elko radial | Panasonic EEHZK1E101UP, Hybrid-Polymer-Elko 100 µF 25 V, 6,3 x 5,8 mm; laut Datenblatt auf feuchte Wärme geprüft (85 °C, 85–90 % r. F., 2000 h unter Spannung), 4000 h bei 125 °C, AEC-Q200 | C454668 |
| C2 | X2 Folie 10 nF | Murata GA355QR7GB103KW01L, 10 nF X2 250 VAC, Bauform 2220 | C237426 |
| J1 | Lochreihe 1,27 mm | SMD-Pads 1,27 mm, unbestückt | – |
| U4 | SHT40-AD1B | SHT40-AD1F-R2 mit Polyimid-Membran (IP68), gleiche Pins, gleicher Footprint, Adresse 0x44 | C7461846 |
| U3, Q1, R16, R17 | Photo-Triac AQH3223A (ein Bauteil) | Optotriac Lite-On MOC3052S-TA1 plus Triac ST ACST410-8BTR mit Zündwiderstand 390 Ω (1206) und Gate-Widerstand 390 Ω (0603). Grund: vom AQH3223A lagen bei JLCPCB nur 7 Stück, und die Markenbauteile sind robuster | C115471, C221462, C4491, C23151 |
| D1, R13–R15 | – | neu: RGB-LED Foshan NationStar FM-B2020RGBA-HG (2,1 x 2,1 mm) mit Vorwiderständen 680 Ω / 220 Ω / 150 Ω | C42421005, C23228, C22962, C22808 |

Bedrahtet sind nur noch Netzteil und Klemme. Beide werden von oben bestückt und im Wellenlöten gelötet; ihre Stifte stehen unten über (Netzteil bis 3,4 mm, Klemme 1,9 mm).

## 4. Anordnung

Die Platine ist so gezeichnet, wie sie eingebaut von vorn zu sehen ist: unten links im Lüfterkasten, vor dem Lüftergehäuse. Alle Bauteile sitzen auf der Oberseite; die Unterseite dient als zweite Verdrahtungsebene, dort stehen nur die Lötstifte von Netzteil und Klemme über.

- **Unterer Teil (76 mm breit, bis 43,2 mm Höhe):** ganz links ein 22 mm breiter 3,3-V-Streifen (Programmierpads J1, Stützkondensator), daneben das Netzteil PS1 (3,3 V links, Netz rechts) und die Schraubklemme X1 mit der Leitereinführung nach rechts. Rechts neben der Klemme ist die Platine 13,4 x 30 mm ausgeschnitten: dort liegt der Anschlussraum für die Adern. Über Netzteil und Klemme die Netzreihe mit dem Triac Q1 (liegend, Kühlfahne links), Varistor, Sicherung und Teilerwiderständen. Der Snubber R5/C2 sitzt im Streifen zwischen Netzteil und Klemme.
- **Isolationsschlitz 2 mm**, nach rechts offen, zwischen Netzreihe und Arm. Der Optotriac U3 und der Optokoppler U2 sitzen darüber: Netzpins unten, 3,3-V-Pins oben.
- **Arm oben (68 x 18 mm):** links das WLAN-Modul U1 mit der Antenne an der Oberkante, daneben C1 und die RGB-LED D1 mit ihren Vorwiderständen, ganz rechts hinter einem Thermoschlitz die Sensorinsel mit U4 und C7. Die Ecke oben rechts ist abgeschrägt und zeigt zum Lüfter-Einlass. Der Arm ist 8 mm schmaler als der untere Teil.
- **Zwei Bohrungen 6,6 mm** (unten links und im Arm) für die Schraubdome des Gehäuses, beide im 3,3-V-Bereich und mehr als 10 mm vom Netzkupfer entfernt.
- **Klemmenbelegung von oben nach unten: L, Licht, N, Lüfter** (Raster 5,08 mm). Die Reihenfolge ergibt sich aus der kreuzungsfreien Verdrahtung. Die Beschriftung steht auf der Unterseite neben den Stiften und im Gehäusedeckel.
- **Isolation:** kupferfreie Streifen von 6,3 mm zwischen Netz und 3,3 V (im unteren Teil senkrecht mit Schlitz 2 x 20 mm unter dem Netzteil, darüber waagrecht mit dem durchgehenden Schlitz).
- **Netzseite von Hand geroutet** (1,0 mm; nach den 2 x 100 kΩ 0,4 mm, dort fließt weniger als 2 mA). Licht, N und Lüfter laufen auf der Unterseite von den Stiften der Klemme erst nach links und dann nebeneinander nach oben in die Netzreihe, L vom obersten Pol direkt zur Sicherung. Die **3,3-V-Seite hat der Autorouter Freerouting verlegt**, danach Masseflächen auf beiden Lagen mit Masse-Durchkontaktierungen.
- **RGB-LED D1** (gemeinsame Anode an 3,3 V): rot an GPIO4 über 680 Ω, grün an GPIO5 über 220 Ω, blau an GPIO1 über 150 Ω. Die LED leuchtet bei Pegel 0; beim Start sind die Pins hochohmig, die LED ist aus. Rechnerisch je etwa 2 bis 3 mA; grün und blau werden dunkler, wenn ihre Flussspannung an der oberen Grenze (3,2 V) liegt.

## 5. Dateien

- `kicad/` – Projekt für KiCad 10: Schaltplan, Platine, Regeln (`.kicad_dru`), Symbol- und Footprint-Bibliothek des Projekts
- `bestellpaket/` – Gerber und Bohrdaten (auch als `gerber_lueftersteuerung.zip`), `BOM_JLCPCB.csv`, `CPL_JLCPCB.csv`, Bestückungspläne, `LIESMICH.md`
- `doku/` – Schaltplan als PDF, Bilder der Platine (auch 3D-Ansichten und `platine_3d.glb` zum Drehen), DRC-Bericht
- `gehaeuse/` – Gehäuse für den 3D-Druck: OpenSCAD-Modell, STL für Wanne und Deckel, Bilder
- `skripte/` – erzeugen alles aus dem ursprünglichen Schaltplan neu (`alles.sh`, `bis_sauber.sh`, `export_fab.sh`); laufen in einem KiCad-10-Container
- `eingang/` – die ursprünglich übergebenen Dateien

## 6. Vor der Bestellung zu prüfen

1. **Bedrahtete Teile.** Beim Bestellen die Bestückung bedrahteter Bauteile mit auswählen (JLCPCB führt Klemme und Netzteil unter Wellenlöten). Die Stifte des Netzteils sind 5 mm lang und stehen unten bis 3,4 mm über; das Gehäuse lässt 4 mm Platz.
2. **Drehlage in der JLCPCB-Vorschau.** Die Winkel in `CPL_JLCPCB.csv` sind KiCad-Winkel; JLCPCB dreht einzelne Gehäuse anders. In der Bestückungsvorschau jedes gepolte Bauteil ansehen (U1–U4, Q1, C1, D1, PS1, X1).
3. **Sensor.** U4 ist der Sensirion SHT40-AD1F-R2 mit Polyimid-Membran, bei JLCPCB unter C7461846 am Lager. Unter C54823945 gibt es eine Fremdmarke (Tokmas), deren Datenblatt keine Membran nennt: nicht verwenden. Die Membran nicht überlackieren.
4. **Lagerbestand bei JLCPCB** (Bauteilsuche am 23. und 24.11.2026): alle Teile der Stückliste waren am Lager. Die kleinsten Bestände: X2-Kondensator C2 448 Stück, Triac Q1 rund 1.200, Sensor rund 2.100, Netzteil rund 3.200. Ausweichtyp für das Netzteil: YLPTEC HAW3-220S03T2 (C19724490), Reihenabstand 29,4 statt 29,08 mm.
5. **Netzteil.** Das HLK-PM03 nennt im Datenblatt 3000 VAC (an anderer Stelle 2500 VAC) Isolation und „Entwurf entspricht UL/CE“; eine Zertifizierung des Moduls weist es nicht aus. Wer ein zertifiziertes Netzteil will, braucht ein anderes Modul und einen neuen Footprint.
6. **Sicherung.** Die 0443001.DR schaltet 50 A bei 250 VAC ab. Wer mehr will: Schurter UMT 250 (200 A) passt auf dieselben Pads.
7. **Antenne.** Die Antenne sitzt an der Oberkante des Arms, gut 25 mm über dem Netzteil; links liegt die Kastenwand, dahinter das Lüftergehäuse. Wie gut das WLAN im Kasten ist, zeigt erst ein Versuch.
8. **Typenschild des KN2:** die elektrischen Daten sind weiter nicht bekannt. Im Kasten liegen flexible Litzen mit Steckverbindern; die Schraubklemme nimmt Leiter von 0,14 bis 1,5 mm² auf, feindrähtige am besten mit Aderendhülse.
9. **Schutzlack.** Die Steuerung sitzt im Lüfterkasten im Strom der Badluft; die Platine sollte lackiert werden (Sensor, Klemme, LED und Programmierpads aussparen). Panasonic verlangt für den Kondensator C1 einen halogenfreien Lack, der die Gummidichtung am Boden zu höchstens zwei Dritteln bedeckt, und schließt Betauung als Betriebsbedingung aus; die Lebensdauer begrenzt Panasonic wegen der Dichtung auf 15 Jahre. Wer ganz ohne Elektrolyt auskommen will: Tantal Vishay 293D107X9016D2TE3 (C129696, Bauform D, neuer Footprint nötig).

## 7. Noch offen

- Firmware (Regellogik siehe erste Übergabe, Abschnitt 7; Lüfter an GPIO10, Licht an GPIO3 low-aktiv, SHT40 an GPIO6/7, Adresse 0x44, RGB-LED low-aktiv an GPIO4 rot / GPIO5 grün / GPIO1 blau)
- Home Assistant vorhanden? (entscheidet über ESPHome oder eigene Firmware)
- Gehäuse: Entwurf für den 3D-Druck in `gehaeuse/`, passend zur Platine v1.5 und zum Einbau unten links vor dem Lüftergehäuse. Dort sind nachgemessen höchstens 85 mm Breite, 40 mm Tiefe und 140 mm Höhe frei; das Gehäuse braucht 80,6 x 25,7 x 67,6 mm. Noch nicht gedruckt. Details in `gehaeuse/README.md`

## 8. Sicherheit

230 V im Feuchtraum: geschlossenes Gehäuse außerhalb des Spritzbereichs, Anschluss durch eine Elektrofachkraft abnehmen lassen. Netzkupfer reicht an der Klemmenseite bis etwa 2,5 mm an die Platinenkante. Einrohrsystem am gemeinsamen Schacht: Brandschutzklappe nicht verändern.
