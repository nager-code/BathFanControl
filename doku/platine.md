# Platine

[← Zur Übersicht](../README.md)

Die Platine hat eine Sonderform, damit sie unten links in den Lüfterkasten passt: Unten liegen Netzteil und Klemme, rechts kommen die Leitungen herein, und oben rechts sitzt der Feuchtesensor in einer abgeschrägten Ecke, die zum Lüfter-Einlass zeigt.

![Lageplan: was sitzt wo auf der Platine](lageplan.png?v=1.0)

Den Lageplan gibt es auch als [SVG](lageplan.svg). Auf der Platine selbst ist für die Namen der kleinen Bauteile kein Platz; der Lageplan ersetzt diese Beschriftung.

## Eckdaten

| | |
|---|---|
| Umriss | 68 x 72,5 mm, unten rechts ein Ausschnitt 13,4 x 34,5 mm für die Leitungen, darüber ein nach rechts offener Isolationsschlitz, oben rechts eine abgeschrägte Ecke |
| Aufbau | 2 Lagen, FR4 1,6 mm, 35 µm Kupfer |
| Bestückung | nur von oben: 38 SMD-Bauteile, dazu bedrahtet Netzteil und Klemme |
| Bauhöhe | ca. 20 mm: Netzteil 15,1 mm über der Platine, seine Lötstifte bis 3,4 mm darunter |
| Abstand zwischen Netzpotentialen | mind. 2,5 mm (Ausnahmen direkt an Bauteilen, siehe [Isolation](#isolation)) |
| Abstand Netz zu 3,3 V | mind. 6 mm, dazu 2 mm breite Frässchlitze |
| Bestückungsdruck | alle Texte mind. 1,0 mm hoch und 0,15 mm stark (als Designregel hinterlegt) |
| Entwurf | KiCad 10.0.8, Projekt in [`kicad/`](../kicad) |

## Anordnung

Die Platine ist so gezeichnet, wie man sie eingebaut **von vorn** sieht. Höhenangaben zählen ab der Unterkante des Netzteil-Riegels (y = 0). Von unten nach oben:

| Bereich | Größe | Inhalt |
|---|---|---|
| **Streifen unten** | 4,5 mm hoch | links die Bohrung für den unteren Schraubdom, unter dem 3,3-V-Ende des Netzteils. Rechts, unter dem Netz-Ende des Netzteils, der Snubber R5/C2; daneben der Titel mit dem Versionsstand und „230 V~“. |
| **Riegel** | 54,6 x 30 mm | Netzteil PS1 (3,3 V links, Netz rechts), Schraubklemme X1 mit Leitereinführung nach rechts, dazwischen auf der Oberseite die Klemmenbelegung. Rechts neben der Klemme ist die Platine ausgeschnitten: dort ist der Anschlussraum für die Adern. |
| **Netzreihe** | bis 43,2 mm Höhe, 68 mm breit | Triac Q1 (liegend, Kühlfahne links), Varistor, Sicherung, R1/R2. Links davon ein 14 mm breiter 3,3-V-Streifen. |
| **Isolationsschlitz** | 2 mm, nach rechts offen | trennt Netzreihe und Arm. Optotriac U3 und Optokoppler U2 sitzen darüber: Netzpins unten, 3,3-V-Pins oben. |
| **Arm** | 68 x 23 mm | links das WLAN-Modul U1 (Antenne an der Oberkante), daneben C1, RGB-LED D1 mit Vorwiderständen, USB-C-Buchse J2 mit Regler U5. Ganz rechts hinter einem Thermoschlitz die **Sensorinsel** mit U4 und C7. |

Weitere Merkmale:

- **Zwei Bohrungen 6,6 mm** (unten links und oben rechts im Arm) für die Schraubdome des Gehäuses. Beide liegen im 3,3-V-Bereich, mehr als 10 mm vom Netzkupfer entfernt.
- **Die Unterseite trägt keine Bauteile.** Sie dient als zweite Verdrahtungsebene; dort stehen nur die Lötstifte von Netzteil und Klemme über.
- **Der Thermoschlitz** vor der Sensorinsel hält die Abwärme von Netzteil und Controller vom Sensor fern.

## Klemmenbelegung

Von oben nach unten (Raster 5,08 mm):

| Pol | Anschluss |
|---|---|
| 1 | **L** – Phase |
| 2 | **Licht** – geschaltete Phase vom Lichtschalter |
| 3 | **N** – Neutralleiter |
| 4 | **Lüfter** – geschaltete Phase zum Lüfter |

Die Reihenfolge ergibt sich aus der kreuzungsfreien Verdrahtung. Sie steht:

- auf der Oberseite direkt hinter der Klemme, je Pol ein Name auf Höhe der Schraube – lesbar, wenn die Platine in der Wanne liegt und der Deckel ab ist,
- auf der Unterseite neben den Stiften,
- außen auf dem Gehäusedeckel.

## Isolation

- **Netz zu 3,3 V:** kupferfreie Streifen von 6,3 mm. Im unteren Teil verlaufen sie senkrecht, mit einem Frässchlitz 2 x 20 mm unter dem Netzteil; darüber waagrecht entlang des durchgehenden Isolationsschlitzes unter U2 und U3.
- **Zwischen Netzpotentialen:** mindestens 2,5 mm. Ausnahmen gibt es nur direkt an Bauteilen, deren Anschlüsse enger liegen: Teiler R1/R2, Snubber, Zünd- und Gate-Widerstand, Substrat-Pin des Optotriacs.
- **Zur Platinenkante:** Das Netzkupfer reicht an der Klemmenseite bis etwa 2,5 mm an die Kante.

## Leiterbahnen

- **Netzseite von Hand geroutet**, 1,0 mm breit; nach den beiden 100-kΩ-Widerständen 0,4 mm, dort fließen weniger als 2 mA. Licht, N und Lüfter laufen auf der Unterseite von den Klemmenstiften erst nach links und dann nebeneinander nach oben in die Netzreihe. L geht vom obersten Pol direkt zur Sicherung.
- **3,3-V-Seite mit dem Autorouter** [Freerouting](https://github.com/freerouting/freerouting) verlegt, danach Masseflächen auf beiden Lagen mit Masse-Durchkontaktierungen.

## Bestückungsdruck

- **Oberseite:** Titel mit Versionsstand, „230 V~“, Namen der größeren Bauteile, BOOT/RST, USB, LED und die Klemmenbelegung.
- **Unterseite:** Belegung der Netzteil- und Klemmenstifte.

## Ansichten

| Oberseite | Unterseite |
|---|---|
| ![Kupferlagen Oberseite](lagen_oberseite.png?v=1.0) | ![Kupferlagen Unterseite](lagen_unterseite.png?v=1.0) |

![3D-Ansichten der Platine von allen Seiten](platine_3d_ansichten.png?v=1.0)

In den 3D-Bildern sind Sicherung, Varistor, X2-Kondensator, Triac, LED, USB-Buchse und Sensor vereinfachte Quader, weil es für sie kein fertiges 3D-Modell gibt. Die Datei [`platine_3d.glb`](platine_3d.glb) lässt sich in jedem glTF-Betrachter drehen.

## Prüfung in KiCad

| Prüfung | Ergebnis |
|---|---|
| Schaltplanprüfung (ERC) | 0 Meldungen |
| Designregelprüfung (DRC) mit Schaltplanabgleich | 0 Verletzungen, 0 offene Verbindungen – [Bericht](drc_bericht.txt) |

Platine und Fertigungsdaten lassen sich mit den [Skripten](../skripte/README.md) neu erzeugen.
