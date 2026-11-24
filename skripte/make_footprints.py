# Erzeugt die Projekt-Footprints in <projektordner>/lueftersteuerung.pretty.
# Aufruf im KiCad-10-Python, je Schritt ein eigener Aufruf:
#   python3 make_footprints.py <projektordner> text   (reine Textausgabe, ohne pcbnew)
import sys, os
PRJ, MODE = sys.argv[1], sys.argv[2]
SYSLIB = "/usr/share/kicad/footprints/"
PRJLIB = os.path.join(PRJ, "lueftersteuerung.pretty")
os.makedirs(PRJLIB, exist_ok=True)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

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

# LTV-814S und MOC3052S sitzen ueber dem Isolationsschlitz: Footprints ohne Bestueckungsdruck.
# MOC3052S (Lite-On, SMD-6): Anschlussbreite 10,16 +-0,3 mm, Fuss 1,0 mm, Raster 2,54 mm -> passt auf SMDIP-6_W9.53mm
# (Pads 2,0 x 1,78 mm bei +-4,765 mm).
strip_silk(SYSLIB + "Package_DIP.pretty/SMDIP-4_W9.53mm.kicad_mod", os.path.join(PRJLIB, "LTV-814S_SMDIP-4_W9.53mm.kicad_mod"), "LTV-814S_SMDIP-4_W9.53mm")
strip_silk(SYSLIB + "Package_DIP.pretty/SMDIP-6_W9.53mm.kicad_mod", os.path.join(PRJLIB, "MOC3052S_SMDIP-6_W9.53mm.kicad_mod"), "MOC3052S_SMDIP-6_W9.53mm")

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
# X2-Kondensator Murata GA355 (2220): Loetflaechen 1,4 x 4,8 bei +-2,7, Abstand 4,0 mm (Murata 4,0-4,6)
two_pad("C_2220_Murata_GA355_X2", "Sicherheitskondensator Murata GA355 (2220, 5,7 x 5,0 mm), Padabstand 4,0 mm", 2.7, 1.4, 4.8, 5.7, 5.0)

# RGB-LED Foshan NationStar FM-B2020RGBA-HG (2,1 x 2,1 x 1,0 mm, gemeinsame Anode). Loetflaechen laut Datenblatt:
# vier Flaechen 0,8 x 0,7 mm, Abstand 0,9 mm in x und 0,4 mm in y -> Mitten bei (+-0,85 / +-0,55).
# Draufsicht: Pin 3 (+) oben links, Pin 4 (gruen) oben rechts, Pin 1 (rot, Eckmarke) unten rechts, Pin 2 (blau) unten links.
def make_led():
    name = "LED_RGB_NationStar_FM-B2020"
    L = header(name, "RGB-LED NationStar FM-B2020RGBA-HG, 2,1 x 2,1 mm, 3 = Anode, 1 = rot, 4 = gruen, 2 = blau", 2.3)
    L.append(rect("F.Fab", -1.05, -1.05, 1.05, 1.05, 0.1))
    L.append('  (fp_line (start 0.55 1.05) (end 1.05 0.55) (stroke (width 0.1) (type solid)) (layer "F.Fab"))')      # Eckmarke bei Pin 1
    L.append('  (fp_circle (center 1.75 1.0) (end 1.85 1.0) (stroke (width 0.2) (type solid)) (fill solid) (layer "F.SilkS"))')
    L.append(rect("F.CrtYd", -1.5, -1.3, 1.5, 1.3, 0.05))
    for num, x, y in (("1", 0.85, 0.55), ("2", -0.85, 0.55), ("3", -0.85, -0.55), ("4", 0.85, -0.55)):
        L.append(smdpad(num, x, y, 0.8, 0.7))
    save(name, L)
make_led()

# Triac ST ACST410-8B im DPAK. Loetflaechen nach ST-Datenblatt (Figure 22): Kuehlfahne 6,7 x 6,7 mm, 3,0 mm Abstand,
# zwei Anschlussflaechen 3,0 x 1,6 mm im Abstand 5,094 mm. 1 = COM, 2 = OUT (Fahne), 3 = G.
# Ursprung in der Mitte des Loetbilds, Anschluesse zeigen nach links, Pin 1 oben (Draufsicht).
def make_dpak():
    name = "DPAK_ST_ACST4"
    L = header(name, "DPAK (TO-252) nach ST-Datenblatt ACST4: Fahne 6,7 x 6,7, Anschluesse 3,0 x 1,6, 1 = COM, 2 = OUT (Fahne), 3 = G", 4.6)
    L.append(rect("F.Fab", -3.35, -3.3, 2.75, 3.3, 0.1))            # Gehaeuse 6,1 x 6,6 mm
    L.append(rect("F.Fab", 2.75, -2.7, 3.75, 2.7, 0.1))             # Kuehlfahne
    L.append(rect("F.CrtYd", -6.6, -3.6, 6.6, 3.6, 0.05))
    L.append('  (fp_circle (center -6.9 -2.55) (end -6.8 -2.55) (stroke (width 0.2) (type solid)) (fill solid) (layer "F.SilkS"))')
    L.append(smdpad("1", -4.85, -2.547, 3.0, 1.6))
    L.append(smdpad("3", -4.85, 2.547, 3.0, 1.6))
    L.append(smdpad("2", 3.0, 0, 6.7, 6.7))
    save(name, L)
make_dpak()

# Netzklemme X1, bedrahtet: 4-polige Schraubklemme im Raster 5,08 mm, Leitereinfuehrung parallel zur Platine.
# Abgeleitet vom KiCad-Footprint der Phoenix MKDS 1,5/4-5,08 (Stifte 1,0 mm, Bohrung 1,3 mm); die Loetaugen sind
# von 2,6 auf 2,4 mm verkleinert, damit zwischen benachbarten Netzpotentialen 2,68 mm Kupferabstand bleiben.
def make_x1():
    src = SYSLIB + "TerminalBlock_Phoenix.pretty/TerminalBlock_Phoenix_MKDS-1,5-4-5.08_1x04_P5.08mm_Horizontal.kicad_mod"
    name = "Klemme_4pol_P5.08mm_Horizontal_THT"
    dst = os.path.join(PRJLIB, name + ".kicad_mod")
    strip_silk(src, dst, name)          # ohne Bestueckungsdruck: die Klemme schliesst mit der Platinenkante ab
    t = open(dst, encoding="utf-8").read()
    assert t.count("(size 2.6 2.6)") == 4 and name in t
    t = t.replace("(size 2.6 2.6)", "(size 2.4 2.4)").replace("(roundrect_rratio 0.096154)", "(roundrect_rratio 0.104167)")
    open(dst, "w", encoding="utf-8").write(t)
make_x1()
print("Footprints ok")
