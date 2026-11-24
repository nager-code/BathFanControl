# Zeichnet einen beschrifteten Lageplan der Platine (was sitzt wo, wozu) als SVG.
# Aufruf im KiCad-Python: python3 lageplan.py <platine.kicad_pcb> <ausgabe.svg>
import sys, html
import pcbnew
pcb, out = sys.argv[1], sys.argv[2]
b = pcbnew.LoadBoard(pcb)
OX = OY = 100.0
M = 5.0                     # Rand in mm
K = 2.0                     # die Platine wird in doppelter Groesse gezeichnet
mm = pcbnew.ToMM
def X(v): return mm(v) - OX                    # Platinenkoordinaten in mm (Ursprung oben links)
def Y(v): return mm(v) - OY

# Was ist was: Referenz(en) -> Text. Reihenfolge = Reihenfolge in der Legende.
NETZ = [
    ("X1", "Schraubklemme, Adern von rechts: L, Licht, N, Lüfter"),
    ("F1", "Sicherung T 1 A"),
    ("RV1", "Varistor 275 V~ (Überspannungsschutz)"),
    ("PS1", "Netzteil 230 V~ auf 3,3 V (Hi-Link HLK-PM03)"),
    ("Q1", "Triac, schaltet den Lüfter (ACST410-8B)"),
    ("U3", "Optotriac, zündet Q1 (MOC3052S), über dem Isolationsschlitz"),
    ("R16", "Zündwiderstand 390 Ω"),
    ("R17", "Gate-Widerstand 390 Ω"),
    ("R5, C2", "Snubber 100 Ω + 10 nF parallel zu Q1"),
    ("U2", "Optokoppler Lichteingang (LTV-814S), über dem Isolationsschlitz"),
    ("R1, R2", "Vorwiderstände Lichteingang 2 x 100 kΩ"),
    ("R12", "3,3 kΩ parallel zum Optokoppler, nicht bestückt"),
]
KLEIN = [
    ("U1", "WLAN-Modul ESP32-C3-MINI-1, Antenne an der Oberkante"),
    ("U4", "Feuchte-/Temperatursensor SHT40 mit Membran"),
    ("C7", "100 nF am Sensor"),
    ("D1", "RGB-LED"),
    ("R13, R14, R15", "LED-Vorwiderstände rot 680 Ω, grün 220 Ω, blau 150 Ω"),
    ("R3", "Vorwiderstand 100 Ω für die LED des Optotriacs U3"),
    ("R4, C3", "Lichtsignal: Pull-up 220 kΩ und Filter 470 nF"),
    ("R10, R11", "Pull-ups 10 kΩ für den Sensorbus (SDA, SCL)"),
    ("R6, C6", "Reset (EN): Pull-up 10 kΩ und 1 µF"),
    ("R7, R8, R9", "Pull-ups 10 kΩ an GPIO9 (Boot), GPIO8, GPIO2"),
    ("C1", "Stützkondensator 100 µF (Panasonic Hybrid)"),
    ("C4, C5", "Abblockkondensatoren 10 µF und 100 nF"),
    ("J1", "Programmierflächen: 3V3, GND, TX, RX, IO9, EN (nicht bestückt)"),
]
netz_refs = set(r.strip() for k, _ in NETZ for r in k.split(","))

# ---- Umriss
ps = pcbnew.SHAPE_POLY_SET()
b.GetBoardPolygonOutlines(ps, True)
def ring(c): return "M" + " L".join("%.2f %.2f" % (X(c.CPoint(k).x), Y(c.CPoint(k).y)) for k in range(c.PointCount())) + " Z"
path = ""
for i in range(ps.OutlineCount()):
    path += ring(ps.Outline(i))
    for j in range(ps.HoleCount(i)):
        path += ring(ps.Hole(i, j))
bb = b.GetBoardEdgesBoundingBox()
W, H = mm(bb.GetWidth()), mm(bb.GetHeight())
LX = M + K * W + 10.0                           # Beginn der Legende
TOT_W, TOT_H = LX + 97.0, max(K * H + 2 * M + 9.0, 7.0 + 2 * M + 3.2 * (len(NETZ) + len(KLEIN) + 3) + 14)
S = []
S.append('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %.1f %.1f" width="%.0fmm" height="%.0fmm" font-family="DejaVu Sans, Arial, sans-serif">' % (TOT_W, TOT_H, TOT_W, TOT_H))
S.append('<rect width="100%" height="100%" fill="#ffffff"/>')
S.append('<text x="%.1f" y="7.5" font-size="3.4" font-weight="bold" fill="#222">Lüftersteuerung Bad – Lageplan der Platine (Ansicht von vorn, wie eingebaut)</text>' % M)
S.append('<g transform="translate(%.1f %.1f) scale(%.2f)">' % (M, M + 7.0, K))
S.append('<clipPath id="pl"><path d="%s" clip-rule="evenodd"/></clipPath>' % path)
def yb(y_up): return H - y_up                   # Hoehe ueber der Unterkante -> Zeichnung
ISO0, ISO1, NETZ_OBEN, KS_UNTEN = 21.95, 28.25, 41.05, 47.35
S.append('<g clip-path="url(#pl)">')
S.append('<rect x="-5" y="-5" width="300" height="300" fill="#e3ecfa"/>')                                                 # 3,3 V
S.append('<rect x="%.2f" y="%.2f" width="200" height="200" fill="#fbe3df"/>' % (ISO1, yb(NETZ_OBEN)))                        # Netz
S.append('<rect x="%.2f" y="%.2f" width="%.2f" height="200" fill="#e9e9e9"/>' % (ISO0, yb(KS_UNTEN), ISO1 - ISO0))           # Isolation senkrecht
S.append('<rect x="%.2f" y="%.2f" width="200" height="%.2f" fill="#e9e9e9"/>' % (ISO0, yb(KS_UNTEN), KS_UNTEN - NETZ_OBEN))  # waagrecht
S.append('</g>')
S.append('<path d="%s" fill="none" stroke="#333" stroke-width="0.2" fill-rule="evenodd"/>' % path)

# ---- Bauteile
def fab_box(fp):
    xs, ys = [], []
    def nimm(q):
        xs.extend((q.GetLeft(), q.GetRight())); ys.extend((q.GetTop(), q.GetBottom()))
    for g in fp.GraphicalItems():
        if g.GetClass() == "PCB_SHAPE" and g.GetLayer() == pcbnew.F_Fab:
            nimm(g.GetBoundingBox())
    if not xs:
        for p in fp.Pads():
            nimm(p.GetBoundingBox())
    return X(min(xs)), Y(min(ys)), mm(max(xs) - min(xs)), mm(max(ys) - min(ys))
for fp in sorted(b.GetFootprints(), key=lambda f: f.GetReference()):
    ref = fp.GetReference()
    x, y, w, h = fab_box(fp)
    col = "#b3261e" if ref in netz_refs else "#1f4e9c"
    dash = ' stroke-dasharray="0.5 0.3"' if fp.IsDNP() else ""
    S.append('<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" rx="0.25" fill="#ffffff" fill-opacity="0.92" stroke="%s" stroke-width="0.14"%s/>' % (x, y, w, h, col, dash))
    lang, kurz = max(w, h), min(w, h)
    fs = max(0.8, min(2.0, kurz * 0.72, lang / (0.66 * len(ref))))
    cx, cy = x + w / 2, y + h / 2
    rot = ' transform="rotate(-90 %.2f %.2f)"' % (cx, cy) if h > w * 1.25 and w < 0.66 * len(ref) * fs else ""
    S.append('<text x="%.2f" y="%.2f" font-size="%.2f" text-anchor="middle" dominant-baseline="central" fill="%s" font-weight="bold"%s>%s</text>' % (cx, cy, fs, col, rot, ref))

# ---- Hinweise an der Platine
def note(x, y, t, anchor="start", size=1.2, col="#444", bold=False):
    S.append('<text x="%.2f" y="%.2f" font-size="%.2f" text-anchor="%s" fill="%s"%s>%s</text>' % (x, y, size, anchor, col, ' font-weight="bold"' if bold else "", html.escape(t)))
x1 = b.FindFootprintByReference("X1")
namen = {"4": "L", "3": "Licht", "2": "N", "1": "Lüfter"}
for p in x1.Pads():
    px, py = X(p.GetPosition().x), Y(p.GetPosition().y)
    S.append('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="#b3261e" stroke-width="0.15"/>' % (px + 5.0, py, px + 7.6, py))
    note(px + 8.2, py + 0.6, namen[p.GetNumber()], size=1.7, col="#b3261e", bold=True)
note(63.3, yb(27.3), "Adern von rechts", size=1.25, col="#b3261e")
note(37.0, yb(0.9), "230 V~", "middle", 1.7, "#b3261e", True)
note(1.5, yb(20.0), "3,3 V", "start", 1.7, "#1f4e9c", True)
note(51.0, yb(60.3), "3,3 V", "start", 1.7, "#1f4e9c", True)
note(57.3, yb(43.8), "Isolationsschlitz", "start", 1.1, "#666")
note(W - 7.9, yb(54.3), "Sensor", "start", 1.1, "#1f4e9c")
note(8.3, yb(61.0), "Antenne", "middle", 1.1, "#1f4e9c")
note(4.8, yb(5.1), "Dom", "middle", 1.1, "#666"); note(46.5, yb(55.6), "Dom", "middle", 1.1, "#666")
S.append('</g>')

# ---- Legende
y = 7.0 + M + 2.5
def kopf(t, col):
    global y
    S.append('<rect x="%.1f" y="%.2f" width="3.0" height="2.2" fill="%s" stroke="#555" stroke-width="0.15"/>' % (LX, y - 1.9, col))
    S.append('<text x="%.1f" y="%.2f" font-size="2.5" font-weight="bold" fill="#222">%s</text>' % (LX + 4.2, y, html.escape(t)))
    y += 3.6
def zeile(refs, t, col):
    global y
    S.append('<text x="%.1f" y="%.2f" font-size="2.05" font-weight="bold" fill="%s">%s</text>' % (LX, y, col, html.escape(refs)))
    S.append('<text x="%.1f" y="%.2f" font-size="2.05" fill="#222">%s</text>' % (LX + 19.5, y, html.escape(t)))
    y += 3.2
kopf("Netzseite, 230 V~ (rot)", "#fbe3df")
for r, t in NETZ: zeile(r, t, "#b3261e")
y += 1.8
kopf("Kleinspannung 3,3 V (blau)", "#e3ecfa")
for r, t in KLEIN: zeile(r, t, "#1f4e9c")
y += 1.8
S.append('<text x="%.1f" y="%.2f" font-size="1.9" fill="#555">Grau: kupferfreier Isolationsstreifen mit Schlitz. Gestrichelt: nicht bestückt.</text>' % (LX, y))
S.append('<text x="%.1f" y="%.2f" font-size="1.9" fill="#555">Alle Bauteile sitzen auf dieser Seite; „Dom“ = Bohrung für die Gehäuseschraube.</text>' % (LX, y + 3.0))
S.append("</svg>")
open(out, "w", encoding="utf-8").write("\n".join(S) + "\n")
print("Lageplan:", out)
