# Bestellpaket Lüftersteuerung Bad v1.3

## Leiterplatte
- `gerber_lueftersteuerung.zip` hochladen (Inhalt liegt auch entpackt in `gerber/`)
- 2 Lagen, Umriss 76 x 63 mm (keine Rechteckform: unten rechts ein Ausschnitt 14 x 30 mm, oben rechts 8 mm schmaler, dazwischen ein nach rechts offener Schlitz), FR4 1,6 mm, 35 µm Kupfer
- Kleinste Leiterbahn 0,2 mm, kleinster Abstand 0,2 mm, kleinste Bohrung 0,3 mm (Durchkontaktierung 0,6 mm)
- Fräsungen: Isolationsschlitz 2 x 20 mm unter dem Netzteil und zwei Bohrungen 6,6 mm (ohne Kupfer) innerhalb der Kontur; der 2 mm breite Isolationsschlitz unter den Optokopplern und der Thermoschlitz 1 mm sind Teil der Außenkontur

## Bestückung
- Einseitig (nur Oberseite), nur SMD
- `BOM_JLCPCB.csv` – Stückliste mit LCSC-Nummern
- `CPL_JLCPCB.csv` – Bestückungsdatei (Koordinaten passend zu den Gerberdaten)
- `bestueckung_oben.pdf` – Bestückungsplan; `bestueckung_unten.pdf` zeigt nur die Beschriftung der Unterseite
- `nicht_bestueckt.csv` – R12 (nur bei Fehlauslösung durch Glimmlampe/LED-Leuchte) und J1 (Programmierpads)

## Besonderheiten
- X1 besteht aus zwei 2-poligen Klemmen WAGO 2061-602; in Stückliste und Bestückungsdatei heißen sie X1A und X1B.
- PS1 (Mean Well IRM-02-3.3S) ist bei LCSC/JLCPCB nicht gelistet: beistellen oder von Hand löten. Ohne LCSC-Nummer überspringt JLCPCB die Position.
- Drehlage aller gepolten Bauteile in der Bestückungsvorschau prüfen. Bei der RGB-LED D1 liegt die Eckmarke (Pin 1, rot) unten rechts, wenn die Klemmen rechts unten liegen.
- Lagerbestand der „Extended“-Teile prüfen, vor allem AQH3223A (C719698).
- U4 (Sensirion SHT40-AD1F-R2, Sensor mit Membran) hat keine LCSC-Nummer: beistellen. Bei LCSC gibt es unter C54823945 nur eine Fremdmarke.
