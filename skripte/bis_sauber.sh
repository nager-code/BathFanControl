#!/bin/bash
W=$(cd "$(dirname "$0")/.." && pwd)   # Projektordner (im Container unter /w eingebunden)
# Wiederholt Aufbau + Autorouting, bis die Regelpruefung ohne Befund ist (der Router arbeitet nicht deterministisch).
cd $W
for i in 1 2 3 4 5 6 7 8; do
  skripte/alles.sh > work/alles.log 2>&1 || { echo "Lauf $i: Abbruch"; tail -3 work/alles.log; continue; }
  r=$(skripte/drc.sh | head -1)
  echo "Lauf $i: $r"
  case "$r" in "{} unverbunden: 0 Schaltplanabgleich: 0") echo "sauber"; exit 0;; esac
done
exit 1
