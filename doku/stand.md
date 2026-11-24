# Projektstand

[← Zur Übersicht](../README.md)

**Stand:** V1.0 – Planung abgeschlossen · Platine und Gehäuse V1.0

## Kurz gesagt

| Bereich | Stand |
|---|---|
| Schaltplan | fertig, gegen Datenblätter geprüft, ERC ohne Befund |
| Platine | fertig geroutet, DRC ohne Befund, Bestellpaket erzeugt |
| Gehäuse | fertig geplant, rechnerisch gegen die Platine und im Slicer geprüft, **noch nicht gedruckt** |
| Firmware | **fehlt**, Konzept siehe [Funktion](funktion.md) |
| Muster | **noch nicht gebaut, nicht elektrisch getestet** |

Geprüft wurde bisher nur in KiCad und rechnerisch am 3D-Modell.

## Was geprüft ist

- **Schaltplanprüfung (ERC):** 0 Meldungen.
- **Designregelprüfung (DRC)** mit Schaltplanabgleich: 0 Verletzungen, 0 offene Verbindungen ([Bericht](drc_bericht.txt)).
- **Pinbelegungen und Grenzwerte** aller wichtigen Bauteile gegen die Datenblätter ([Datenblattprüfung](schaltung.md#datenblattprüfung)).
- **Abstände:** 2,5 mm zwischen Netzpotentialen und 6 mm zwischen Netz und 3,3 V eingehalten ([Isolation](platine.md#isolation)).
- **Gehäuse gegen Platine:** keine Durchdringung, kleinster Abstand 0,6 mm; beide STL-Dateien laufen ohne Warnung durch PrusaSlicer ([Gehäuse → Geprüft](../gehaeuse/README.md#geprüft)).
- **Lieferbarkeit:** alle Teile am 23./24.11.2026 bei JLCPCB am Lager ([Lagerbestand](bestellen.md#lagerbestand)).

## Offene Punkte

### Firmware

- Regellogik umsetzen (Konzept und Pinbelegung in [Funktion](funktion.md) und [Schaltung](schaltung.md#gpio-belegung)).
- Erstes Aufspielen über die USB-C-Buchse, danach Updates über WLAN.
- Offen: Ist Home Assistant vorhanden? Davon hängt ab, ob ESPHome oder eine eigene Firmware mit MQTT/REST die bessere Wahl ist.
- Offen: Welche LED-Farbe zeigt welchen Zustand an?

Beide Fragen werden zu Beginn der Firmware-Entwicklung geklärt.

### Hardware

- Erstes Muster bestellen, aufbauen und elektrisch testen.
- Typenschild des KN2 ablesen: Die elektrischen Daten des Lüfters sind noch nicht bekannt.
- WLAN-Empfang im Lüfterkasten ausprobieren.
- Verlötung der USB-Buchsen-Zapfen am gelieferten Muster prüfen.

### Gehäuse

- Probedruck, Passform und Einbaulage prüfen. Die vollständige Liste steht unter [Gehäuse → Offen](../gehaeuse/README.md#offen-und-vor-dem-druck-zu-klären).

## Versionsgeschichte

Gegenüber dem ersten Entwurf (Stand in der Git-Historie) wurde die Steuerung überarbeitet:

- Pinbelegungen gegen Datenblätter geprüft
- Umstellung auf KiCad 10 und auf SMD-Bauteile, einseitige Bestückung von oben
- Platinenform und Gehäuse für den Einbau unten links im Lüfterkasten
- Photo-Triac AQH3223A ersetzt durch Optotriac MOC3052S und Triac ACST410-8B
- neu: RGB-LED und USB-C-Buchse zum Programmieren (statt Programmierleiste)
- Layout geroutet, Bestellpaket erzeugt
