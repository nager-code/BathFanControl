# Funktion

[← Zur Übersicht](../README.md)

Diese Seite beschreibt, was die Steuerung leisten soll und nach welcher Logik die Firmware den Lüfter schaltet.

> [!NOTE]
> Die Firmware ist noch nicht geschrieben. Die Regellogik unten ist das Konzept, nach dem sie entstehen soll.

## Anforderungen

Die Steuerung soll den Lüfter **nach der Luftfeuchte** schalten und **nicht stundenlang nutzlos laufen lassen**.

- Versorgung mit 230 V.
- Zweiter 230-V-Eingang vom Lichtschalter: zeigt, dass jemand im Bad ist.
- Luftfeuchte messen und den Lüfter danach schalten.
- Fortschritt messen: Sinkt die Feuchte nicht (feuchte Wohnungs- oder Außenluft), eine längere Pause einlegen. Die alte Steuerung lief teils acht Stunden durch.
- Licht zehn Minuten an, aber noch kein Feuchteanstieg: Lüfter kurz einschalten.
- Über WLAN erreichbar, möglichst geringer Stromverbrauch.

## Der Lüfter

Die Steuerung ist für den **KN2 UP** ausgelegt: Unterputz-Ventilator für Einrohr-Lüftungssysteme, Baureihe KN ([Anleitung als PDF](https://de.ventilatory.net/media/catalog/product/data/ds-kn2-de.pdf)).

| | |
|---|---|
| Motorleistung | ca. 50 W |
| Grundlüftung | ab Werk keine – es reicht ein Schaltkanal |
| Elektrische Daten | nur auf dem Typenschild (liegt noch nicht vor) |

> [!IMPORTANT]
> Laut Anleitung zerstört eine falsche Beschaltung die Elektronik im Lüfter. Die Steuerung schaltet deshalb **nur die Phase vor dem Ventilator** und greift sonst nicht in das Gerät ein.

## Regellogik

Gerechnet wird mit der **absoluten Feuchte** (g/m³, berechnet aus Temperatur und relativer Feuchte). So wirkt sich eine Temperaturänderung nicht als scheinbare Feuchteänderung aus. Ein langsamer Mittelwert über mehrere Stunden bildet die **Basis**, also den Normalzustand des Raums.

Die Zahlenwerte sind Startwerte und sollen in der Firmware einstellbar sein.

| Zustand | Was passiert | Weiter, wenn … |
|---|---|---|
| **1. Bereit** | Messung alle 30 s. | Start-Bedingung (2) oder Aktivität (5) erfüllt |
| **2. Start** | Lüfter ein bei schnellem Anstieg (z. B. +5 % rF in 5 min) oder Feuchte über Basis +10 %. | sofort weiter mit 3 |
| **3. Lüften** | Alle 10 bis 15 min muss die Feuchte um z. B. 2 bis 3 % rF gefallen sein. Ziel: Basis +3 %, danach 5 min Nachlauf. | Ziel erreicht → 1; kein Fortschritt → 4 |
| **4. Pause** | Kein Fortschritt nach zwei Prüffenstern: Lüfter aus, Pause 1 h. Bei Wiederholung 2 h, dann 4 h. Die Basis wird auf den aktuellen Wert nachgezogen. | Pause vorbei → 1 |
| **5. Aktivität** | Licht 10 min an ohne Feuchteanstieg: 2 bis 3 min Probelauf. Nächster Probelauf frühestens nach 15 bis 20 min. | Feuchte steigt → 3; sonst → 1 |

**Harte Obergrenze:** Eine Laufphase dauert höchstens 45 bis 60 Minuten, unabhängig vom Zustand.

## WLAN und Bedienung

Vorgeschlagen ist **[ESPHome](https://esphome.io/)**: Anbindung an Home Assistant, Updates über WLAN und eine eigene Weboberfläche sind dort bereits enthalten. Alternativ ist eine eigene Firmware mit MQTT oder REST möglich.

Einstellbar sein sollen:

- Schwellwerte für Start, Fortschritt und Ziel
- Pausenzeiten und Obergrenze der Laufzeit
- manuelles Ein- und Ausschalten

Die Pinbelegung für die Firmware steht unter [Schaltung → GPIO-Belegung](schaltung.md#gpio-belegung).

## Anzeige

Die RGB-LED ist von außen durch einen Lichtschacht im Gehäusedeckel zu sehen. Welche Farbe welchen Zustand anzeigt, legt die Firmware fest.
