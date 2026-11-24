# Bestellen

[← Zur Übersicht](../README.md)

Die Platine ist für die Fertigung **mit Bestückung bei JLCPCB** vorbereitet. Alle Dateien und die Angaben für das Bestellformular stehen im [Bestellpaket](../bestellpaket/LIESMICH.md). Diese Seite ist die Checkliste, die vor dem Abschicken der Bestellung abgearbeitet werden sollte.

## Checkliste vor der Bestellung

- [ ] **Bedrahtete Bestückung mit auswählen.** JLCPCB führt Klemme und Netzteil unter Wellenlöten. Ihre Stifte stehen unten über (Netzteil bis 3,4 mm, Klemme 1,9 mm); das Gehäuse lässt 4 mm Platz, kürzen ist nicht nötig.
- [ ] **Drehlage in der Bestückungsvorschau prüfen.** Die Winkel in `CPL_JLCPCB.csv` sind KiCad-Winkel; JLCPCB dreht manche Gehäuse anders. Jedes gepolte Bauteil ansehen: U1–U5, Q1, C1, D1, D2, J2, PS1, X1. Merkhilfen stehen [unten](#merkhilfen-für-die-bestückungsvorschau).
- [ ] **Richtigen Sensor prüfen.** U4 muss der Sensirion SHT40-AD1F-R2 mit Membran sein (**C7461846**). Nicht verwechseln mit C54823945: das ist eine Fremdmarke (Tokmas), deren Datenblatt keine Membran nennt.
- [ ] **Lagerbestand prüfen.** Die kleinsten Bestände sind knapp, siehe [Lagerbestand](#lagerbestand).
- [ ] **Hinweis zur USB-Buchse angeben.** Die vier Gehäusezapfen von J2 sind 2,3 mm lang, gehen durch die 1,6-mm-Platine und stehen unten 0,7 mm über. Sie sollen auf der Unterseite mitverlötet werden – das als Hinweis in die Bestellung schreiben und am gelieferten Muster prüfen. Die Lötflächen liegen im Raster 0,5 mm: Vorschau und Lötstellen an dieser Buchse besonders genau ansehen.

## Bekannte Kompromisse

Diese Punkte sind bewusst so entschieden. Wer höhere Ansprüche hat, findet hier die Alternative.

| Thema | Stand | Alternative |
|---|---|---|
| **Netzteil** | Das HLK-PM03 nennt 3000 VAC (an anderer Stelle 2500 VAC) Isolation und „Entwurf entspricht UL/CE“, weist aber keine Zertifizierung des Moduls aus. | Ein zertifiziertes Netzteil braucht ein anderes Modul und einen neuen Footprint. |
| **Sicherung** | Die 0443001.DR schaltet 50 A bei 250 VAC ab. | Schurter UMT 250 (200 A), passt auf dieselben Pads. |
| **Elko C1** | Hybrid-Polymer mit Gummidichtung; Panasonic begrenzt die Lebensdauer deshalb auf 15 Jahre. | Tantal Vishay 293D107X9016D2TE3 (C129696, Bauform D) – braucht einen neuen Footprint. |
| **Snubber C2** | 10 nF | bis 56 nF mit gleichem Footprint (Murata GA355XR7GB563KW06L) |
| **USB** | keine ESD-Schutzbeschaltung an den Datenleitungen | – |

## Lagerbestand

Stand der Bauteilsuche bei JLCPCB am 23. und 24.11.2026: **Alle Teile der Stückliste waren am Lager.** Die kleinsten Bestände:

| Bauteil | LCSC | Bestand | Ausweichtyp |
|---|---|---|---|
| USB-Buchse J2 (USB4145-03-0230-C) | C5291559 | 355 | gleiches Lötbild mit kürzeren Zapfen: USB4145-03-0170-C (C5181332, 363 Stück), USB4145-03-0070-C (C5815189, rund 2.200) |
| X2-Kondensator C2 | C237426 | 448 | – |
| Triac Q1 | C221462 | rund 1.200 | – |
| Sensor U4 | C7461846 | rund 2.100 | – |
| Netzteil PS1 | C209904 | rund 3.200 | YLPTEC HAW3-220S03T2 (C19724490), Reihenabstand 29,4 statt 29,08 mm – vor dem Tausch die Maße prüfen |

Bestände ändern sich schnell. Vor der Bestellung erneut nachsehen.

> [!NOTE]
> Bei den kürzeren USB-Buchsen (Zapfen 1,7 bzw. 0,7 mm) stehen die Zapfen unten kaum oder gar nicht über. Ob sie dann noch sicher verlötet werden, ist nicht geprüft.

## Merkhilfen für die Bestückungsvorschau

Alle Angaben gelten für die Ansicht von oben, mit der Klemme unten rechts.

| Bauteil | Richtige Lage |
|---|---|
| RGB-LED D1 | Eckmarke (Pin 1, rot) unten rechts |
| Triac Q1 | Kühlfahne nach links, Pin 1 (COM) unten |
| Optotriac U3 | sitzt über dem Isolationsschlitz, Pins 1 bis 3 oben (3,3-V-Seite) |
| USB-Buchse J2 | Reihe A zeigt zur Oberkante der Platine, A1 liegt links |
| Netzteil PS1 | 3,3-V-Seite links, Netzseite rechts |
| Klemme X1 | Leitereinführung zur rechten Platinenkante |
