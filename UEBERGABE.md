# Übergabe: Lüftersteuerung Bad (KN2 UP) – Stand 23.11.2026, Platine v1.3 (nur SMD, einseitig bestückt, Form für den Lüfterkasten)

Fortsetzung der Übergabe vom selben Tag. Neu: Pinbelegungen gegen Datenblätter geprüft, Umstellung auf KiCad 10 und auf ausschließlich SMD-Bauteile, Platinenform und Gehäuse für den Einbau unten links im Lüfterkasten, einseitige Bestückung, RGB-LED, geroutetes Layout, Bestellpaket.

## 1. Ergebnis

| | |
|---|---|
| Platine | Umriss 76 x 63 mm (unterer Teil 76 mm breit mit Ausschnitt 14 x 30 mm für die Leitungen, Arm oben 68 x 18 mm), 2 Lagen, FR4 1,6 mm, 35 µm, nur auf der Oberseite bestückt |
| KiCad | 10.0.8, Projekt in `kicad/` |
| Schaltplanprüfung (ERC) | 0 Meldungen |
| Regelprüfung (DRC) mit Schaltplanabgleich | 0 Verletzungen, 0 offene Verbindungen, Bericht in `doku/drc_bericht.txt` |
| Abstand zwischen Netzpotentialen | Regel 2,5 mm, eingehalten (Ausnahmen wie bisher: Teiler, Snubber, Gate-Pad) |
| Abstand Netz zu 3,3 V | Regel 6 mm, eingehalten; dazu 2 mm breite Frässchlitze unter dem Netzteil und unter U2/U3 |
| Bauhöhe | ca. 18 mm (Netzteil 16 mm über der Platine, unten nichts) |
| Gehäuse | 80,6 x 67,6 x 23,5 mm (oben rechts 8 mm schmaler), Entwurf für den 3D-Druck in `gehaeuse/` |

Nichts davon ist gebaut oder elektrisch getestet. Geprüft wurde nur in KiCad und rechnerisch am 3D-Modell.

## 2. Datenblattprüfung der Pinbelegungen

| Bauteil | Ergebnis | Folge |
|---|---|---|
| ESP32-C3-MINI-1 | alle Annahmen stimmen | Typ auf -H4X geändert, weil -N4 abgekündigt ist (gleicher Footprint) |
| SHT40-AD1B | stimmt, I2C-Adresse 0x44 | – |
| LTV-814S | stimmt | – |
| AQH3223A | Pins 2, 3, 6, 8 stimmen. Pins 1 und 4 sind intern mit der Kathode verbunden, Pin 5 ist das Gate | Pins 1/4/5 bleiben auf eigenen, unverbundenen Pads; Pin 5 wird als Netzpotential behandelt |
| AQH3223A, LED-Strom | Zündstrom max. 10 mA, empfohlen 15–25 mA | R3 von 150 Ω auf 100 Ω (rechnerisch ca. 17–21 mA statt 14 mA) |
| IRM-02-3.3 | Pin 1 ist AC/N, nicht AC/L | entfällt durch die SMD-Ausführung, siehe unten |
| IRM-02-3.3S (SMD) | 1 = AC/L, 24 = AC/N, 12 = +Vo, 13 = −Vo | so im Schaltplan |
| LTV-814S, Eingang | die beiden Eingangspins sind gleichwertig (antiparallele LEDs) | Pins 1 und 2 im Schaltplan getauscht, damit das einseitige Layout ohne Kreuzung auskommt |
| FM-B2020RGBA-HG (RGB-LED) | gemeinsame Anode an Pin 3; Pin 1 rot (Eckmarke), Pin 4 grün, Pin 2 blau; UF typ. 2,0 / 2,7 / 2,8 V | eigener Footprint nach Datenblatt (Pads 0,8 x 0,7 mm) |

Hinweis zum Snubber: Panasonic nennt allgemein 0,1 µF und 20–100 Ω. Geblieben sind 10 nF und 100 Ω wie in der ersten Übergabe; als SMD mit X2-Zulassung gibt es höchstens 56 nF (Murata GA355XR7GB563KW06L, gleicher Footprint).

## 3. Umstellung auf SMD und Sensor mit Membran

| Ref | vorher | jetzt | JLCPCB/LCSC |
|---|---|---|---|
| X1 | Phoenix MKDS 4-polig | 2 x WAGO 2061-602/998-404 (je 2-polig, Raster 6 mm, 0,5–1,5 mm², 250 V/17,5 A) | C2765058 |
| F1 | TR5 T1A | Littelfuse 0443001.DR, T1A 250 V, 10 x 3 mm (Pads passen auch für Schurter UMT 250) | C95352 |
| RV1 | S07K275 | TDK CU3225K275G2, 275 VAC, 8,0 x 6,3 mm | C211106 |
| PS1 | IRM-02-3.3 | IRM-02-3.3S | C6062464 (am 23.11.2026 Bestand 0) |
| C1 | Elko radial | Elko SMD 100 µF 16 V, 6,3 x 5,4 mm | C970684 |
| C2 | X2 Folie 10 nF | Murata GA355QR7GB103KW01L, 10 nF X2 250 VAC, Bauform 2220 | C237426 |
| J1 | Lochreihe 1,27 mm | SMD-Pads 1,27 mm, unbestückt | – |
| U4 | SHT40-AD1B | SHT40-AD1F-R2 mit Polyimid-Membran (IP68), gleiche Pins, gleicher Footprint, Adresse 0x44 | C7461846 |
| D1, R13–R15 | – | neu: RGB-LED Foshan NationStar FM-B2020RGBA-HG (2,1 x 2,1 mm) mit Vorwiderständen 680 Ω / 220 Ω / 150 Ω | C42421005, C23228, C22962, C22808 |

Die Platine hat keine bedrahteten Bauteile mehr; Bohrungen gibt es nur für Durchkontaktierungen und für die beiden Schraubdome des Gehäuses.

## 4. Anordnung

Die Platine ist so gezeichnet, wie sie eingebaut von vorn zu sehen ist: unten links im Lüfterkasten, vor dem Lüftergehäuse. Alle Bauteile sitzen auf der Oberseite; die Unterseite dient nur als zweite Verdrahtungsebene.

- **Unterer Teil (76 mm breit, bis 43,2 mm Höhe):** ganz links ein 22 mm breiter 3,3-V-Streifen (Programmierpads J1, Stützkondensator), daneben das Netzteil PS1 und die Klemmen X1 mit der Leitereinführung nach rechts. Rechts neben den Klemmen ist die Platine 14 x 30 mm ausgeschnitten: dort liegt der Anschlussraum für die Adern. Über Netzteil und Klemmen die Netzreihe mit Sicherung, Varistor, Snubber und Teilerwiderständen.
- **Isolationsschlitz 2 mm**, nach rechts offen, zwischen Netzreihe und Arm. Die beiden Optokoppler U2 und U3 sitzen darüber: Netzpins unten, 3,3-V-Pins oben.
- **Arm oben (68 x 18 mm):** links das WLAN-Modul U1 mit der Antenne an der Oberkante, daneben C1 und die RGB-LED D1 mit ihren Vorwiderständen, ganz rechts hinter einem Thermoschlitz die Sensorinsel mit U4 und C7. Die Ecke oben rechts ist abgeschrägt und zeigt zum Lüfter-Einlass. Der Arm ist 8 mm schmaler als der untere Teil.
- **Zwei Bohrungen 6,6 mm** (unten links und im Arm) für die Schraubdome des Gehäuses, beide im 3,3-V-Bereich und mehr als 10 mm vom Netzkupfer entfernt.
- **Klemmenbelegung von oben nach unten: L, Lüfter, Licht, N.** Die Beschriftung steht auf der Unterseite, weil das Klemmengehäuse die Oberseite verdeckt, und im Gehäusedeckel.
- **Isolation:** kupferfreie Streifen von 6,3 mm zwischen Netz und 3,3 V (im unteren Teil senkrecht mit Schlitz 2 x 20 mm unter dem Netzteil, darüber waagrecht mit dem durchgehenden Schlitz).
- **Netzseite von Hand geroutet** (1,0 mm; nach den 2 x 100 kΩ 0,4 mm, dort fließt weniger als 2 mA). N, Licht, Lüfter und L laufen auf der Unterseite von den Klemmen nach oben in die Netzreihe. Die **3,3-V-Seite hat der Autorouter Freerouting verlegt**, danach Masseflächen auf beiden Lagen mit Masse-Durchkontaktierungen.
- **RGB-LED D1** (gemeinsame Anode an 3,3 V): rot an GPIO4 über 680 Ω, grün an GPIO5 über 220 Ω, blau an GPIO1 über 150 Ω. Die LED leuchtet bei Pegel 0; beim Start sind die Pins hochohmig, die LED ist aus. Rechnerisch je etwa 2 bis 3 mA; grün und blau werden dunkler, wenn ihre Flussspannung an der oberen Grenze (3,2 V) liegt.

## 5. Dateien

- `kicad/` – Projekt für KiCad 10: Schaltplan, Platine, Regeln (`.kicad_dru`), Symbol- und Footprint-Bibliothek des Projekts
- `bestellpaket/` – Gerber und Bohrdaten (auch als `gerber_lueftersteuerung.zip`), `BOM_JLCPCB.csv`, `CPL_JLCPCB.csv`, Bestückungspläne, `LIESMICH.md`
- `doku/` – Schaltplan als PDF, Bilder der Platine (auch 3D-Ansichten und `platine_3d.glb` zum Drehen), DRC-Bericht
- `gehaeuse/` – Gehäuse für den 3D-Druck: OpenSCAD-Modell, STL für Wanne und Deckel, Bilder
- `skripte/` – erzeugen alles aus dem ursprünglichen Schaltplan neu (`alles.sh`, `bis_sauber.sh`, `export_fab.sh`); laufen in einem KiCad-10-Container
- `eingang/` – die ursprünglich übergebenen Dateien

## 6. Vor der Bestellung zu prüfen

1. **Footprint der WAGO-Klemme.** Padgrößen und Raster stammen aus dem Datenblatt, die Lage der Pads zur Gehäusekante ist aus der Zeichnung abgeleitet. Mit dem CAD-Footprint von WAGO vergleichen.
2. **Drehlage in der JLCPCB-Vorschau.** Die Winkel in `CPL_JLCPCB.csv` sind KiCad-Winkel; JLCPCB dreht einzelne Gehäuse anders. In der Bestückungsvorschau jedes gepolte Bauteil ansehen (U1–U4, C1, D1, PS1, X1A/X1B).
3. **Sensor.** U4 ist der Sensirion SHT40-AD1F-R2 mit Polyimid-Membran, bei JLCPCB unter C7461846 am Lager. Unter C54823945 gibt es eine Fremdmarke (Tokmas), deren Datenblatt keine Membran nennt: nicht verwenden. Die Membran nicht überlackieren.
4. **Lagerbestand bei JLCPCB** (Bauteilsuche am 23.11.2026): alle Teile der Stückliste sind dort gelistet und bis auf das Netzteil am Lager. Das IRM-02-3.3S (C6062464) hatte Bestand 0 und muss vorbestellt oder beigestellt werden; ein anderes SMD-Netzmodul war nicht am Lager, nur bedrahtete wie Hi-Link HLK-PM03 (C209904, 3,3 V/1 A). Knapp ist der AQH3223A mit 7 Stück; Ausweichtyp AQH3213A (C91557, Nullspannungsschalter, Pinbelegung vor dem Tausch prüfen).
5. **Sicherung.** Die 0443001.DR schaltet 50 A bei 250 VAC ab. Wer mehr will: Schurter UMT 250 (200 A) passt auf dieselben Pads.
6. **Antenne.** Die Antenne sitzt an der Oberkante des Arms, gut 25 mm über dem Netzteil; links liegt die Kastenwand, dahinter das Lüftergehäuse. Wie gut das WLAN im Kasten ist, zeigt erst ein Versuch.
7. **Typenschild des KN2:** die elektrischen Daten sind weiter nicht bekannt. Im Kasten liegen flexible Litzen mit Steckverbindern; die Klemmen nehmen feindrähtige Leiter von 0,5 bis 1,5 mm² auf.
8. **Schutzlack.** Die Steuerung sitzt im Lüfterkasten im Strom der Badluft; die Platine sollte lackiert werden (Sensor, Klemmen und Programmierpads aussparen).

## 7. Noch offen

- Firmware (Regellogik siehe erste Übergabe, Abschnitt 7; Lüfter an GPIO10, Licht an GPIO3 low-aktiv, SHT40 an GPIO6/7, Adresse 0x44, RGB-LED low-aktiv an GPIO4 rot / GPIO5 grün / GPIO1 blau)
- Home Assistant vorhanden? (entscheidet über ESPHome oder eigene Firmware)
- Gehäuse: Entwurf für den 3D-Druck in `gehaeuse/`, passend zur Platine v1.3 und zum Einbau unten links vor dem Lüftergehäuse (dort sind etwa 50 mm Tiefe bis zur Frontabdeckung frei, das Gehäuse braucht 23,5 mm). Noch nicht gedruckt; die Lage von Kabeltasche, Wartungsklappe und Einlass ist nur aus Fotos geschätzt. Details in `gehaeuse/README.md`

## 8. Sicherheit

230 V im Feuchtraum: geschlossenes Gehäuse außerhalb des Spritzbereichs, Anschluss durch eine Elektrofachkraft abnehmen lassen. Netzkupfer reicht an der Klemmenseite bis 1 mm an die Platinenkante. Einrohrsystem am gemeinsamen Schacht: Brandschutzklappe nicht verändern.
