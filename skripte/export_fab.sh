#!/bin/bash
W=$(cd "$(dirname "$0")/.." && pwd)   # Projektordner (im Container unter /w eingebunden)
# Erzeugt das Bestellpaket (Gerber, Bohrdaten, Stueckliste, Bestueckungsdatei) aus der KiCad-Platine.
# Aufruf: export_fab.sh   (laeuft gegen den Container "kc", Projekt unter /w/kicad)
set -e
OUT=$W/bestellpaket
rm -rf $OUT/gerber $OUT/*.csv $OUT/*.pdf $OUT/*.zip; mkdir -p $OUT/gerber
docker exec -w /w/kicad kc kicad-cli pcb export gerbers --layers "F.Cu,B.Cu,F.Paste,B.Paste,F.SilkS,B.SilkS,F.Mask,B.Mask,Edge.Cuts" \
   --subtract-soldermask -o /w/bestellpaket/gerber/ lueftersteuerung.kicad_pcb
docker exec -w /w/kicad kc kicad-cli pcb export drill --format excellon --excellon-units mm --excellon-separate-th \
   --generate-map --map-format pdf -o /w/bestellpaket/gerber/ lueftersteuerung.kicad_pcb
docker exec -w /w/kicad kc kicad-cli pcb export pos --format csv --units mm --side both --exclude-dnp \
   -o /w/bestellpaket/pos_kicad.csv lueftersteuerung.kicad_pcb
docker exec kc python3 /w/skripte/bom_cpl.py /w/kicad/lueftersteuerung.kicad_pcb /w/bestellpaket
docker exec -w /w/kicad kc kicad-cli pcb export pdf --layers "F.Fab,F.SilkS,Edge.Cuts" --mode-single --black-and-white \
   -o /w/bestellpaket/bestueckung_oben.pdf lueftersteuerung.kicad_pcb >/dev/null 2>&1 || true
docker exec -w /w/kicad kc kicad-cli pcb export pdf --layers "B.Fab,B.SilkS,Edge.Cuts" --mirror --mode-single --black-and-white \
   -o /w/bestellpaket/bestueckung_unten.pdf lueftersteuerung.kicad_pcb >/dev/null 2>&1 || true
docker exec kc chmod -R a+rwX /w/bestellpaket
rm -f $OUT/pos_kicad.csv
(cd $OUT/gerber && zip -q ../gerber_lueftersteuerung.zip *)
ls -la $OUT $OUT/gerber
