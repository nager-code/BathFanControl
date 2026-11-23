# Bestellpaket Lüftersteuerung Bad v1.2

## Leiterplatte
- `gerber_lueftersteuerung.zip` hochladen (Inhalt liegt auch entpackt in `gerber/`)
- 2 Lagen, Umriss 68 x 58 mm (keine Rechteckform: Riegel und Arm mit Spalt dazwischen), FR4 1,6 mm, 35 µm Kupfer
- Kleinste Leiterbahn 0,2 mm, kleinster Abstand 0,2 mm, kleinste Bohrung 0,3 mm (Durchkontaktierung 0,6 mm)
- Fräsungen: Isolationsschlitz 2 x 20 mm innerhalb der Kontur, Thermoschlitz 1 mm und der 10 mm breite Spalt zwischen Riegel und Arm als Teil der Außenkontur

## Bestückung
- Beidseitig, nur SMD
- `BOM_JLCPCB.csv` – Stückliste mit LCSC-Nummern
- `CPL_JLCPCB.csv` – Bestückungsdatei (Koordinaten passend zu den Gerberdaten)
- `bestueckung_oben.pdf`, `bestueckung_unten.pdf` – Bestückungspläne
- `nicht_bestueckt.csv` – R12 (nur bei Fehlauslösung durch Glimmlampe/LED-Leuchte) und J1 (Programmierpads)

## Besonderheiten
- X1 besteht aus zwei 2-poligen Klemmen WAGO 2061-602; in Stückliste und Bestückungsdatei heißen sie X1A und X1B.
- PS1 (Mean Well IRM-02-3.3S) ist bei LCSC/JLCPCB nicht gelistet: beistellen oder von Hand löten. Ohne LCSC-Nummer überspringt JLCPCB die Position.
- Drehlage aller gepolten Bauteile in der Bestückungsvorschau prüfen.
- Lagerbestand der „Extended“-Teile prüfen, vor allem AQH3223A (C719698).
- U4 (Sensirion SHT40-AD1F-R2, Sensor mit Membran) hat keine LCSC-Nummer: beistellen. Bei LCSC gibt es unter C54823945 nur eine Fremdmarke.
