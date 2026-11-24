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
    # Bedrahtete Bauteile haben ihren Ursprung in Pin 1; JLCPCB erwartet die Bauteilmitte (Mitte der Loetaugen)
    mitte = {}
    for fp in b.GetFootprints():
        ps = [q.GetPosition() for q in fp.Pads() if q.GetAttribute() == pcbnew.PAD_ATTRIB_PTH]
        if ps:
            mitte[fp.GetReference()] = ((min(q.x for q in ps) + max(q.x for q in ps)) / 2e6, -(min(q.y for q in ps) + max(q.y for q in ps)) / 2e6)
    for r in csv.DictReader(f):
        if r["Ref"] in mitte:
            r["PosX"], r["PosY"] = mitte[r["Ref"]]
        w.writerow([r["Ref"], "%.4fmm" % float(r["PosX"]), "%.4fmm" % float(r["PosY"]),
                    "Top" if r["Side"].lower().startswith("top") else "Bottom", "%g" % float(r["Rot"])])
        n += 1
print("Stueckliste: %d Positionen, %d Bauteile bestueckt, %d nicht bestueckt" % (len(rows), n, len(dnp)))
