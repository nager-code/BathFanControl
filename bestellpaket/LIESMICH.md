# Bestellpaket – Lüftersteuerung Bad V1.0

[← Zur Übersicht](../README.md)

Fertigungsdaten für Leiterplatte und Bestückung bei **JLCPCB**. Vor der Bestellung die [Checkliste](../doku/bestellen.md) abarbeiten.

## Dateien

| Datei | Wofür |
|---|---|
| `gerber_lueftersteuerung.zip` | **beim Leiterplatten-Auftrag hochladen** (gleicher Inhalt entpackt in `gerber/`) |
| `BOM_JLCPCB.csv` | Stückliste mit LCSC-Nummern – beim Bestückungsauftrag hochladen |
| `CPL_JLCPCB.csv` | Bestückungsdatei (Koordinaten passend zu den Gerberdaten) – beim Bestückungsauftrag hochladen |
| `nicht_bestueckt.csv` | Teile, die nicht bestückt werden: R12 (nur bei Fehlauslösung durch Glimmlampe/LED-Leuchte), JP1 und JP2 (Lötflächen für Boot und Reset, kein Bauteil) |
| `bestueckung_oben.pdf` | Bestückungsplan |
| `bestueckung_unten.pdf` | zeigt nur die Beschriftung der Unterseite |

Auf der Platine selbst stehen nur die Namen der größeren Bauteile und die Klemmenbelegung. Eine beschriftete Übersicht ist der [Lageplan](../doku/lageplan.png).

## Angaben für den Leiterplatten-Auftrag

| | |
|---|---|
| Lagen | 2 |
| Material | FR4, 1,6 mm, 35 µm Kupfer |
| Umriss | 68 x 72,5 mm, **keine Rechteckform**: unten rechts ein Ausschnitt 13,4 x 34,5 mm, darüber ein nach rechts offener Schlitz, oben rechts eine abgeschrägte Ecke |
| Kleinste Leiterbahn / Abstand | 0,2 mm / 0,2 mm |
| Kleinste Bohrung | 0,3 mm (Durchkontaktierung 0,6 mm) |
| Bestückungsdruck | beide Seiten, kleinste Schrift 1,0 mm hoch, 0,15 mm Strichstärke |

**Bohrungen:**

- Bedrahtete Bauteile, durchkontaktiert: 4 x 1,3 mm (Klemme) und 4 x 1,0 mm (Netzteil).
- USB-Buchse: vier metallisierte Langlöcher 1,10 x 0,60 mm und zwei Führungslöcher ohne Kupfer (rund 0,71 mm, Langloch 1,01 x 0,71 mm).

**Fräsungen:**

- Innerhalb der Kontur: Isolationsschlitz 2 x 20 mm unter dem Netzteil und zwei Bohrungen 6,6 mm (ohne Kupfer).
- Teil der Außenkontur: der 2 mm breite Isolationsschlitz unter den Optokopplern und der 1 mm breite Thermoschlitz.

## Angaben für den Bestückungsauftrag

- **Alles von oben:** 38 SMD-Bauteile und zwei bedrahtete Teile (Klemme X1, Netzteil PS1).
- **Bedrahtete Bestückung mit auswählen** – JLCPCB lötet X1 und PS1 im Wellenlöten.
- **Hinweis zur USB-Buchse J2 in die Bestellung schreiben:** Die vier Gehäusezapfen (2,3 mm) gehen durch die Platine und sollen auf der Unterseite verlötet werden.

## Besonderheiten einzelner Bauteile

| Ref | Bauteil | Hinweis |
|---|---|---|
| X1 | Phoenix MKDS 1,5/4-5,08 (C5443561) | Leitereinführung zur rechten Platinenkante. Belegung von oben nach unten: L, Licht, N, Lüfter (steht auf der Unterseite neben den Stiften). |
| PS1 | Hi-Link HLK-PM03 (C209904) | Lötstifte 5 mm lang, stehen unten bis 3,4 mm über; das Gehäuse lässt 4 mm Platz, nicht kürzen. Ausweichtyp: YLPTEC HAW3-220S03T2 (C19724490, Reihenabstand 29,4 statt 29,08 mm) – vor einem Tausch die Maße prüfen. |
| U4 | Sensirion SHT40-AD1F-R2 mit Membran (C7461846) | **Nicht** mit C54823945 verwechseln: Fremdmarke, deren Datenblatt keine Membran nennt. |
| U3, Q1 | Lite-On MOC3052S-TA1 (C115471), ST ACST410-8BTR (C221462) | Der Optotriac U3 zündet den Triac Q1. Q1 liegt mit der Kühlfahne nach links, Pin 1 (COM) unten. U3 sitzt über dem Isolationsschlitz, Pins 1 bis 3 oben (3,3-V-Seite). |
| D1 | RGB-LED FM-B2020RGBA-HG (C42421005) | Eckmarke (Pin 1, rot) unten rechts, wenn die Klemme rechts unten liegt. |
| C1 | Panasonic EEHZK1E101UP (C454668) | Hybrid-Polymer-Elko für feuchte Wärme. Beim Lackieren halogenfreien Lack nehmen und die Dichtung am Boden nicht ganz verschließen. |
| J2 | GCT USB4145-03-0230-C (C5291559) | USB-C stehend. Reihe A zeigt zur Oberkante der Platine, A1 liegt links. Lötflächen im Raster 0,5 mm: Vorschau und Lötstellen genau ansehen. Gleiches Lötbild mit kürzeren Zapfen: USB4145-03-0170-C (C5181332), -0070-C (C5815189). |

**Drehlage:** Alle gepolten Bauteile in der Bestückungsvorschau prüfen. Merkhilfen stehen unter [Bestellen → Merkhilfen](../doku/bestellen.md#merkhilfen-für-die-bestückungsvorschau).

## Lagerbestand

Alle Teile der Stückliste waren am 23./24.11.2026 bei JLCPCB am Lager. Die kleinsten Bestände:

| Bauteil | LCSC | Bestand |
|---|---|---|
| USB-Buchse J2 | C5291559 | 355 |
| X2-Kondensator C2 | C237426 | 448 |
| Triac Q1 | C221462 | rund 1.200 |
| Sensor U4 | C7461846 | rund 2.100 |
| Netzteil PS1 | C209904 | rund 3.200 |
