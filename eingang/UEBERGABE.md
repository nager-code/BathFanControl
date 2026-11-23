# Übergabe: Lüftersteuerung Bad (KN2 UP) – Stand 23.11.2026

Dieses Dokument enthält alles, um das Projekt in einem neuen Chat oder mit einer anderen Person fortzusetzen. Die Dateien im ZIP gehören dazu.

## 1. Aufgabe

Eigene Steuerung für einen Badlüfter, die den Lüfter feuchteabhängig schaltet und nicht stundenlang nutzlos läuft.

- Versorgung 230 V, zweiter 230-V-Eingang vom Lichtschalter (zeigt Aktivität im Bad)
- Luftfeuchte messen und Lüfter danach schalten
- Fortschritt messen: Sinkt die Feuchte nicht (feuchte Wohnungs- oder Außenluft), längere Pause einlegen. Die alte Steuerung lief teils 8 Stunden durch.
- Licht 10 Minuten an und noch kein Feuchteanstieg: Lüfter kurz einschalten, weil der Sensor in einer Raumecke sitzt und die Feuchte dort spät ankommt
- Über WLAN erreichbar
- Möglichst wenig Stromverbrauch
- Platine maximal 70 x 30 mm

## 2. Lüfter

- Typ: KN2 UP Ventilator (Unterputz, Einrohrlüftungs-System, Baureihe KN), Anleitung: https://de.ventilatory.net/media/catalog/product/data/ds-kn2-de.pdf
- Motor ca. 50 W, keine Grundlüftung ab Werk, also ein Schaltkanal
- Laut Anleitung zerstört falsche Beschaltung die Elektronik im Gerät. Die Steuerung schaltet deshalb nur die Phase vor dem Ventilator.
- Elektrische Daten stehen nur auf dem Typenschild, das liegt noch nicht vor.

## 3. Schaltungskonzept

- Netzteil: Mean Well IRM-02-3.3 (230 V auf 3,3 V, 600 mA), davor Sicherung T1A und Varistor 275 V
- Controller: ESP32-C3-MINI-1
- Sensor: SHT40 (I2C), thermisch durch Frässchlitz entkoppelt
- Lichtschalter-Eingang: AC-Optokoppler LTV-814S, 2 x 100 k in Serie, Ausgang mit 220 k Pull-up und 470 n Filter (low = Licht an). R12 (3k3) parallel zum Optokoppler-Eingang nur bei Fehlauslösung durch Glimmlampe oder LED-Leuchte bestücken.
- Lüfter-Ausgang: Photo-Triac Panasonic AQH3223A (1,2 A, schaltet nicht im Nulldurchgang, JLCPCB C719698), LED über 150 R an GPIO10, Snubber 100 R + 10 n X2 über dem Triac
- Erwarteter Eigenverbrauch ca. 0,2 bis 0,3 W (WLAN Power-Save, Light-Sleep, Messung alle 30 s)

### GPIO-Belegung ESP32-C3

| GPIO | Modul-Pin | Funktion |
|---|---|---|
| GPIO6 | 20 | SDA (SHT40) |
| GPIO7 | 21 | SCL (SHT40) |
| GPIO3 | 6 | Lichtschalter, low = Licht an |
| GPIO10 | 16 | Lüfter ein (high) |
| GPIO20 / GPIO21 | 30 / 31 | RX / TX (Programmierung) |
| GPIO9 | 23 | Boot, Pull-up 10 k |
| GPIO2, GPIO8 | 5, 22 | Strapping, Pull-up 10 k |
| EN | 8 | Pull-up 10 k, 1 u gegen GND |

## 4. Stückliste

| Ref | Wert | Footprint (KiCad) | Hinweis |
|---|---|---|---|
| X1 | L / N / L-Licht / L-Luefter | TerminalBlock_Phoenix:TerminalBlock_Phoenix_MKDS-1,5-4-5.08_1x04_P5.08mm_Horizontal | Klemme 4-polig 5,08 mm |
| F1 | T1A 250V | Fuse:Fuse_Littelfuse_395Series | Sicherung traege, TR5 radial |
| RV1 | S07K275 | Varistor:RV_Disc_D7mm_W3.4mm_P5mm | Varistor 275 VAC |
| PS1 | IRM-02-3.3 | Converter_ACDC:Converter_ACDC_MeanWell_IRM-02-xx_THT | Mean Well, 230 V -> 3,3 V / 600 mA |
| U1 | ESP32-C3-MINI-1 | RF_Module:ESP32-C3-MINI-1 | WLAN-Modul; Pinnummern gegen Datenblatt pruefen |
| U2 | LTV-814S | Package_DIP:SMDIP-4_W9.53mm | AC-Optokoppler, Unterseite |
| U3 | AQH3223A | Package_DIP:SMDIP-8_W9.53mm | Photo-Triac 1,2 A (schaltet nicht im Nulldurchgang); Pad 7 entfaellt; Pinbelegung gegen Datenblatt pruefen; Unterseite |
| U4 | SHT40-AD1B | Sensor_Humidity:Sensirion_DFN-4_1.5x1.5mm_P0.8mm_SHT4x_NoCentralPad | Feuchte/Temperatur, I2C |
| J1 | Prog 3V3 GND TX RX IO9 EN | Connector_PinHeader_1.27mm:PinHeader_1x06_P1.27mm_Vertical | Programmierpads Raster 1,27 mm, unbestueckt |
| R1 | 100k | Resistor_SMD:R_1206_3216Metric | Lichteingang, 200 V Typ |
| R2 | 100k | Resistor_SMD:R_1206_3216Metric | Lichteingang, 200 V Typ |
| R3 | 150R | Resistor_SMD:R_0603_1608Metric | LED-Vorwiderstand Triac, ca. 14 mA |
| R4 | 220k | Resistor_SMD:R_0603_1608Metric | Pull-up Lichtsignal |
| R5 | 100R | Resistor_SMD:R_1206_3216Metric | Snubber, impulsfest |
| R6 | 10k | Resistor_SMD:R_0603_1608Metric | EN Pull-up |
| R7 | 10k | Resistor_SMD:R_0603_1608Metric | IO9 Pull-up (Boot) |
| R8 | 10k | Resistor_SMD:R_0603_1608Metric | IO8 Pull-up (Strapping) |
| R9 | 10k | Resistor_SMD:R_0603_1608Metric | IO2 Pull-up (Strapping) |
| R10 | 10k | Resistor_SMD:R_0603_1608Metric | SDA Pull-up |
| R11 | 10k | Resistor_SMD:R_0603_1608Metric | SCL Pull-up |
| R12 | 3k3 DNP | Resistor_SMD:R_0603_1608Metric | Option gegen Glimmlampen-/LED-Leckstrom, nur bei Bedarf bestuecken |
| C1 | 100u 10V | Capacitor_THT:CP_Radial_D5.0mm_P2.00mm | Puffer WLAN-Spitzen |
| C2 | 10n X2 275VAC | Capacitor_THT:C_Rect_L13.0mm_W5.0mm_P10.00mm_FKS3_FKP3_MKS4 | Snubber |
| C3 | 470n | Capacitor_SMD:C_0603_1608Metric | Filter Lichtsignal (ca. 100 ms) |
| C4 | 10u | Capacitor_SMD:C_0805_2012Metric | nahe U1 |
| C5 | 100n | Capacitor_SMD:C_0603_1608Metric | nahe U1 |
| C6 | 1u | Capacitor_SMD:C_0603_1608Metric | EN Verzoegerung |
| C7 | 100n | Capacitor_SMD:C_0603_1608Metric | nahe U4 |

## 5. Netzliste

Schreibweise: Bauteil.Pin

- **L**: X1.1, F1.1
- **L_F**: F1.2, RV1.1, PS1.1, U3.6, R5.1
- **N**: X1.2, RV1.2, PS1.2, U2.2, R12.2
- **L_LICHT**: X1.3, R1.1
- **LICHT_A**: R1.2, R2.1
- **LICHT_B**: R2.2, U2.1, R12.1
- **L_FAN**: X1.4, U3.8, C2.2
- **SNUB**: R5.2, C2.1
- **+3V3**: PS1.4, C1.1, C4.1, C5.1, U1.3, R4.1, R6.1, R7.1, R8.1, R9.1, R10.1, R11.1, U4.3, C7.1, J1.1
- **GND**: PS1.3, C1.2, C4.2, C5.2, C3.2, C6.2, C7.2, U2.3, U3.3, U4.4, J1.2, U1.1, U1.2, U1.11, U1.14, U1.36, U1.37, U1.38, U1.39, U1.40, U1.41, U1.42, U1.43, U1.44, U1.45, U1.46, U1.47, U1.48, U1.49, U1.50, U1.51, U1.52, U1.53
- **EN**: U1.8, R6.2, C6.1, J1.6
- **BOOT_IO9**: U1.23, R7.2, J1.5
- **IO8**: U1.22, R8.2
- **IO2**: U1.5, R9.2
- **SDA_IO6**: U1.20, R10.2, U4.1
- **SCL_IO7**: U1.21, R11.2, U4.2
- **LICHT_N_IO3**: U1.6, U2.4, R4.2, C3.1
- **FAN_EN_IO10**: U1.16, R3.1
- **FAN_LED**: R3.2, U3.2
- **TXD**: U1.31, J1.3
- **RXD**: U1.30, J1.4

Nicht angeschlossen: U1 Pins 4, 7, 9, 10, 12, 13, 15, 17, 18, 19, 24–29, 32–35; U3 Pins 1, 4, 5 (Pin 7 existiert nicht).

Angenommene Pinbelegungen, gegen Datenblatt zu prüfen:
- AQH3223A: 2 Anode, 3 Kathode, 6 und 8 Lastanschlüsse, 1/4/5 frei
- LTV-814S: 1 und 2 AC-Eingang, 3 Emitter, 4 Kollektor
- IRM-02-3.3: 1 AC/L, 2 AC/N, 3 -Vo, 4 +Vo
- SHT40: 1 SDA, 2 SCL, 3 VDD, 4 VSS
- ESP32-C3-MINI-1: GND an 1, 2, 11, 14, 36–53; 3 = 3V3

## 6. Platzierung (70 x 30 mm)

Ursprung linke obere Ecke, x nach rechts, y nach unten, Maße in mm, Position = Bauteilmitte (Richtwert).

| Ref | x | y | Drehung | Seite |
|---|---|---|---|---|
| X1 | 4.5 | 15.0 | 270° | oben |
| F1 | 15.0 | 5.5 | 0° | oben |
| RV1 | 15.0 | 14.5 | 0° | oben |
| R1 | 12.5 | 20.5 | 0° | oben |
| R2 | 17.5 | 20.5 | 0° | oben |
| R12 | 15.0 | 24.0 | 0° | unten |
| PS1 | 38.0 | 11.5 | 0° | oben |
| C2 | 28.5 | 26.5 | 0° | oben |
| R5 | 15.0 | 27.0 | 0° | oben |
| C1 | 50.0 | 26.5 | 0° | oben |
| U3 | 38.0 | 7.0 | 0° | unten |
| U2 | 38.0 | 17.5 | 180° | unten |
| R3 | 47.0 | 5.0 | 90° | unten |
| R4 | 47.0 | 16.0 | 90° | unten |
| C3 | 50.0 | 16.0 | 90° | unten |
| U1 | 62.6 | 8.8 | 0° | oben |
| C4 | 58.0 | 19.5 | 0° | oben |
| C5 | 62.0 | 19.5 | 0° | oben |
| R6 | 57.0 | 8.0 | 90° | unten |
| C6 | 59.5 | 8.0 | 90° | unten |
| R7 | 62.0 | 12.0 | 90° | unten |
| R8 | 64.5 | 12.0 | 90° | unten |
| R9 | 67.0 | 12.0 | 90° | unten |
| J1 | 58.5 | 25.0 | 90° | oben |
| U4 | 67.0 | 27.0 | 0° | oben |
| C7 | 67.0 | 24.0 | 0° | oben |
| R10 | 57.0 | 17.0 | 0° | unten |
| R11 | 57.0 | 19.5 | 0° | unten |

Layoutregeln:
- 2 Lagen, FR4 1,6 mm, 35 µm Kupfer
- Netzseite links (x < 38), 3,3-V-Seite rechts (x > 44,4). Dazwischen 6,4 mm ohne Kupfer auf beiden Lagen.
- U2 und U3 sitzen unten unter dem Netzteil auf der Trennlinie x = 38, Netzpins links, Kleinspannungspins rechts. Zwischen den Pinreihen ein Frässchlitz.
- Netzleiterbahnen mindestens 1 mm breit, L zu N mindestens 2,5 mm Abstand
- Massefläche nur auf der 3,3-V-Seite, kein Kupfer unter der Antenne von U1 (oberste 5 mm des Moduls)
- Thermoschlitz um den Sensor: senkrecht bei x = 62 von y = 30 bis 21, waagrecht bei y = 21 von x = 62 bis 66, rechts ein Steg
- Engste Stelle: zwischen U1 und rechtem Platinenrand knapp 1 mm
- Bauhöhe ca. 21 mm

## 7. Regellogik (Firmware, noch nicht geschrieben)

Gerechnet wird mit absoluter Feuchte (g/m³ aus Temperatur und relativer Feuchte). Ein langsamer Mittelwert über Stunden bildet die Basis.

1. Bereit: Messung alle 30 s.
2. Start: schneller Anstieg (z. B. +5 % rF in 5 min) oder Basis +10 %.
3. Lüften mit Fortschrittskontrolle: alle 10 bis 15 min muss die Feuchte um z. B. 2 bis 3 % rF fallen. Ziel Basis +3 %, danach 5 min Nachlauf.
4. Kein Fortschritt nach zwei Fenstern: Pause 1 h, bei Wiederholung 2 h, dann 4 h. Basis auf den aktuellen Wert nachziehen. Harte Obergrenze 45 bis 60 min Laufzeit.
5. Aktivität: Licht 10 min an ohne Anstieg, dann 2 bis 3 min Probelauf. Steigt die Feuchte dabei, weiter mit Schritt 3. Nächster Probelauf frühestens nach 15 bis 20 min.

WLAN: vorgeschlagen ESPHome (Home Assistant, OTA, Weboberfläche), alternativ eigene Firmware mit MQTT/REST. Schwellwerte, Pausenzeiten und manuelles Ein/Aus einstellbar. Ob Home Assistant vorhanden ist, ist noch offen.

## 8. Stand

Vorhanden (im ZIP):
- `schaltplan.pdf` – Schaltplan zum Ansehen (Verbindungen über Netznamen)
- `lueftersteuerung.kicad_sch` – Schaltplan für KiCad 8
- `lueftersteuerung.net` – Netzliste für den KiCad-Platineneditor
- `stueckliste.csv` – Stückliste
- `platzierung.py` – Skript für die KiCad-Skripting-Konsole (Umriss, Grobplatzierung, Hilfslinien)
- `platine_bestueckung.png` – Bild der Bestückung, Ober- und Unterseite

Nicht geprüft:
- Keine der KiCad-Dateien wurde in KiCad geöffnet (nur rechnerische Konsistenzprüfung der Netze).
- Footprint-Namen und Pinbelegungen stammen aus dem Gedächtnis, siehe Abschnitt 5.
- Bauteilmaße in der Platzierung sind Näherungen.

Fehlt noch:
- Geroutetes Layout und Design-Rule-Check
- Fertigungsdaten zum Bestellen einer bestückten Platine: Gerber, Bohrdatei, Stückliste und Bestückungsdatei im Format des Fertigers
- Firmware

## 9. Offene Fragen

1. Bei welchem Fertiger wird bestellt (z. B. JLCPCB)? Davon hängen Dateiformate und Bauteilnummern ab.
2. Sollen die Durchsteckteile (PS1, X1, F1, RV1, C1, C2) mitbestückt werden oder werden sie selbst gelötet?
3. Typenschild und Anschlussklemme des KN2 (Foto) zur Kontrolle der Klemmenbelegung
4. Home Assistant vorhanden?

## 10. Sicherheit

230 V im Feuchtraum: geschlossenes Gehäuse außerhalb des Spritzbereichs, Anschluss durch eine Elektrofachkraft abnehmen lassen. Einrohrsystem am gemeinsamen Schacht: Brandschutzklappe nicht verändern, im Zweifel Hausverwaltung fragen.

## 11. Auftrag für die Fortsetzung

Erstelle aus Schaltplan, Netzliste und Platzierung ein geroutetes zweilagiges Layout (70 x 30 mm) nach den Layoutregeln in Abschnitt 6, prüfe die Pinbelegungen aus Abschnitt 5 gegen die Datenblätter und liefere ein Bestellpaket für eine bestückte Platine (Gerber, Bohrdatei, Stückliste, Bestückungsdatei).
