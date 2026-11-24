#!/bin/bash
W=$(cd "$(dirname "$0")/.." && pwd)   # Projektordner (im Container unter /w eingebunden)
# Kompletter Durchlauf: Schaltplan anpassen -> Netzliste -> Footprints -> Platine -> Autorouting 3,3 V -> Masse -> DRC
set -e

cd $W
python3 -I skripte/update_sch.py eingang/lueftersteuerung.kicad_sch kicad/lueftersteuerung.kicad_sch kicad/Luefter.kicad_sym
docker exec -w /w/kicad kc bash -c 'kicad-cli sym upgrade Luefter.kicad_sym >/dev/null 2>&1; kicad-cli sch upgrade lueftersteuerung.kicad_sch >/dev/null 2>&1; kicad-cli sch export netlist -o /w/work/sch/neu.net lueftersteuerung.kicad_sch >/dev/null 2>&1'
docker exec kc python3 /w/skripte/make_footprints.py /w/kicad text 2>&1 | grep -v -E "Debug|leak" | tail -1
docker exec kc python3 /w/skripte/build_board.py /w/work/sch/neu.net /w/kicad 2>&1 | grep -v -E "Debug|leak" | head -1
python3 -I skripte/patch_pro.py kicad/lueftersteuerung.kicad_pro
if [ "$1" = "nurnetz" ]; then exit 0; fi
rm -rf work/route; mkdir -p work/route work/sch work/render; chmod -R 777 work
docker exec kc python3 /w/skripte/route_lv_export.py /w/kicad/lueftersteuerung.kicad_pcb /w/work/route/tmp.kicad_pcb /w/work/route/lv.dsn 2>&1 | grep -E "DSN|Netze"
(cd work/route && timeout 500 xvfb-run -a java -jar "$W/tools/freerouting-1.9.0.jar" -de lv.dsn -do lv.ses -mp 30 2>&1 | grep -E "Auto-routing was completed|optimization was completed|not found|unrouted" | tail -3 || true)
test -s work/route/lv.ses
docker exec kc python3 /w/skripte/route_lv_import.py /w/kicad/lueftersteuerung.kicad_pcb /w/work/route/tmp.kicad_pcb /w/work/route/lv.ses 2>&1 | grep -E "SES|uebernommen"
docker exec kc python3 /w/skripte/stitch.py /w/kicad/lueftersteuerung.kicad_pcb 2>&1 | grep -E "Masse"
python3 -I skripte/patch_pro.py kicad/lueftersteuerung.kicad_pro
