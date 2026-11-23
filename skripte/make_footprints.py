# Erzeugt die Projekt-Footprints in <projektordner>/lueftersteuerung.pretty.
# Aufruf im KiCad-10-Python, je Schritt ein eigener Aufruf:
#   python3 make_footprints.py <projektordner> aqh    Photo-Triac AQH3223A (aus SMDIP-8 abgeleitet)
#   python3 make_footprints.py <projektordner> text   alle uebrigen (reine Textausgabe, ohne pcbnew)
import sys, os
PRJ, MODE = sys.argv[1], sys.argv[2]
SYSLIB = "/usr/share/kicad/footprints/"
PRJLIB = os.path.join(PRJ, "lueftersteuerung.pretty")
os.makedirs(PRJLIB, exist_ok=True)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from x1_param import X1

if MODE == "aqh":
    import pcbnew
    mm = pcbnew.FromMM
    # Panasonic AQ-H SMD (AQH3223A): 8 Pins ohne Pin 7, Raster 2,54 mm.
    # Datenblatt-Loetflaeche 1,5 x 1,9 mm bei Reihenabstand 8,3 mm; hier nach aussen auf 2,3 mm
    # verlaengert (Reihenmitte 8,7 mm), damit auch laengere Anschluesse sicher aufliegen.
    fp = pcbnew.FootprintLoad(SYSLIB + "Package_DIP.pretty", "SMDIP-8_W9.53mm")
    for pad in list(fp.Pads()):
        if pad.GetNumber() == "7":
            fp.Remove(pad)
            continue
        pos = pad.GetPosition()
        sx = -1 if pos.x < 0 else 1
        pad.SetPosition(pcbnew.VECTOR2I(sx * mm(4.35), pos.y))
        pad.SetSize(pcbnew.F_Cu, pcbnew.VECTOR2I(mm(2.3), mm(1.5)))
    fp.SetFPID(pcbnew.LIB_ID("lueftersteuerung", "AQH3223A_SMD-8-N7"))
    fp.SetLibDescription("Panasonic AQ-H SMD, 8 Pins ohne Pin 7 (AQH3223A), Reihenmitte 8,7 mm, Pads 2,3 x 1,5 mm")
    pcbnew.PCB_IO_MGR.FindPlugin(pcbnew.PCB_IO_MGR.KICAD_SEXP).FootprintSave(PRJLIB, fp)
    print("AQH ok"); sys.exit(0)

def strip_silk(src, dst, newname=None):
    """Kopiert eine .kicad_mod-Datei ohne Grafik auf F.SilkS (reine Textbearbeitung)."""
    s = open(src).read()
    body_start = s.index("\n") + 1
    head = s[:body_start] if not newname else '(footprint "%s"\n' % newname
    out, depth, start = [], 0, None
    for i in range(body_start, len(s)):
        c = s[i]
        if c == "(":
            if depth == 0: start = i
            depth += 1
        elif c == ")":
            depth -= 1
            if depth < 0: break
            if depth == 0:
                el = s[start:i + 1]
                if not (el.startswith(("(fp_line", "(fp_arc", "(fp_rect", "(fp_poly", "(fp_circle")) and '"F.SilkS"' in el):
                    out.append("\t" + el)
    open(dst, "w").write(head + "\n".join(out) + "\n)\n")

# LTV-814S und AQH3223A sitzen ueber dem Isolationsschlitz: Footprints ohne Bestueckungsdruck
strip_silk(SYSLIB + "Package_DIP.pretty/SMDIP-4_W9.53mm.kicad_mod", os.path.join(PRJLIB, "LTV-814S_SMDIP-4_W9.53mm.kicad_mod"), "LTV-814S_SMDIP-4_W9.53mm")
f_ = os.path.join(PRJLIB, "AQH3223A_SMD-8-N7.kicad_mod")
strip_silk(f_, f_)

# ---- Footprints als Text im KiCad-Format

def header(name, descr, ty):
    return ['(footprint "%s"' % name, '  (version 20240108) (generator "skript") (layer "F.Cu")',
            '  (descr "%s")' % descr, '  (attr smd)',
            '  (property "Reference" "REF**" (at 0 %.2f 0) (layer "F.SilkS") (effects (font (size 1 1) (thickness 0.15))))' % (-ty),
            '  (property "Value" "%s" (at 0 %.2f 0) (layer "F.Fab") (effects (font (size 1 1) (thickness 0.15))))' % (name, ty),
            '  (fp_text user "${REFERENCE}" (at 0 0 0) (layer "F.Fab") (effects (font (size 0.8 0.8) (thickness 0.12))))']
def rect(layer, x1, y1, x2, y2, w):
    return '  (fp_rect (start %.3f %.3f) (end %.3f %.3f) (stroke (width %.2f) (type solid)) (fill none) (layer "%s"))' % (x1, y1, x2, y2, w, layer)
def smdpad(num, x, y, w, h):
    return '  (pad "%s" smd roundrect (at %.3f %.3f) (size %.3f %.3f) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.1))' % (num, x, y, w, h)
def save(name, lines):
    open(os.path.join(PRJLIB, name + ".kicad_mod"), "w").write("\n".join(lines + [")"]) + "\n")

def two_pad(name, descr, px, pw, ph, bl, bw):
    """Zweipoliges SMD-Bauteil: Pads bei x = +-px (Groesse pw x ph), Gehaeuse bl x bw."""
    ex = max(px + pw / 2.0, bl / 2.0) + 0.25
    ey = max(ph, bw) / 2.0 + 0.25
    L = header(name, descr, ey + 1.2)
    L.append(rect("F.Fab", -bl / 2.0, -bw / 2.0, bl / 2.0, bw / 2.0, 0.1))
    L.append(rect("F.CrtYd", -ex, -ey, ex, ey, 0.05))
    L.append(smdpad("1", -px, 0, pw, ph)); L.append(smdpad("2", px, 0, pw, ph))
    save(name, L)

# Sicherung 10 x 3 mm: Loetflaechen nach Littelfuse 443 (3,25 x 3,43 bei +-4,675), in y auf 3,75 mm
# verbreitert, damit auch Schurter UMT 250 (2,0 x 3,75 bei +-4,25) passt.
two_pad("Fuse_SMD_10x3mm_Littelfuse443_UMT250", "SMD-Sicherung 10,1 x 3 mm, Littelfuse 443 (0443001.DR) oder Schurter UMT 250", 4.675, 3.25, 3.75, 10.1, 3.1)
# Varistor TDK CU3225K275G2 (8,0 x 6,3 mm): Loetflaechen 2,8 x 3,5 bei +-3,65 (Datenblatt)
two_pad("Varistor_TDK_CU3225", "SMD-Varistor TDK CU3225 (B72650M), 8,0 x 6,3 x 4,5 mm", 3.65, 2.8, 3.5, 8.0, 6.3)
# X2-Kondensator Murata GA355 (2220): Loetflaechen 1,5 x 4,8 bei +-2,9, Abstand 4,3 mm (Murata 4,0-4,6)
two_pad("C_2220_Murata_GA355_X2", "Sicherheitskondensator Murata GA355 (2220, 5,7 x 5,0 mm), Padabstand 4,3 mm", 2.9, 1.5, 4.8, 5.7, 5.0)

def make_x1():
    n = len(X1["order"]); p = X1["pitch"]
    y0 = -p * (n - 1) / 2.0
    bx1, bx2 = X1["body"]; hy = p * n / 2.0 - 0.15
    L = header(X1["name"], X1["descr"], hy + 1.2)
    for yc in (-p, p):      # zwei 2-polige Klemmen
        L.append(rect("F.Fab", bx1, yc - 5.85, bx2, yc + 5.85, 0.1))
    L.append(rect("F.CrtYd", min(bx1, X1["pads"][0][0] - X1["pads"][0][2] / 2) - 0.25, -hy - 0.25,
                  max(bx2, X1["pads"][1][0] + X1["pads"][1][2] / 2) + 0.25, hy + 0.25, 0.05))
    for i, num in enumerate(X1["order"]):
        yc = y0 + i * p
        L.append('  (fp_line (start %.3f %.3f) (end %.3f %.3f) (stroke (width 0.1) (type solid)) (layer "F.Fab"))' % (bx1 - 1.0, yc, bx1 + 1.5, yc))
        for dx, dy, w, h in X1["pads"]:
            L.append(smdpad(num, dx, yc + dy, w, h))
    save(X1["name"], L)
make_x1()
print("Footprints ok")
