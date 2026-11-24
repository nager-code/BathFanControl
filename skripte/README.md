# Skripte

[← Zur Übersicht](../README.md)

Die Skripte bauen **Platine und Bestellpaket** aus dem Schaltplan `kicad/lueftersteuerung.kicad_sch` neu auf. Den Schaltplan selbst bearbeitet man in KiCad; alles danach – Footprints, Platzierung, Leiterbahnen, Masseflächen, Beschriftung, Fertigungsdaten – erzeugen die Skripte.

Wer nur die Platine bestellen will, braucht die Skripte nicht: Das fertige [Bestellpaket](../bestellpaket/LIESMICH.md) liegt im Repository.

## Voraussetzungen

Auf dem Rechner:

- Docker
- Python 3
- Java 17 oder neuer; ohne Bildschirm zusätzlich `xvfb-run`
- `rsvg-convert` oder das Python-Paket `cairosvg` (für die Bilder)
- `zip`

### KiCad-Container

Die Skripte erwarten einen laufenden **KiCad-10-Container namens `kc`**, in dem das Projektverzeichnis (die oberste Ebene dieses Repositorys) unter `/w` eingebunden ist. Im Projektverzeichnis ausführen:

```bash
docker run -d --name kc -u 0 -v "$(pwd)":/w -w /w kicad/kicad:10.0 sleep infinity
```

```bash
docker exec kc bash -c 'mkdir -p ~/.config/kicad/10.0 && cp /usr/share/kicad/template/*-lib-table ~/.config/kicad/10.0/'
```

### Freerouting

Für das Autorouting der 3,3-V-Seite wird [Freerouting](https://github.com/freerouting/freerouting) 1.9.0 unter `tools/freerouting-1.9.0.jar` gebraucht:

```bash
mkdir -p tools && curl -L -o tools/freerouting-1.9.0.jar https://github.com/freerouting/freerouting/releases/download/v1.9.0/freerouting-1.9.0.jar
```

## Ablauf

Alle Befehle im Projektverzeichnis ausführen.

**1. Platine neu aufbauen**, bis die Regelprüfung ohne Befund ist:

```bash
skripte/bis_sauber.sh
```

**2. Regelprüfung** zur Kontrolle (Kurzfassung):

```bash
skripte/drc.sh
```

**3. Bestellpaket und Lageplan erzeugen:**

```bash
skripte/export_fab.sh
```

> [!NOTE]
> Der Autorouter arbeitet **nicht deterministisch**. Ein Neuaufbau ergibt auf der 3,3-V-Seite andere Leiterbahnen als die eingecheckte Platine. Die Netzseite ist dagegen fest im Skript hinterlegt.

Zwischenergebnisse landen im Ordner `work/`.

## Übersicht

### Einstiegspunkte

| Skript | Zweck |
|---|---|
| `bis_sauber.sh` | kompletter Neuaufbau; wiederholt `alles.sh` bis zu achtmal, bis die Regelprüfung ohne Befund ist |
| `alles.sh` | ein Durchlauf: Netzliste aus dem Schaltplan, Footprints, Platine, Autorouting, Masseflächen, Beschriftung. Mit `alles.sh nurnetz` nur bis zur Platzierung, ohne Autorouting |
| `drc.sh` | Regelprüfung mit Schaltplanabgleich, Kurzfassung; optional Fehlertypen als Argumente, die übersprungen werden sollen |
| `export_fab.sh` | Gerber, Bohrdaten, Stückliste, Bestückungsdatei und Bestückungspläne nach `bestellpaket/`, dazu der Lageplan nach `doku/` |
| `render.sh` | Bilder der Kupferlagen: `render.sh <platine> <ausgabe-präfix>` |

### Bausteine

| Skript | Zweck |
|---|---|
| `make_footprints.py` | Projekt-Footprints: Klemme, Sicherung, Varistor, X2-Kondensator, RGB-LED, Triac, USB-C-Buchse, Optokoppler |
| `build_board.py` | Platzierung, Umriss, Sperrflächen, handverlegte Netzseite |
| `patch_pro.py` | trägt Netzklassen und Designregeln in die Projektdatei ein (KiCad speichert sie nicht in der `.kicad_pcb`) |
| `route_lv_export.py` | Autorouting Schritt 1: Hilfsplatine ohne Netzseite und Masse als Specctra-DSN für Freerouting |
| `route_lv_import.py` | Autorouting Schritt 2: Ergebnis (Specctra-SES) zurück in die Platine übernehmen |
| `stitch.py` | Masse-Durchkontaktierungen auf der 3,3-V-Seite setzen |
| `fill.py` | alle Kupferflächen füllen |
| `beschriftung.py` | Bestückungsdruck ergänzen, Mindestschrift 1,0 mm / 0,15 mm sicherstellen |
| `bom_cpl.py` | Stückliste und Bestückungsdatei im JLCPCB-Format |
| `teile.py` | Bauteildaten und LCSC-Nummern für die Stückliste |
| `lageplan.py` | beschrifteter Lageplan der Platine (`doku/lageplan.svg`) |
| `einbaulage.py` | Zeichnung der Einbaulage im Lüfterkasten (`doku/einbaulage.svg`) |
| `drcsum.py`, `netparse.py` | Hilfsfunktionen: DRC-Bericht zusammenfassen, Netzliste einlesen |

## Bauteile ändern

Hersteller-Typen und LCSC-Nummern stehen in `teile.py`. Nach einer Änderung `export_fab.sh` erneut laufen lassen, damit Stückliste und Bestückungsdatei aktuell sind. Lagerbestände bei JLCPCB vor der Bestellung neu prüfen.
