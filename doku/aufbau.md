# Aufbau und Einbau

[← Zur Übersicht](../README.md)

Diese Seite beschreibt die Schritte von der gelieferten Platine bis zur eingebauten Steuerung.

> [!CAUTION]
> Die Steuerung arbeitet mit **230 V im Feuchtraum**. Den Anschluss an das Hausnetz muss eine Elektrofachkraft vornehmen oder abnehmen. Alle Arbeiten nur im spannungsfreien Zustand.

> [!NOTE]
> Bisher wurde keine Platine gebaut. Die Schritte beruhen auf dem Entwurf und sind noch nicht erprobt.

## Übersicht

1. [Firmware aufspielen](#firmware-aufspielen)
2. [Platine lackieren](#platine-lackieren)
3. [Gehäuse drucken und Platine einsetzen](#gehäuse-drucken-und-platine-einsetzen)
4. [Anschließen](#anschließen)
5. [Im Lüfterkasten befestigen](#im-lüfterkasten-befestigen)

## Firmware aufspielen

> [!IMPORTANT]
> **USB nur anstecken, wenn die Platine vom Netz getrennt ist.** Programmiert wird nur bei abgenommenem Deckel, also mit offen liegender Netzseite.

1. Deckel abnehmen. Die USB-C-Buchse J2 steht senkrecht auf der Platine und ist nur bei offenem Gehäuse erreichbar; der Stecker kommt von vorn.
2. USB-Kabel anstecken. Die Platine wird dann aus USB mit 3,3 V versorgt, Netzspannung ist nicht nötig.
3. Firmware aufspielen. Der ESP32-C3 meldet sich über seine eingebaute USB-Schnittstelle.
4. Den Stecker gerade herausziehen, nicht seitlich abknicken.

Danach kommen Updates über WLAN.

**Notfall – Firmware legt USB lahm:** Lötflächen **JP1** (Boot) überbrücken, dann kurz **JP2** (Reset) überbrücken. Der Controller startet in den Bootloader und meldet sich wieder über USB. Danach die Brücke an JP1 wieder entfernen.

Die Pinbelegung für die Firmware steht unter [Schaltung → GPIO-Belegung](schaltung.md#gpio-belegung).

## Platine lackieren

Die Steuerung sitzt im Lüfterkasten im Strom der feuchten Badluft. Die Platine sollte deshalb einen **Schutzlack** bekommen.

**Aussparen** (abkleben oder nicht besprühen):

- Sensor U4 – die Membran darf nicht überlackiert werden
- Schraubklemme X1
- RGB-LED D1
- USB-Buchse J2
- Lötflächen JP1 und JP2

**Elko C1:** Panasonic verlangt einen **halogenfreien Lack**, der die Gummidichtung am Boden des Kondensators zu höchstens zwei Dritteln bedeckt. Betauung schließt Panasonic als Betriebsbedingung aus.

## Gehäuse drucken und Platine einsetzen

Das Gehäuse besteht aus Wanne und Deckel für den 3D-Druck. Alle Details – Werkstoff, Druckdateien, offene Punkte – stehen in der [Gehäuse-Doku](../gehaeuse/README.md).

- **Werkstoff:** flammhemmend nach UL 94 V-0, z. B. entsprechend ausgewiesenes PETG, ABS oder PC. **Kein normales PLA.**
- Die Platine liegt auf Leisten der Wanne; zwei Dome gehen durch ihre Bohrungen.
- Verschlossen wird mit zwei Kunststoffschrauben 3 x 10 mm von vorn, am besten mit Senkkopf (der Sitz im Deckel ist eine 90°-Senkung).

## Anschließen

Die vier Adern kommen von rechts durch die Öffnungen im Gehäuse in den Anschlussraum vor der Schraubklemme.

| Pol (von oben) | Anschluss |
|---|---|
| 1 | **L** – Phase |
| 2 | **Licht** – geschaltete Phase vom Lichtschalter |
| 3 | **N** – Neutralleiter |
| 4 | **Lüfter** – geschaltete Phase zum Lüfter |

- Die Klemme nimmt Leiter von 0,14 bis 1,5 mm² auf. Feindrähtige Litzen mit **Aderendhülse** anschließen.
- Im Lüfterkasten liegen flexible Litzen mit Steckverbindern. Mit starren Adern wird der Leitungsaustritt eng.
- Die Steuerung schaltet **nur die Phase vor dem Ventilator**. Laut Anleitung des KN2 zerstört eine falsche Beschaltung die Elektronik im Lüfter.
- Die Klemmenbelegung steht auf der Platine direkt hinter der Klemme; außen auf dem Gehäuse sind die Anschlüsse nicht beschriftet.

## Im Lüfterkasten befestigen

![Einbaulage im Lüfterkasten](einbaulage.svg?v=1.0)

- **Einbauort:** unten links im Lüfterkasten, vor dem Lüftergehäuse. Linke Seite an der Kastenwand, Unterseite auf dem Kastenboden.
- **Platz:** am Einbauort sind höchstens 85 mm Breite, 40 mm Tiefe und 140 mm Höhe frei; das Gehäuse braucht 72,6 x 25,7 x 77,1 mm.
- **Befestigung:** doppelseitiges Klebeband auf der linken Seite (zur Kastenwand) oder auf der Rückseite. Flächen vorher entstauben und entfetten. In den Lüfterkasten wird nicht gebohrt.
- **Vorher prüfen:** mit einer Pappschablone 73 x 77 mm, ob die Wartungsöffnung der Rückstauklappe frei bleibt.
- **Brandschutz:** Bei Einrohrsystemen am gemeinsamen Schacht die Brandschutzklappe nicht verändern.
- **WLAN:** Die Antenne sitzt an der Oberkante der Platine, gut 25 mm über dem Netzteil; links liegt die Kastenwand, dahinter das Lüftergehäuse. Wie gut der Empfang im Kasten ist, zeigt erst ein Versuch.
