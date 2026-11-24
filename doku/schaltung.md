# Schaltung

[← Zur Übersicht](../README.md)

Diese Seite erklärt die Funktionsblöcke der Schaltung, die Pinbelegung des Controllers und warum welche Bauteile gewählt wurden. Den vollständigen Schaltplan gibt es als [PDF](schaltplan.pdf) und im KiCad-Projekt unter [`kicad/`](../kicad).

**Inhalt:** [Funktionsblöcke](#funktionsblöcke) · [GPIO-Belegung](#gpio-belegung) · [Bauteilauswahl](#bauteilauswahl) · [Datenblattprüfung](#datenblattprüfung)

## Funktionsblöcke

| Block | Bauteile | Aufgabe |
|---|---|---|
| **Netzanschluss** | Klemme X1, Sicherung F1 (T1A), Varistor RV1 | Anschluss von L, N, Licht und Lüfter; Absicherung und Überspannungsschutz |
| **Netzteil** | PS1 Hi-Link HLK-PM03, Elko C1 | 3,3 V / 1 A für die gesamte Elektronik |
| **Lüfter schalten** | Optotriac U3 (MOC3052S), Triac Q1 (ACST410-8B), R16, R17, Snubber R5/C2 | schaltet die Phase zum Lüfter, galvanisch getrennt |
| **Lichteingang** | AC-Optokoppler U2 (LTV-814S), R1/R2 (2 x 100 kΩ), optional R12 | meldet „Licht an“ galvanisch getrennt an den Controller |
| **Controller** | U1 ESP32-C3-MINI-1 | Regellogik, WLAN, USB |
| **Sensor** | U4 SHT40-AD1F-R2, C7 | Temperatur und Feuchte über I²C; auf eigener Insel hinter einem Thermoschlitz |
| **Anzeige** | RGB-LED D1, R13–R15 | Zustandsanzeige |
| **USB** | Buchse J2, Regler U5, Diode D2, C8, C9, R18, R19 | Programmieren und Versorgung aus USB ohne Netzspannung |
| **Boot / Reset** | Lötflächen JP1, JP2 | Notfall-Zugang zum Bootloader |

### Lüfter schalten

Der Optotriac U3 zündet den Triac Q1. Ein Pegel *high* an GPIO10 schaltet die LED im Optotriac ein, der Triac leitet, der Lüfter läuft. Der Zündwiderstand R16 (390 Ω) begrenzt den Spitzenstrom durch den Optotriac, R17 (390 Ω) liegt vom Gate nach COM.

Parallel zum Triac liegt ein **Snubber** aus 10 nF (X2) und 100 Ω. Laut ST schaltet der ACST4 induktive Lasten bis 4 A auch ohne Snubber ab. Er ist trotzdem geblieben, als Reserve und gegen Störungen. Wer mehr Kapazität will: Als SMD mit X2-Zulassung gibt es höchstens 56 nF (Murata GA355XR7GB563KW06L, gleicher Footprint).

### Lichteingang

Der AC-Optokoppler LTV-814S hat antiparallele LEDs und reagiert deshalb auf beide Halbwellen. Liegt am Eingang „Licht“ Spannung an, zieht er GPIO3 auf *low*.

R12 wird **nicht bestückt**. Er ist nur nötig, wenn eine Glimmlampe oder LED-Leuchte am Lichtschalter auch im ausgeschalteten Zustand einen kleinen Strom fließen lässt und dadurch „Licht an“ gemeldet wird.

### RGB-LED

Die LED D1 hat eine gemeinsame Anode an 3,3 V und leuchtet, wenn der jeweilige GPIO auf *low* liegt. Beim Start sind die Pins hochohmig, die LED ist also aus.

| Farbe | GPIO | Vorwiderstand |
|---|---|---|
| rot | GPIO4 | 680 Ω |
| grün | GPIO5 | 220 Ω |
| blau | GPIO1 | 150 Ω |

Rechnerisch fließen je etwa 2 bis 3 mA. Grün und blau werden dunkler, wenn ihre Flussspannung an der oberen Grenze (3,2 V) liegt.

### USB

Der ESP32-C3 hat USB eingebaut; D+ und D− der Buchse J2 gehen direkt an GPIO19 und GPIO18. Die 5 V aus USB versorgen die Platine über die Schottky-Diode D2 und den Regler U5 mit 3,3 V. So lässt sich **ohne Netzspannung** programmieren. Die Widerstände R18 und R19 (je 5,1 kΩ) an den CC-Leitungen sorgen dafür, dass USB-C-Netzteile und -Ports 5 V liefern.

Eine ESD-Schutzbeschaltung an den Datenleitungen gibt es nicht.

Wie man programmiert und den Bootloader im Notfall erreicht, steht unter [Aufbau → Firmware aufspielen](aufbau.md#firmware-aufspielen).

## GPIO-Belegung

Pinbelegung des ESP32-C3-MINI-1, Grundlage für die Firmware:

| GPIO | Modul-Pin | Funktion | aktiv bei |
|---|---|---|---|
| GPIO6 | 20 | I²C SDA (SHT40, Adresse 0x44) | – |
| GPIO7 | 21 | I²C SCL (SHT40) | – |
| GPIO3 | 6 | Lichtschalter | *low* = Licht an |
| GPIO10 | 16 | Lüfter ein | *high* |
| GPIO4 | 18 | RGB-LED rot | *low* |
| GPIO5 | 19 | RGB-LED grün | *low* |
| GPIO1 | 13 | RGB-LED blau | *low* |
| GPIO18 | 26 | USB D− | – |
| GPIO19 | 27 | USB D+ | – |
| GPIO9 | 23 | Boot; Pull-up 10 kΩ, Lötflächen JP1 nach Masse | – |
| GPIO2, GPIO8 | 5, 22 | Strapping-Pins, Pull-up 10 kΩ | – |
| EN | 8 | Reset; Pull-up 10 kΩ, 1 µF gegen Masse, Lötflächen JP2 nach Masse | – |
| GPIO20 / GPIO21 | 30 / 31 | RX / TX, nicht herausgeführt | – |

## Bauteilauswahl

Die wichtigsten Bauteile und warum sie gewählt wurden. Die vollständige Stückliste mit allen LCSC-Nummern steht in [`bestellpaket/BOM_JLCPCB.csv`](../bestellpaket/BOM_JLCPCB.csv).

Grundsätze: alles bei JLCPCB lieferbar, möglichst SMD, alles von oben bestückt. **Bedrahtet sind nur Netzteil und Klemme**, weil es bei JLCPCB kein lagerndes SMD-Netzteil gibt.

| Ref | Bauteil | LCSC | Begründung |
|---|---|---|---|
| X1 | Phoenix MKDS 1,5/4-5,08 (1715747), Schraubklemme 4-polig, waagrechte Leitereinführung | C5443561 | bewährte Klemme, 0,14–1,5 mm² |
| F1 | Littelfuse 0443001.DR, T1A 250 V, 10 x 3 mm | C95352 | vom Netzteil-Datenblatt gefordert; Pads passen auch für Schurter UMT 250 |
| RV1 | TDK CU3225K275G2, 275 VAC, 8,0 x 6,3 mm | C211106 | Überspannungsschutz, vom Netzteil-Datenblatt gefordert; festgelegt auf 275 VAC (siehe [Datenblattprüfung](#datenblattprüfung)) |
| PS1 | Hi-Link HLK-PM03, 3,3 V / 1 A, 34,8 x 20,5 x 15 mm, vergossen | C209904 | Mean Well IRM-02-3.3 und -3.3S waren bei JLCPCB nicht lieferbar |
| C1 | Panasonic EEHZK1E101UP, Hybrid-Polymer-Elko 100 µF 25 V, 6,3 x 5,8 mm | C454668 | für feuchte Wärme geprüft (85 °C, 85–90 % r. F., 2000 h unter Spannung), 4000 h bei 125 °C, AEC-Q200 |
| C2 | Murata GA355QR7GB103KW01L, 10 nF X2 250 VAC, Bauform 2220 | C237426 | Snubber-Kondensator mit X2-Zulassung als SMD |
| U1 | Espressif ESP32-C3-MINI-1-H4X | C41349510 | WLAN und USB eingebaut; Variante -H4X, weil -N4 abgekündigt ist (gleicher Footprint) |
| U3 | Lite-On MOC3052S-TA1, Optotriac | C115471 | Markenbauteil, gut lieferbar |
| Q1 | ST ACST410-8BTR, Triac 800 V / 4 A, DPAK | C221462 | überspannungsfest, robust |
| R16, R17 | 390 Ω (1206) und 390 Ω (0603) | C4491, C23151 | Zünd- und Gate-Widerstand |
| U4 | Sensirion SHT40-AD1F-R2 mit Polyimid-Membran (IP68) | C7461846 | Membran schützt vor Staub und Wasser; I²C-Adresse 0x44 |
| D1 | Foshan NationStar FM-B2020RGBA-HG, 2,1 x 2,1 mm | C42421005 | kleine RGB-LED mit gemeinsamer Anode |
| R13–R15 | 680 Ω / 220 Ω / 150 Ω | C23228, C22962, C22808 | LED-Vorwiderstände |
| J2 | GCT USB4145-03-0230-C, USB-C stehend, 7,5 mm hoch, Zapfen 2,3 mm | C5291559 | Programmieren ohne Adapter |
| U5 | Richtek RT9013-33GB, Regler 3,3 V | C47773 | Versorgung aus USB |
| D2 | B5819W, Schottky-Diode | C8598 | Rückstromschutz zur USB-Buchse |
| C8, C9 | 1 µF | C15849 | am Regler U5 |
| R18, R19 | 5,1 kΩ | C23186 | CC-Leitungen der USB-C-Buchse |
| JP1, JP2 | Lötflächen | – | Boot und Reset, kein Bauteil |

> [!NOTE]
> Der erste Entwurf verwendete einen Photo-Triac AQH3223A, bedrahtete Bauteile und eine Programmierleiste statt USB. Wer die Unterschiede nachvollziehen will, findet den alten Stand in der Git-Historie.

## Datenblattprüfung

Alle Pinbelegungen und Grenzwerte wurden gegen die Datenblätter geprüft. Die Spalte „Folge“ zeigt, was daraus für Schaltplan und Footprint folgte.

| Bauteil | Datenblatt | Folge |
|---|---|---|
| ESP32-C3-MINI-1 | alle Annahmen stimmen | Typ auf -H4X geändert (-N4 abgekündigt) |
| SHT40 | Pinbelegung stimmt, I²C-Adresse 0x44 | – |
| LTV-814S | Pinbelegung stimmt; die beiden Eingangspins sind gleichwertig (antiparallele LEDs) | Pins 1 und 2 im Schaltplan getauscht, damit das einseitige Layout ohne Kreuzung auskommt |
| MOC3052S | 1 = Anode, 2 = Kathode, 3 frei, 4 und 6 = Ausgang (gleichwertig), 5 = Substrat (nicht anschließen); 600 V, 5 kV Isolation, **kein** Nullspannungsschalter | Pin 6 ans Gate, Pin 4 über R16 an OUT. Pin 5 auf eigenem, unverbundenem Pad, als Netzpotential behandelt. Footprint SMDIP-6 (Anschlussbreite 10,16 mm) |
| MOC3052S, LED-Strom | Zündstrom max. 10 mA; U<sub>F</sub> typ. 1,15 V, max. 1,5 V | R3 = 100 Ω (statt 150 Ω): rechnerisch 18 bis 21 mA an 3,3 V |
| Zündkreis | Spitzenstrom des Optotriacs max. 1 A | R16 = 390 Ω (1206): höchstens 0,92 A bei 253 V; R17 = 390 Ω vom Gate nach COM |
| ACST410-8B | 1 = COM, Kühlfahne = OUT, 3 = G; 800 V, 4 A (1 A bei 60 °C mit 0,5 cm² Kupfer); I<sub>GT</sub> max. 10 mA (Quadranten I–III), I<sub>H</sub> max. 20 mA; klemmt Überspannung bei 850 V | COM an L hinter der Sicherung, OUT zur Klemme „Lüfter“. Footprint nach ST-Datenblatt (Fahne 6,7 x 6,7 mm, 3,0 mm Abstand zu den Anschlussflächen) |
| RT9013-33GB (SOT-23-5) | 1 = VIN, 2 = GND, 3 = EN, 4 frei, 5 = VOUT; Eingang max. 5,5 V, 500 mA, Dropout typ. 0,25 V | EN an VIN; Eingang über D2 an VBUS, Ausgang direkt an 3,3 V |
| USB4145-03-0230-C | A1/A12/B1/B12 = GND, A4/A9/B4/B9 = VBUS, A5 = CC1, B5 = CC2, A6/B6 = D+, A7/B7 = D−, A8/B8 = SBU; Lötflächen 0,30 x 1,15 mm im Raster 0,5 mm; vier Gehäusezapfen 2,3 mm lang in metallisierten Langlöchern 1,10 x 0,60 mm | eigener Footprint nach dem Lötbild im Datenblatt; D+ an GPIO19, D− an GPIO18 (im ESP32-C3 fest so belegt) |
| HLK-PM03, Pins | 1 und 2 = AC (gleichwertig), 3 = −Vo, 4 = +Vo; AC-Stifte 5,0 mm, Ausgangsstifte 15,0 mm auseinander, Reihenabstand 29,08 mm, Stifte 0,8 mm | KiCad-Footprint `Converter_ACDC_Hi-Link_HLK-PMxx` passt. Im Schaltplan AC/N = 1, AC/L = 2 |
| HLK-PM03, Beschaltung | Sicherung 1 A träge und Varistor am Eingang gefordert; X-Kondensator und Drossel nur für die EMV-Zulassung | F1 (T1A) und RV1 vorhanden. Das Datenblatt nennt als Beispiel 10D561K (350 VAC); **festgelegt ist der verbaute Typ CU3225K275G2 mit 275 VAC** |
| MKDS 1,5/4-5,08 | Raster 5,08 mm, Stifte 1,0 mm (Bohrung 1,3 mm), Stiftreihe 4,6 mm hinter der Leitereinführung, 250 V / 17,5 A, 0,14–1,5 mm² | Footprint vom KiCad-Original abgeleitet, Lötaugen 2,4 statt 2,6 mm (2,68 mm Kupferabstand zwischen den Polen) |
| FM-B2020RGBA-HG | gemeinsame Anode an Pin 3; Pin 1 rot (Eckmarke), Pin 4 grün, Pin 2 blau; U<sub>F</sub> typ. 2,0 / 2,7 / 2,8 V | eigener Footprint nach Datenblatt (Pads 0,8 x 0,7 mm) |
