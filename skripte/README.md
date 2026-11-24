# Skripte

Die Skripte bauen Platine und Bestellpaket aus dem Schaltplan `kicad/lueftersteuerung.kicad_sch` neu auf. Der Schaltplan selbst wird in KiCad bearbeitet.
Sie erwarten einen laufenden KiCad-10-Container namens `kc`, in dem dieser Ordner unter `/w` liegt:

```bash
docker run -d --name kc -u 0 -v "$(pwd)":/w -w /w kicad/kicad:10.0 sleep infinity
docker exec kc bash -c 'mkdir -p ~/.config/kicad/10.0 && cp /usr/share/kicad/template/*-lib-table ~/.config/kicad/10.0/'
```

Für das Autorouting der 3,3-V-Seite wird Freerouting 1.9.0 unter `tools/freerouting-1.9.0.jar` gebraucht
(Java 17 oder neuer, ohne Bildschirm zusätzlich `xvfb-run`):

```bash
mkdir -p tools && curl -L -o tools/freerouting-1.9.0.jar https://github.com/freerouting/freerouting/releases/download/v1.9.0/freerouting-1.9.0.jar
```

| Skript | Zweck |
|---|---|
| `bis_sauber.sh` | kompletter Neuaufbau, wiederholt das Autorouting, bis die Regelprüfung ohne Befund ist |
| `alles.sh` | ein Durchlauf: Netzliste aus dem Schaltplan, Footprints, Platine, Autorouting, Masseflächen, Beschriftung |
| `drc.sh` | Regelprüfung mit Schaltplanabgleich, Kurzfassung |
| `export_fab.sh` | Gerber, Bohrdaten, Stückliste und Bestückungsdatei nach `bestellpaket/` |
| `render.sh` | Bilder der Lagen |
| `build_board.py` | Platzierung, Umriss, Sperrflächen, handverlegte Netzseite |
| `beschriftung.py` | Bestückungsdruck: Beschriftungen ergänzen, Mindestschrift 1,0 mm / 0,15 mm sicherstellen |
| `lageplan.py` | beschrifteter Lageplan der Platine für die Doku (läuft in `export_fab.sh` mit) |
| `einbaulage.py` | Zeichnung der Einbaulage im Lüfterkasten (`doku/einbaulage.svg`) |
| `make_footprints.py` | Projekt-Footprints (Klemme, Sicherung, Varistor, X2-Kondensator, RGB-LED, Triac, USB-C-Buchse, Optokoppler) |
| `teile.py` | Bauteildaten und LCSC-Nummern für die Stückliste |

Der Autorouter arbeitet nicht deterministisch: ein Neuaufbau ergibt auf der 3,3-V-Seite andere Leiterbahnen
als die eingecheckte Platine. Die Netzseite ist fest im Skript hinterlegt.
