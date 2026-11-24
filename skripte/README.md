# Skripte

Die Skripte bauen Schaltplan, Platine und Bestellpaket aus `eingang/lueftersteuerung.kicad_sch` neu auf.
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
| `alles.sh` | ein Durchlauf: Schaltplan anpassen, Footprints, Platine, Autorouting, Masseflächen |
| `drc.sh` | Regelprüfung mit Schaltplanabgleich, Kurzfassung |
| `export_fab.sh` | Gerber, Bohrdaten, Stückliste und Bestückungsdatei nach `bestellpaket/` |
| `render.sh` | Bilder der Lagen |
| `update_sch.py` | Änderungen am übergebenen Schaltplan (Datenblattkorrekturen, SMD-Bauteile) |
| `build_board.py` | Platzierung, Umriss, Sperrflächen, handverlegte Netzseite |
| `make_footprints.py` | Projekt-Footprints (Klemme, Sicherung, Varistor, X2-Kondensator, RGB-LED, Optokoppler) |
| `teile.py` | Bauteildaten und LCSC-Nummern für die Stückliste |

Der Autorouter arbeitet nicht deterministisch: ein Neuaufbau ergibt auf der 3,3-V-Seite andere Leiterbahnen
als die eingecheckte Platine. Die Netzseite ist fest im Skript hinterlegt.
