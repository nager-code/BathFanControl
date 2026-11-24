# Übergabe: Lüftersteuerung Bad (KN2 UP) – Stand 24.11.2026, Platine v1.6 (von oben bestückt, SMD mit bedrahtetem Netzteil und bedrahteter Klemme, Form für den Lüfterkasten)

Stand nach der Überarbeitung des ersten Entwurfs (der ursprüngliche Schaltplan und seine Übergabe liegen in der Git-Historie). Neu: Pinbelegungen gegen Datenblätter geprüft, Umstellung auf KiCad 10 und auf SMD-Bauteile, Platinenform und Gehäuse für den Einbau unten links im Lüfterkasten, einseitige Bestückung, RGB-LED, USB-C-Buchse zum Programmieren, geroutetes Layout, Bestellpaket. Netzteil und Netzklemme sind bedrahtet, weil es bei JLCPCB kein lagerndes SMD-Netzteil gibt; alle Bauteile der Stückliste waren am 24.11.2026 dort am Lager.

## 0. Aufgabe und Lüfter

Eigene Steuerung für einen Badlüfter, die den Lüfter feuchteabhängig schaltet und nicht stundenlang nutzlos läuft.

- Versorgung 230 V, zweiter 230-V-Eingang vom Lichtschalter (zeigt Aktivität im Bad)
- Luftfeuchte messen und den Lüfter danach schalten
- Fortschritt messen: sinkt die Feuchte nicht (feuchte Wohnungs- oder Außenluft), längere Pause einlegen. Die alte Steuerung lief teils 8 Stunden durch.
- Licht 10 Minuten an und noch kein Feuchteanstieg: Lüfter kurz einschalten
- Über WLAN erreichbar, möglichst wenig Stromverbrauch

Lüfter: KN2 UP Ventilator (Unterputz, Einrohrlüftungs-System, Baureihe KN), Anleitung: https://de.ventilatory.net/media/catalog/product/data/ds-kn2-de.pdf. Motor ca. 50 W, keine Grundlüftung ab Werk, also ein Schaltkanal. Laut Anleitung zerstört falsche Beschaltung die Elektronik im Gerät; die Steuerung schaltet deshalb nur die Phase vor dem Ventilator. Die elektrischen Daten stehen nur auf dem Typenschild, das nicht vorliegt.

### GPIO-Belegung des ESP32-C3-MINI-1

| GPIO | Modul-Pin | Funktion |
|---|---|---|
| GPIO6 | 20 | SDA (SHT40, Adresse 0x44) |
| GPIO7 | 21 | SCL (SHT40) |
| GPIO3 | 6 | Lichtschalter, low = Licht an |
| GPIO10 | 16 | Lüfter ein (high) |
| GPIO4 / GPIO5 / GPIO1 | 18 / 19 / 13 | RGB-LED rot / grün / blau, leuchtet bei low |
| GPIO18 / GPIO19 | 26 / 27 | USB D− / D+ (Programmieren über die USB-C-Buchse) |
| GPIO9 | 23 | Boot, Pull-up 10 kΩ; Lötflächen JP1 nach Masse |
| GPIO2, GPIO8 | 5, 22 | Strapping, Pull-up 10 kΩ |
| EN | 8 | Pull-up 10 kΩ, 1 µF gegen Masse; Lötflächen JP2 nach Masse |
| GPIO20 / GPIO21 | 30 / 31 | RX / TX, nicht herausgeführt |

### Regellogik (Firmware, noch nicht geschrieben)

Gerechnet wird mit absoluter Feuchte (g/m³ aus Temperatur und relativer Feuchte). Ein langsamer Mittelwert über Stunden bildet die Basis.

1. Bereit: Messung alle 30 s.
2. Start: schneller Anstieg (z. B. +5 % rF in 5 min) oder Basis +10 %.
3. Lüften mit Fortschrittskontrolle: alle 10 bis 15 min muss die Feuchte um z. B. 2 bis 3 % rF fallen. Ziel Basis +3 %, danach 5 min Nachlauf.
4. Kein Fortschritt nach zwei Fenstern: Pause 1 h, bei Wiederholung 2 h, dann 4 h. Basis auf den aktuellen Wert nachziehen. Harte Obergrenze 45 bis 60 min Laufzeit.
5. Aktivität: Licht 10 min an ohne Anstieg, dann 2 bis 3 min Probelauf. Steigt die Feuchte dabei, weiter mit Schritt 3. Nächster Probelauf frühestens nach 15 bis 20 min.

WLAN: vorgeschlagen ESPHome (Home Assistant, Updates über WLAN, Weboberfläche), alternativ eigene Firmware mit MQTT/REST. Schwellwerte, Pausenzeiten und manuelles Ein/Aus einstellbar. Ob Home Assistant vorhanden ist, ist noch offen.

## 1. Ergebnis

| | |
|---|---|
| Platine | Umriss 68 x 72,5 mm (unten rechts ein Ausschnitt 13,4 x 34,5 mm für die Leitungen, darüber nach rechts offener Isolationsschlitz), 2 Lagen, FR4 1,6 mm, 35 µm, nur von oben bestückt (38 SMD-Bauteile, Netzteil und Klemme bedrahtet) |
| KiCad | 10.0.8, Projekt in `kicad/` |
| Schaltplanprüfung (ERC) | 0 Meldungen |
| Regelprüfung (DRC) mit Schaltplanabgleich | 0 Verletzungen, 0 offene Verbindungen, Bericht in `doku/drc_bericht.txt` |
| Abstand zwischen Netzpotentialen | Regel 2,5 mm, eingehalten (Ausnahmen an Bauteilen: Teiler R1/R2, Snubber, Zünd- und Gate-Widerstand, Substrat-Pin des Optotriacs) |
| Abstand Netz zu 3,3 V | Regel 6 mm, eingehalten; dazu 2 mm breite Frässchlitze unter dem Netzteil und unter U2/U3 |
| Bauhöhe | ca. 20 mm (Netzteil 15,1 mm über der Platine, seine Lötstifte bis 3,4 mm darunter) |
| Gehäuse | 72,6 x 77,1 x 25,7 mm, Entwurf für den 3D-Druck in `gehaeuse/` |
| Bestückungsdruck | alle Texte mindestens 1,0 mm hoch und 0,15 mm stark (als DRC-Regel hinterlegt) |

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
| RT9013-33GB (Regler für USB, SOT-23-5) | 1 = VIN, 2 = GND, 3 = EN, 4 = frei, 5 = VOUT; Eingang max. 5,5 V, 500 mA, Dropout typ. 0,25 V | EN an VIN; Eingang über Schottky-Diode D2 an VBUS, Ausgang direkt an 3,3 V |
| TYPE-C-31-D-06 (USB-C stehend, 16-polig) | A1/A12/B1/B12 = GND, A4/A9/B4/B9 = VBUS, A5 = CC1, B5 = CC2, A6/B6 = D+, A7/B7 = D−, A8/B8 = SBU; Lötflächen 0,30 x 0,87 mm im Raster 0,5 mm, vier Gehäusezapfen in Langlöchern | eigener Footprint nach dem Lötbild im Datenblatt. D+ an GPIO19, D− an GPIO18 (im ESP32-C3 fest so belegt) |
| Zündkreis | Spitzenstrom des Optotriacs max. 1 A | R16 = 390 Ω (1206): höchstens 0,92 A bei 253 V Netzspannung. R17 = 390 Ω vom Gate nach COM |
| HLK-PM03 (Netzteil, bedrahtet) | 1 und 2 = AC (gleichwertig), 3 = −Vo, 4 = +Vo; AC-Stifte 5,0 mm, Ausgangsstifte 15,0 mm auseinander, Reihenabstand 29,08 mm, Stifte 0,8 mm | KiCad-Footprint `Converter_ACDC_Hi-Link_HLK-PMxx` stimmt damit überein. Im Schaltplan AC/N = 1, AC/L = 2 |
| HLK-PM03, Beschaltung | Datenblatt verlangt Sicherung 1 A träge und Varistor am Eingang; X-Kondensator und Drossel nur für die EMV-Zulassung | F1 (T1A) und RV1 sind vorhanden. RV1 ist ein 275-VAC-Typ, das Datenblatt nennt 10D561K (350 VAC) |
| MKDS 1,5/4-5,08 (Klemme, bedrahtet) | Raster 5,08 mm, Stifte 1,0 mm (Bohrung 1,3 mm), Stiftreihe 4,6 mm hinter der Leitereinführung, 250 V / 17,5 A, 0,14–1,5 mm² | Footprint vom KiCad-Original abgeleitet, Lötaugen 2,4 statt 2,6 mm (2,68 mm Kupferabstand zwischen den Polen) |
| LTV-814S, Eingang | die beiden Eingangspins sind gleichwertig (antiparallele LEDs) | Pins 1 und 2 im Schaltplan getauscht, damit das einseitige Layout ohne Kreuzung auskommt |
| FM-B2020RGBA-HG (RGB-LED) | gemeinsame Anode an Pin 3; Pin 1 rot (Eckmarke), Pin 4 grün, Pin 2 blau; UF typ. 2,0 / 2,7 / 2,8 V | eigener Footprint nach Datenblatt (Pads 0,8 x 0,7 mm) |

Hinweis zum Snubber: ST gibt an, dass der ACST4 induktive Lasten bis 4 A ohne Snubber abschaltet. Geblieben sind trotzdem 10 nF und 100 Ω parallel zum Triac wie im ersten Entwurf, als Reserve und gegen Störungen; als SMD mit X2-Zulassung gibt es höchstens 56 nF (Murata GA355XR7GB563KW06L, gleicher Footprint).

## 3. Bauteilwahl gegenüber dem ersten Entwurf

| Ref | vorher | jetzt | JLCPCB/LCSC |
|---|---|---|---|
| X1 | Phoenix MKDS 4-polig | bleibt bedrahtet: Phoenix MKDS 1,5/4-5,08 (1715747), Schraubklemme mit waagrechter Leitereinführung | C5443561 |
| F1 | TR5 T1A | Littelfuse 0443001.DR, T1A 250 V, 10 x 3 mm (Pads passen auch für Schurter UMT 250) | C95352 |
| RV1 | S07K275 | TDK CU3225K275G2, 275 VAC, 8,0 x 6,3 mm | C211106 |
| PS1 | IRM-02-3.3 | bedrahtet: Hi-Link HLK-PM03, 3,3 V / 1 A, 34,8 x 20,5 x 15 mm, vergossen. Mean Well IRM-02-3.3 und -3.3S hatten bei JLCPCB Bestand 0 | C209904 |
| C1 | Elko radial | Panasonic EEHZK1E101UP, Hybrid-Polymer-Elko 100 µF 25 V, 6,3 x 5,8 mm; laut Datenblatt auf feuchte Wärme geprüft (85 °C, 85–90 % r. F., 2000 h unter Spannung), 4000 h bei 125 °C, AEC-Q200 | C454668 |
| C2 | X2 Folie 10 nF | Murata GA355QR7GB103KW01L, 10 nF X2 250 VAC, Bauform 2220 | C237426 |
| J1 | Lochreihe 1,27 mm | entfällt; programmiert wird über USB | – |
| J2, U5, D2, C8, C9, R18, R19 | – | neu: stehende USB-C-Buchse HRO TYPE-C-31-D-06 (6,4 mm hoch), Regler Richtek RT9013-33GB, Schottky-Diode B5819W, 2 x 1 µF, 2 x 5,1 kΩ an den CC-Leitungen | C2689964, C47773, C8598, C15849, C23186 |
| JP1, JP2 | – | neu: Lötflächen zum Überbrücken, Boot (GPIO9 nach Masse) und Reset (EN nach Masse); kein Bauteil | – |
| U4 | SHT40-AD1B | SHT40-AD1F-R2 mit Polyimid-Membran (IP68), gleiche Pins, gleicher Footprint, Adresse 0x44 | C7461846 |
| U3, Q1, R16, R17 | Photo-Triac AQH3223A (ein Bauteil) | Optotriac Lite-On MOC3052S-TA1 plus Triac ST ACST410-8BTR mit Zündwiderstand 390 Ω (1206) und Gate-Widerstand 390 Ω (0603). Grund: vom AQH3223A lagen bei JLCPCB nur 7 Stück, und die Markenbauteile sind robuster | C115471, C221462, C4491, C23151 |
| D1, R13–R15 | – | neu: RGB-LED Foshan NationStar FM-B2020RGBA-HG (2,1 x 2,1 mm) mit Vorwiderständen 680 Ω / 220 Ω / 150 Ω | C42421005, C23228, C22962, C22808 |

Bedrahtet sind nur noch Netzteil und Klemme. Beide werden von oben bestückt und im Wellenlöten gelötet; ihre Stifte stehen unten über (Netzteil bis 3,4 mm, Klemme 1,9 mm).

## 4. Anordnung

Die Platine ist so gezeichnet, wie sie eingebaut von vorn zu sehen ist: unten links im Lüfterkasten, vor dem Lüftergehäuse. Alle Bauteile sitzen auf der Oberseite; die Unterseite dient als zweite Verdrahtungsebene, dort stehen nur die Lötstifte von Netzteil und Klemme über. Einen beschrifteten Plan zeigt `doku/lageplan.png`. Höhen zählen ab der Unterkante des Netzteil-Riegels (y = 0).

- **Streifen ganz unten (4,5 mm hoch):** hier sitzt links die Bohrung für den unteren Schraubdom, unter dem 3,3-V-Ende des Netzteils.
- **Riegel (54,6 x 30 mm):** das Netzteil PS1 (3,3 V links, Netz rechts) und die Schraubklemme X1 mit der Leitereinführung nach rechts. Rechts neben der Klemme ist die Platine ausgeschnitten: dort liegt der Anschlussraum für die Adern. Zwischen Netzteil und Klemme sitzt der Snubber R5/C2.
- **Netzreihe (bis 43,2 mm Höhe, 68 mm breit):** Triac Q1 (liegend, Kühlfahne links), Varistor, Sicherung und Teilerwiderstände. Links davon bleibt ein 14 mm breiter 3,3-V-Streifen.
- **Isolationsschlitz 2 mm**, nach rechts offen, zwischen Netzreihe und Arm. Der Optotriac U3 und der Optokoppler U2 sitzen darüber: Netzpins unten, 3,3-V-Pins oben.
- **Arm oben (68 x 23 mm):** links das WLAN-Modul U1 mit der Antenne an der Oberkante, daneben C1, die RGB-LED D1 mit ihren Vorwiderständen und die stehende USB-C-Buchse J2 mit Regler; ganz rechts hinter einem Thermoschlitz die Sensorinsel mit U4 und C7. Die Ecke oben rechts ist abgeschrägt und zeigt zum Lüfter-Einlass.
- **Zwei Bohrungen 6,6 mm** (unten links und im Arm) für die Schraubdome des Gehäuses, beide im 3,3-V-Bereich und mehr als 10 mm vom Netzkupfer entfernt.
- **Klemmenbelegung von oben nach unten: L, Licht, N, Lüfter** (Raster 5,08 mm). Die Reihenfolge ergibt sich aus der kreuzungsfreien Verdrahtung. Sie steht auf der Oberseite im unteren Streifen, auf der Unterseite neben den Stiften und im Gehäusedeckel.
- **Isolation:** kupferfreie Streifen von 6,3 mm zwischen Netz und 3,3 V (im unteren Teil senkrecht mit Schlitz 2 x 20 mm unter dem Netzteil, darüber waagrecht mit dem durchgehenden Schlitz).
- **Netzseite von Hand geroutet** (1,0 mm; nach den 2 x 100 kΩ 0,4 mm, dort fließt weniger als 2 mA). Licht, N und Lüfter laufen auf der Unterseite von den Stiften der Klemme erst nach links und dann nebeneinander nach oben in die Netzreihe, L vom obersten Pol direkt zur Sicherung. Die **3,3-V-Seite hat der Autorouter Freerouting verlegt**, danach Masseflächen auf beiden Lagen mit Masse-Durchkontaktierungen.
- **RGB-LED D1** (gemeinsame Anode an 3,3 V): rot an GPIO4 über 680 Ω, grün an GPIO5 über 220 Ω, blau an GPIO1 über 150 Ω. Die LED leuchtet bei Pegel 0; beim Start sind die Pins hochohmig, die LED ist aus. Rechnerisch je etwa 2 bis 3 mA; grün und blau werden dunkler, wenn ihre Flussspannung an der oberen Grenze (3,2 V) liegt.
- **USB zum Programmieren:** die Buchse J2 steht senkrecht, der Stecker kommt von vorn; sie ist nur bei abgenommenem Deckel erreichbar. D+ und D− gehen direkt an GPIO19 und GPIO18, der ESP32-C3 hat USB eingebaut. Die 5 V aus USB versorgen die Platine über die Diode D2 und den Regler U5 mit 3,3 V, damit ohne Netzspannung programmiert werden kann. Für den Notfall (Firmware legt USB lahm): JP1 überbrücken und kurz JP2 überbrücken, dann meldet sich der Bootloader. Eine ESD-Schutzbeschaltung an den Datenleitungen gibt es nicht.
- **Bestückungsdruck:** oben stehen die Namen der größeren Bauteile, BOOT/RST, USB, LED und die Klemmenbelegung, unten die Belegung der Netzteil- und Klemmenstifte. Für die kleinen Bauteile ist kein Platz; dafür gibt es den Lageplan.

## 5. Dateien

- `kicad/` – Projekt für KiCad 10: Schaltplan, Platine, Regeln (`.kicad_dru`), Symbol- und Footprint-Bibliothek des Projekts
- `bestellpaket/` – Gerber und Bohrdaten (auch als `gerber_lueftersteuerung.zip`), `BOM_JLCPCB.csv`, `CPL_JLCPCB.csv`, Bestückungspläne, `LIESMICH.md`
- `doku/` – beschrifteter Lageplan der Platine (`lageplan.png`/`.svg`: was sitzt wo, wozu), Zeichnung der Einbaulage (`einbaulage.svg`), Schaltplan als PDF, Bilder der Platine (3D-Ansichten von allen Seiten in `platine_3d_ansichten.png`, `platine_3d.glb` zum Drehen), DRC-Bericht
- `gehaeuse/` – Gehäuse für den 3D-Druck: OpenSCAD-Modell, STL für Wanne und Deckel, Bilder
- `skripte/` – erzeugen Platine und Bestellpaket aus dem Schaltplan in `kicad/` neu (`alles.sh`, `bis_sauber.sh`, `export_fab.sh`); laufen in einem KiCad-10-Container

## 6. Vor der Bestellung zu prüfen

1. **Bedrahtete Teile.** Beim Bestellen die Bestückung bedrahteter Bauteile mit auswählen (JLCPCB führt Klemme und Netzteil unter Wellenlöten). Die Stifte des Netzteils sind 5 mm lang und stehen unten bis 3,4 mm über; das Gehäuse lässt 4 mm Platz.
2. **Drehlage in der JLCPCB-Vorschau.** Die Winkel in `CPL_JLCPCB.csv` sind KiCad-Winkel; JLCPCB dreht einzelne Gehäuse anders. In der Bestückungsvorschau jedes gepolte Bauteil ansehen (U1–U5, Q1, C1, D1, D2, J2, PS1, X1).
3. **Sensor.** U4 ist der Sensirion SHT40-AD1F-R2 mit Polyimid-Membran, bei JLCPCB unter C7461846 am Lager. Unter C54823945 gibt es eine Fremdmarke (Tokmas), deren Datenblatt keine Membran nennt: nicht verwenden. Die Membran nicht überlackieren.
4. **Lagerbestand bei JLCPCB** (Bauteilsuche am 23. und 24.11.2026): alle Teile der Stückliste waren am Lager. Die kleinsten Bestände: X2-Kondensator C2 448 Stück, Triac Q1 rund 1.200, Sensor rund 2.100, USB-Buchse rund 2.500 (baugleich mit gleichem Lötbild: SHOU HAN TYPE-C 16P LTH6.8, C5187468, rund 52.000), Netzteil rund 3.200. Ausweichtyp für das Netzteil: YLPTEC HAW3-220S03T2 (C19724490), Reihenabstand 29,4 statt 29,08 mm.
5. **USB-Buchse.** Das Datenblatt empfiehlt 0,8 mm Platinendicke; auf der 1,6-mm-Platine stehen die 0,95 mm langen Gehäusezapfen unten nicht über. Sie sitzen in metallisierten Langlöchern und werden von oben mitgelötet; ob das mechanisch genügt, zeigt erst der Aufbau. Den Stecker deshalb gerade ziehen und nicht hebeln. USB nur anstecken, wenn die Platine vom Netz getrennt ist.
6. **Netzteil.** Das HLK-PM03 nennt im Datenblatt 3000 VAC (an anderer Stelle 2500 VAC) Isolation und „Entwurf entspricht UL/CE“; eine Zertifizierung des Moduls weist es nicht aus. Wer ein zertifiziertes Netzteil will, braucht ein anderes Modul und einen neuen Footprint.
7. **Sicherung.** Die 0443001.DR schaltet 50 A bei 250 VAC ab. Wer mehr will: Schurter UMT 250 (200 A) passt auf dieselben Pads.
8. **Antenne.** Die Antenne sitzt an der Oberkante des Arms, gut 25 mm über dem Netzteil; links liegt die Kastenwand, dahinter das Lüftergehäuse. Wie gut das WLAN im Kasten ist, zeigt erst ein Versuch.
9. **Typenschild des KN2:** die elektrischen Daten sind weiter nicht bekannt. Im Kasten liegen flexible Litzen mit Steckverbindern; die Schraubklemme nimmt Leiter von 0,14 bis 1,5 mm² auf, feindrähtige am besten mit Aderendhülse.
10. **Schutzlack.** Die Steuerung sitzt im Lüfterkasten im Strom der Badluft; die Platine sollte lackiert werden (Sensor, Klemme, LED, USB-Buchse und die Lötflächen JP1/JP2 aussparen). Panasonic verlangt für den Kondensator C1 einen halogenfreien Lack, der die Gummidichtung am Boden zu höchstens zwei Dritteln bedeckt, und schließt Betauung als Betriebsbedingung aus; die Lebensdauer begrenzt Panasonic wegen der Dichtung auf 15 Jahre. Wer ganz ohne Elektrolyt auskommen will: Tantal Vishay 293D107X9016D2TE3 (C129696, Bauform D, neuer Footprint nötig).

## 7. Noch offen

- Firmware (Regellogik und GPIO-Belegung siehe Abschnitt 0). Erstes Aufspielen über die USB-C-Buchse, danach Updates über WLAN.
- Home Assistant vorhanden? (entscheidet über ESPHome oder eigene Firmware)
- Gehäuse: Entwurf für den 3D-Druck in `gehaeuse/`, passend zur Platine v1.6 und zum Einbau unten links vor dem Lüftergehäuse. Dort sind nachgemessen höchstens 85 mm Breite, 40 mm Tiefe und 140 mm Höhe frei; das Gehäuse braucht 72,6 x 25,7 x 77,1 mm. Noch nicht gedruckt. Details in `gehaeuse/README.md`

## 8. Sicherheit

230 V im Feuchtraum: geschlossenes Gehäuse außerhalb des Spritzbereichs, Anschluss durch eine Elektrofachkraft abnehmen lassen. Netzkupfer reicht an der Klemmenseite bis etwa 2,5 mm an die Platinenkante. Einrohrsystem am gemeinsamen Schacht: Brandschutzklappe nicht verändern.
