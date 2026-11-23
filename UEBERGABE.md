# Übergabe: Lüftersteuerung Bad (KN2 UP) – Stand 23.11.2026, Platine v1.2 (nur SMD, Form für den Lüfterkasten)

Fortsetzung der Übergabe vom selben Tag. Neu: Pinbelegungen gegen Datenblätter geprüft, Umstellung auf KiCad 10 und auf ausschließlich SMD-Bauteile, Platinenform und Gehäuse für den Einbau unten links im Lüfterkasten, geroutetes Layout, Bestellpaket.

## 1. Ergebnis

| | |
|---|---|
| Platine | Umriss 68 x 58 mm (Riegel unten 54 x 30 mm, Arm oben 68 x 18 mm, links verbunden), 2 Lagen, FR4 1,6 mm, 35 µm, beidseitig bestückt |
| KiCad | 10.0.8, Projekt in `kicad/` |
| Schaltplanprüfung (ERC) | 0 Meldungen |
| Regelprüfung (DRC) mit Schaltplanabgleich | 0 Verletzungen, 0 offene Verbindungen, Bericht in `doku/drc_bericht.txt` |
| Kleinster Abstand zwischen Netzpotentialen | 2,77 mm (Regel 2,5 mm) |
| Kleinster Abstand Netz zu 3,3 V | 6,4 mm (Regel 6 mm), dazu 2 mm breiter Frässchlitz unter U2/U3 und ein 10 mm breiter Spalt zwischen Riegel und Arm |
| Bauhöhe | ca. 22 mm (Netzteil 16 mm oben, Varistor 4,5 mm unten) |
| Gehäuse | 72,6 x 62,6 x 28 mm, Entwurf für den 3D-Druck in `gehaeuse/` |

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

Hinweis zum Snubber: Panasonic nennt allgemein 0,1 µF und 20–100 Ω. Geblieben sind 10 nF und 100 Ω wie in der ersten Übergabe; als SMD mit X2-Zulassung gibt es höchstens 56 nF (Murata GA355XR7GB563KW06L, gleicher Footprint).

## 3. Umstellung auf SMD und Sensor mit Membran

| Ref | vorher | jetzt | JLCPCB/LCSC |
|---|---|---|---|
| X1 | Phoenix MKDS 4-polig | 2 x WAGO 2061-602/998-404 (je 2-polig, Raster 6 mm, 0,5–1,5 mm², 250 V/17,5 A) | C2765058 |
| F1 | TR5 T1A | Littelfuse 0443001.DR, T1A 250 V, 10 x 3 mm (Pads passen auch für Schurter UMT 250) | C95352 |
| RV1 | S07K275 | TDK CU3225K275G2, 275 VAC, 8,0 x 6,3 mm | C211106 |
| PS1 | IRM-02-3.3 | IRM-02-3.3S | nicht gelistet |
| C1 | Elko radial | Elko SMD 100 µF 16 V, 6,3 x 5,4 mm | C970684 |
| C2 | X2 Folie 10 nF | Murata GA355QR7GB103KW01L, 10 nF X2 250 VAC, Bauform 2220 | C237426 |
| J1 | Lochreihe 1,27 mm | SMD-Pads 1,27 mm, unbestückt | – |
| U4 | SHT40-AD1B | SHT40-AD1F-R2 mit Polyimid-Membran (IP68), gleiche Pins, gleicher Footprint, Adresse 0x44 | Original nicht gelistet |

Die Platine hat jetzt keine bedrahteten Bauteile mehr; Bohrungen gibt es nur noch für Durchkontaktierungen.

## 4. Anordnung

Die Platine ist so gezeichnet, wie sie eingebaut von vorn zu sehen ist: unten links im Lüfterkasten, vor dem Lüftergehäuse.

- **Riegel unten (54 x 30 mm):** links das Netzteil PS1, rechts die Klemmen X1 mit der Leitereinführung nach rechts. Auf der Unterseite Sicherung, Varistor, Teilerwiderstände, Snubber und beide Optokoppler über dem Isolationsschlitz.
- **Arm oben (68 x 18 mm):** links das WLAN-Modul U1 mit der Antenne an der Oberkante, daneben C1, ganz rechts hinter einem Thermoschlitz die Sensorinsel mit U4 und C7. Die Ecke oben rechts ist abgeschrägt und zeigt zum Lüfter-Einlass.
- **Dazwischen 10 mm Spalt**, nach rechts offen; verbunden sind Riegel und Arm nur links über einen 14 mm breiten Steg (3,3-V-Seite). Der Sensor ist damit 40 mm vom Netzteil entfernt und thermisch entkoppelt.
- **Klemmenbelegung von oben nach unten: L, Lüfter, Licht, N.** Die Beschriftung steht auf der Unterseite, weil das Klemmengehäuse die Oberseite verdeckt, und im Gehäusedeckel.
- **Isolation:** im Riegel ein kupferfreier Streifen von 6,3 mm mit Schlitz 2 x 20 mm unter den Optokopplern; der Arm ist vom Netzteil des Riegels durch den Spalt getrennt.
- **Netzseite von Hand geroutet** (1,0 mm; nach den 2 x 100 kΩ 0,4 mm, dort fließt weniger als 2 mA). Die **3,3-V-Seite hat der Autorouter Freerouting verlegt**, danach Masseflächen auf beiden Lagen mit Masse-Durchkontaktierungen.

## 5. Dateien

- `kicad/` – Projekt für KiCad 10: Schaltplan, Platine, Regeln (`.kicad_dru`), Symbol- und Footprint-Bibliothek des Projekts
- `bestellpaket/` – Gerber und Bohrdaten (auch als `gerber_lueftersteuerung.zip`), `BOM_JLCPCB.csv`, `CPL_JLCPCB.csv`, Bestückungspläne, `LIESMICH.md`
- `doku/` – Schaltplan als PDF, Bilder der Platine (auch 3D-Ansichten und `platine_3d.glb` zum Drehen), DRC-Bericht
- `gehaeuse/` – Gehäuse für den 3D-Druck: OpenSCAD-Modell, STL für Wanne und Deckel, Bilder
- `skripte/` – erzeugen alles aus dem ursprünglichen Schaltplan neu (`alles.sh`, `bis_sauber.sh`, `export_fab.sh`); laufen in einem KiCad-10-Container
- `eingang/` – die ursprünglich übergebenen Dateien

## 6. Vor der Bestellung zu prüfen

1. **Footprint der WAGO-Klemme.** Padgrößen und Raster stammen aus dem Datenblatt, die Lage der Pads zur Gehäusekante ist aus der Zeichnung abgeleitet. Mit dem CAD-Footprint von WAGO vergleichen.
2. **Drehlage in der JLCPCB-Vorschau.** Die Winkel in `CPL_JLCPCB.csv` sind KiCad-Winkel; JLCPCB dreht einzelne Gehäuse anders. In der Bestückungsvorschau jedes gepolte Bauteil ansehen (U1–U4, C1, PS1, X1A/X1B).
3. **Sensor.** Der SHT40-AD1F-R2 (Sensirion-Bestellnummer 3.000.820) war bei LCSC nur als Fremdmarke zu finden (Tokmas, C54823945); das Original beistellen. Die Membran nicht überlackieren.
4. **Lagerbestand.** AQH3223A hatte bei LCSC Bestand 0, IRM-02-3.3S ist dort nicht gelistet (beistellen oder von Hand löten), der Bestand von JLCPCB selbst war nicht abrufbar.
5. **Sicherung.** Die 0443001.DR schaltet 50 A bei 250 VAC ab. Wer mehr will: Schurter UMT 250 (200 A) passt auf dieselben Pads.
6. **Antenne.** Die Antenne sitzt an der Oberkante des Arms, gut 15 mm über dem Netzteil; links liegt die Kastenwand, dahinter das Lüftergehäuse. Wie gut das WLAN im Kasten ist, zeigt erst ein Versuch.
7. **Typenschild des KN2:** die elektrischen Daten sind weiter nicht bekannt. Im Kasten liegen flexible Litzen mit Steckverbindern; die Klemmen nehmen feindrähtige Leiter von 0,5 bis 1,5 mm² auf.
8. **Schutzlack.** Die Steuerung sitzt im Lüfterkasten im Strom der Badluft; die Platine sollte lackiert werden (Sensor, Klemmen und Programmierpads aussparen).

## 7. Noch offen

- Firmware (Regellogik siehe erste Übergabe, Abschnitt 7; Lüfter an GPIO10, Licht an GPIO3 low-aktiv, SHT40 an GPIO6/7, Adresse 0x44)
- Home Assistant vorhanden? (entscheidet über ESPHome oder eigene Firmware)
- Gehäuse: Entwurf für den 3D-Druck in `gehaeuse/`, passend zur Platine v1.2 und zum Einbau unten links vor dem Lüftergehäuse (dort sind etwa 50 mm Tiefe bis zur Frontabdeckung frei, das Gehäuse braucht 28 mm). Noch nicht gedruckt; die Lage von Kabeltasche, Wartungsklappe und Einlass ist nur aus Fotos geschätzt. Details in `gehaeuse/README.md`

## 8. Sicherheit

230 V im Feuchtraum: geschlossenes Gehäuse außerhalb des Spritzbereichs, Anschluss durch eine Elektrofachkraft abnehmen lassen. Netzkupfer reicht an der Klemmenseite bis 1 mm an die Platinenkante. Einrohrsystem am gemeinsamen Schacht: Brandschutzklappe nicht verändern.
