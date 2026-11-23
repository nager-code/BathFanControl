#!/bin/bash
W=$(cd "$(dirname "$0")/.." && pwd)   # Projektordner (im Container unter /w eingebunden)
# render.sh <pcb> <outprefix>  -> PNGs fuer Ober-/Unterseite
PCB=$1; OUT=$2
docker exec kc kicad-cli pcb export svg --mode-single --page-size-mode 2 --exclude-drawing-sheet --layers "B.Cu,F.Cu,F.SilkS,F.CrtYd,Edge.Cuts,User.Drawings" -o /w/work/render/top.svg "$PCB" >/dev/null 2>&1
docker exec kc kicad-cli pcb export svg --mode-single --page-size-mode 2 --exclude-drawing-sheet --layers "F.Cu,B.Cu,B.SilkS,B.CrtYd,Edge.Cuts" -o /w/work/render/bot.svg "$PCB" >/dev/null 2>&1
for s in top bot; do rsvg-convert -w 2400 -b white $W/work/render/$s.svg -o ${OUT}_$s.png 2>/dev/null || python3 -I -c "import cairosvg,sys; cairosvg.svg2png(url=sys.argv[1],write_to=sys.argv[2],output_width=2400,background_color='white')" $W/work/render/$s.svg ${OUT}_$s.png; done
ls -la ${OUT}_*.png
