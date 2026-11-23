#!/bin/bash
W=$(cd "$(dirname "$0")/.." && pwd)   # Projektordner (im Container unter /w eingebunden)
# drc.sh [zu ueberspringende Typen...]  -> DRC der Projektplatine, Kurzfassung
docker exec -w /w/kicad kc kicad-cli pcb drc --severity-all --schematic-parity --format json -o /w/work/drc.json lueftersteuerung.kicad_pcb >/dev/null 2>&1
python3 -I $W/skripte/drcsum.py $W/work/drc.json "$@"
