# Bestellpaket Lüftersteuerung Bad V1.0

## Leiterplatte
- `gerber_lueftersteuerung.zip` hochladen (Inhalt liegt auch entpackt in `gerber/`)
- 2 Lagen, Umriss 68 x 72,5 mm (keine Rechteckform: unten rechts ein Ausschnitt 13,4 x 34,5 mm, darüber ein nach rechts offener Schlitz, oben rechts eine abgeschrägte Ecke), FR4 1,6 mm, 35 µm Kupfer
- Kleinste Leiterbahn 0,2 mm, kleinster Abstand 0,2 mm, kleinste Bohrung 0,3 mm (Durchkontaktierung 0,6 mm)
- Bohrungen für bedrahtete Bauteile: 4 x 1,3 mm (Klemme) und 4 x 1,0 mm (Netzteil), durchkontaktiert; an der USB-Buchse vier metallisierte Langlöcher 1,10 x 0,60 mm und zwei Führungslöcher ohne Kupfer (rund 0,71 mm, Langloch 1,01 x 0,71 mm)
- Bestückungsdruck auf beiden Seiten, kleinste Schrift 1,0 mm hoch mit 0,15 mm Strichstärke
- Fräsungen: Isolationsschlitz 2 x 20 mm unter dem Netzteil und zwei Bohrungen 6,6 mm (ohne Kupfer) innerhalb der Kontur; der 2 mm breite Isolationsschlitz unter den Optokopplern und der Thermoschlitz 1 mm sind Teil der Außenkontur

## Bestückung
- Alles von oben: 38 SMD-Bauteile, dazu zwei bedrahtete Teile (Klemme X1, Netzteil PS1), die JLCPCB im Wellenlöten bestückt. Beim Bestellen die bedrahtete Bestückung mit auswählen.
- `BOM_JLCPCB.csv` – Stückliste mit LCSC-Nummern
- `CPL_JLCPCB.csv` – Bestückungsdatei (Koordinaten passend zu den Gerberdaten)
- `bestueckung_oben.pdf` – Bestückungsplan; `bestueckung_unten.pdf` zeigt nur die Beschriftung der Unterseite
- Eine beschriftete Übersicht der Bauteile liegt in `../doku/lageplan.png` (auf der Platine selbst stehen keine Bauteilnamen)
- `nicht_bestueckt.csv` – R12 (nur bei Fehlauslösung durch Glimmlampe/LED-Leuchte) sowie JP1 und JP2 (Lötflächen für Boot und Reset, kein Bauteil)

## Besonderheiten
- X1 ist eine 4-polige Schraubklemme Phoenix MKDS 1,5/4-5,08 (C5443561), Leitereinführung zur rechten Platinenkante. Belegung von oben nach unten: L, Licht, N, Lüfter (steht auf der Unterseite neben den Stiften).
- Die Lötstifte des Netzteils sind 5 mm lang und stehen unten bis zu 3,4 mm über; das Gehäuse lässt dafür 4 mm Platz. Sie müssen nicht gekürzt werden.
- PS1 ist das bedrahtete Netzteil Hi-Link HLK-PM03 (C209904). Ausweichtyp mit fast gleichem Stiftbild: YLPTEC HAW3-220S03T2 (C19724490, Reihenabstand 29,4 statt 29,08 mm); vor einem Tausch die Maße prüfen.
- Drehlage aller gepolten Bauteile in der Bestückungsvorschau prüfen. Bei der RGB-LED D1 liegt die Eckmarke (Pin 1, rot) unten rechts, wenn die Klemmen rechts unten liegen.
- Alle Teile der Stückliste waren am 23./24.11.2026 bei JLCPCB am Lager. Die kleinsten Bestände: X2-Kondensator C2 (C237426) 448 Stück, Triac Q1 (C221462) rund 1.200, Sensor U4 rund 2.100, Netzteil rund 3.200.
- U4 ist der Sensirion SHT40-AD1F-R2 mit Membran (C7461846). Nicht mit C54823945 verwechseln: das ist eine Fremdmarke, deren Datenblatt keine Membran nennt.
- Lüfterstufe: Optotriac U3 (Lite-On MOC3052S-TA1, C115471) zündet den Triac Q1 (ST ACST410-8BTR, C221462). Q1 liegt mit der Kühlfahne nach links, Pin 1 (COM) unten; U3 sitzt über dem Isolationsschlitz mit den Pins 1 bis 3 oben (3,3-V-Seite).
- C1 ist ein Hybrid-Polymer-Elko Panasonic EEHZK1E101UP (C454668), für feuchte Wärme spezifiziert. Beim Lackieren der Platine halogenfreien Lack nehmen und die Dichtung am Boden des Kondensators nicht ganz verschließen.
- J2 ist eine stehende USB-C-Buchse GCT USB4145-03-0230-C (C5291559), Reihe A zeigt zur Oberkante der Platine, A1 liegt links. Ihre vier Gehäusezapfen (2,3 mm) gehen durch die Platine und sollen auf der Unterseite verlötet werden: bei der Bestellung als Hinweis angeben. Lötflächen im Raster 0,5 mm: Bestückungsvorschau und Lötstellen an dieser Buchse genau ansehen. Gleiches Lötbild mit kürzeren Zapfen: USB4145-03-0170-C (C5181332) und -0070-C (C5815189).
