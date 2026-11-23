# Schreibt Stueckliste und Bestueckungsdatei im JLCPCB-Format.
# Aufruf im KiCad-Python: python3 bom_cpl.py <platine.kicad_pcb> <ausgabeordner>   (erwartet dort pos_kicad.csv)
import sys, os, csv, collections
import pcbnew
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from teile import TEILE
pcb, out = sys.argv[1], sys.argv[2]
b = pcbnew.LoadBoard(pcb)
rows = collections.OrderedDict()
dnp = []
def refkey(r):
    import re
    m = re.match(r"([A-Z]+)(\d+)", r); return (m.group(1), int(m.group(2)))
for fp in sorted(b.GetFootprints(), key=lambda f: refkey(f.GetReference())):
    ref = fp.GetReference()
    name = str(fp.GetFPID().GetLibItemName())
    bez, typ, lcsc, hinweis = TEILE.get(ref, (fp.GetValue(), "", "", ""))
    if fp.IsDNP():
        dnp.append((ref, bez, name, hinweis)); continue
    k = (bez, typ, name, lcsc, hinweis)
    if ref == "X1":          # ein Footprint, aber zwei 2-polige Klemmen
        rows.setdefault(k, []).extend(["X1A", "X1B"]); continue
    rows.setdefault(k, []).append(ref)
with open(os.path.join(out, "BOM_JLCPCB.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["Comment", "Designator", "Footprint", "LCSC Part #", "Manufacturer Part", "Quantity", "Note"])
    for (bez, typ, name, lcsc, hinweis), refs in rows.items():
        w.writerow([bez, ",".join(refs), name, lcsc, typ, len(refs), hinweis])
with open(os.path.join(out, "nicht_bestueckt.csv"), "w", newline="") as f:
    w = csv.writer(f); w.writerow(["Designator", "Comment", "Footprint", "Note"])
    for r in dnp: w.writerow(r)
n = 0
with open(os.path.join(out, "pos_kicad.csv")) as f, open(os.path.join(out, "CPL_JLCPCB.csv"), "w", newline="") as g:
    w = csv.writer(g)
    w.writerow(["Designator", "Mid X", "Mid Y", "Layer", "Rotation"])
    for r in csv.DictReader(f):
        if r["Ref"] == "X1":
            for suffix, dy in (("A", 6.0), ("B", -6.0)):   # Mitten der beiden Klemmen, 12 mm auseinander
                w.writerow(["X1" + suffix, "%.4fmm" % float(r["PosX"]), "%.4fmm" % (float(r["PosY"]) + dy), "Top", "%g" % float(r["Rot"])])
                n += 1
            continue
        w.writerow([r["Ref"], "%.4fmm" % float(r["PosX"]), "%.4fmm" % float(r["PosY"]),
                    "Top" if r["Side"].lower().startswith("top") else "Bottom", "%g" % float(r["Rot"])])
        n += 1
print("Stueckliste: %d Positionen, %d Bauteile bestueckt, %d nicht bestueckt" % (len(rows), n, len(dnp)))
