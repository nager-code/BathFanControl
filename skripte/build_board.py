# Erzeugt die Platine der Lueftersteuerung (v1.5, 76 x 63 mm, 2 Lagen, nur von oben bestueckt) aus der Netzliste.
# SMD-Bauteile, dazu bedrahtet das Netzteil (Hi-Link HLK-PM03) und die Netzklemme (Phoenix MKDS 1,5/4-5,08).
# Die Platine ist so gezeichnet, wie sie eingebaut von vorn zu sehen ist. Von unten nach oben:
#   Riegel 62,6 x 30 mm: links 3,3 V, dann Netzteil und Klemme (Leiter von rechts in den Ausschnitt)
#   Netzreihe bis y = 43,2 mm (76 mm breit): Triac Q1, Varistor, Sicherung, Teilerwiderstaende, Netzseite von U2 und U3
#   Isolationsschlitz 2 mm (nach rechts offen), die Optokoppler sitzen darueber
#   Arm 68 x 18 mm: WLAN-Modul links, RGB-LED, Feuchtesensor ganz rechts hinter einem Thermoschlitz
# Aufruf im KiCad-10-Python:  python3 build_board.py <netzliste.net> <projektordner>
# Ergebnis: <projektordner>/lueftersteuerung.kicad_pcb  (Bauteile platziert, Netzseite geroutet,
# Sperrflaechen, Masseflaechen; die 3,3-V-Seite wird danach vom Autorouter verlegt)
import sys, re, os, math
import pcbnew

NETLIST, PRJ = sys.argv[1], sys.argv[2]
PCB = os.path.join(PRJ, "lueftersteuerung.kicad_pcb")
SYSLIB = "/usr/share/kicad/footprints/"
PRJLIB = os.path.join(PRJ, "lueftersteuerung.pretty")
OX, OY = 100.0, 100.0          # linke obere Platinenecke im KiCad-Koordinatensystem
W, H = 68.0, 63.0               # Arm oben: Breite, und Hoehe der ganzen Platine
SX = 8.0                        # um so viel ist der Netzteil gegenueber dem Arm nach rechts gerueckt (breiter 3,3-V-Teil links)
WU = W + SX                     # Breite des unteren Teils (Riegel + Netzreihe)
XT = 50.0                       # Stiftreihe der Klemme X1 (im Rahmen des Netzteils, ohne SX)
TP = 5.08                       # Raster der Klemme
BW, BH = XT + 4.6 + SX, 30.0    # Riegel unten (Netzteil, Klemmen); die Klemme schliesst rechts mit der Platine ab
SLITZ0, SLITZ1 = 43.2, 45.2     # Isolationsschlitz zwischen Netzreihe und Arm (Hoehe ueber der Unterkante)
NETZ_OBEN, KS_UNTEN = 41.05, 47.35   # bis hier Netzkupfer / ab hier 3,3-V-Kupfer im Arm
BRIDGE = 14.0 + SX              # Breite der Verbindung links
FASE = 6.0                      # abgeschraegte Ecke oben rechts (zeigt zum Luefter-Einlass)
SLOT_X = W - 9.5                # Thermoschlitz vor der Sensorinsel (1 mm breit)
DXS = W - 72.0                  # Lage der Sensorinsel
ISO0, ISO1 = 13.95 + SX, 20.25 + SX   # kupferfreier Streifen im Riegel zwischen 3,3 V (links) und Netz (rechts)
LOCH = [(4.8, 5.5), (46.5, 56.0)]   # Loecher fuer die beiden Schraubdome des Gehaeuses (6,6 mm)
mm = pcbnew.FromMM
F, B = pcbnew.F_Cu, pcbnew.B_Cu
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def P(x, y):
    return pcbnew.VECTOR2I(mm(OX + x), mm(OY + y))

def U(x, y):
    """Koordinaten mit y nach oben (Hoehe ueber der Platinenunterkante) -> Platinenkoordinaten."""
    return (x, H - y)

# ---------------------------------------------------------------- Netzliste lesen
txt = open(NETLIST).read()
comps = {}
for m in re.finditer(r'\(comp\s+\(ref\s+"([^"]+)"\)\s+\(value\s+"([^"]*)"\)\s+\(footprint\s+"([^"]*)"\)(.*?)\(tstamps\s+"([^"]+)"\)', txt, re.S):
    comps[m.group(1)] = dict(value=m.group(2), fp=m.group(3), uuid=m.group(5))
sheet_uuid = re.search(r'\(sheetpath\s+\(names\s+"/"\)\s+\(tstamps\s+"/"\)\)', txt)
padnet = {}
for m in re.finditer(r'\(net\s+\(code\s+"\d+"\)\s+\(name\s+"([^"]*)"\)(.*?)(?=\(net\s+\(code|\Z)', txt, re.S):
    for r, p in re.findall(r'\(node\s+\(ref\s+"([^"]+)"\)\s+\(pin\s+"([^"]+)"\)', m.group(2)):
        padnet[(r, p)] = m.group(1)
assert len(comps) == 35, len(comps)

# ---------------------------------------------------------------- Platine anlegen
if os.path.exists(PCB):
    os.remove(PCB)
board = pcbnew.CreateEmptyBoard()
board.SetCopperLayerCount(2)
bds = board.GetDesignSettings()
bds.SetBoardThickness(mm(1.6))
bds.m_MinClearance = mm(0.15)
bds.m_TrackMinWidth = mm(0.15)
bds.m_ViasMinSize = mm(0.5)
bds.m_MinThroughDrill = mm(0.3)
bds.m_ViasMinAnnularWidth = mm(0.1)
bds.m_CopperEdgeClearance = mm(0.3)
bds.m_HoleClearance = mm(0.2)
bds.m_HoleToHoleMin = mm(0.25)
bds.m_SolderMaskMinWidth = 0
bds.SetAuxOrigin(P(0, H))
bds.SetGridOrigin(P(0, 0))

MAINS = ["/L", "/L_F", "/N", "/L_LICHT", "/LICHT_A", "/LICHT_B", "/L_FAN", "/SNUB",
         "unconnected-(U3-GATE_OFFEN-Pad5)"]
POWER = ["/+3V3", "/GND"]
ns = bds.m_NetSettings
d = ns.GetDefaultNetclass()
d.SetClearance(mm(0.2)); d.SetTrackWidth(mm(0.25)); d.SetViaDiameter(mm(0.6)); d.SetViaDrill(mm(0.3))
nc = pcbnew.NETCLASS("Netz")
nc.SetClearance(mm(0.5)); nc.SetTrackWidth(mm(1.0)); nc.SetViaDiameter(mm(1.2)); nc.SetViaDrill(mm(0.6))
nc.SetDescription("230 V Netzseite")
ns.SetNetclass("Netz", nc)
pw = pcbnew.NETCLASS("Versorgung")
pw.SetClearance(mm(0.2)); pw.SetTrackWidth(mm(0.4)); pw.SetViaDiameter(mm(0.7)); pw.SetViaDrill(mm(0.3))
pw.SetDescription("3,3 V und Masse")
ns.SetNetclass("Versorgung", pw)
for n in MAINS:
    ns.SetNetclassPatternAssignment(n, "Netz")
for n in POWER:
    ns.SetNetclassPatternAssignment(n, "Versorgung")

nets = {}
def net(name):
    if name not in nets:
        ni = pcbnew.NETINFO_ITEM(board, name)
        board.Add(ni)
        nets[name] = ni
    return nets[name]

# ---------------------------------------------------------------- Platzierung
# ref: (x, y, Drehung, Unterseite) - x/y ist der Footprint-Ursprung in Platinenkoordinaten
# ref: (x, y nach oben, Pad-Nr., Soll-Lage dieses Pads) - die Drehung wird daraus bestimmt. Alles auf der Oberseite.
YT = [15.0 + TP * (k_ - 1.5) for k_ in range(4)]   # Pole der Klemme von unten nach oben: Pin 1..4 = Luefter, N, Licht, L
LED_PAD1 = (37.35, 58.05)           # Soll-Lage von Pad 1 der LED (legt die Drehung fest)
def N(x, y, n, tg):             # Bauteil der Netzseite: mit dem ganzen Netzteil um SX nach rechts
    return (x + SX, y, n, (tg[0] + SX, tg[1]))
OBEN = {
    # Riegel
    "X1":  N(XT, YT[0], "4", (XT, YT[3])),                   # bedrahtet; von oben: L, Licht, N, Luefter; Leiter von rechts
    "PS1": N(33.9, 12.5, "2", (33.9, 17.5)),                 # bedrahtet; 3,3 V links, AC rechts (Pin 2 oben = L, Pin 1 unten = N)
    # Netzreihe
    "F1":  N(56.2, 34.2, "1", (60.875, 34.2)),
    "RV1": N(41.95, 33.1, "2", (45.6, 33.1)),
    # Luefterstufe: Triac Q1 liegend (Anschluesse nach rechts, Fahne links), darueber der Optotriac U3 am Schlitz
    "Q1":  N(29.7, 31.7, "3", (34.55, 34.247)),              # 1 = COM unten (L_F), 3 = G oben, Fahne = OUT (L_FAN)
    "R16": N(27.4975, 37.0, "1", (28.96, 37.0)),             # Zuendwiderstand: Optotriac Pin 4 -> Fahne
    "R17": N(37.7, 38.1, "1", (37.7, 38.925)),               # Gate -> COM
    # Snubber im Streifen zwischen Netzteil und Klemme
    "C2":  N(40.8, 20.5, "2", (40.8, 17.8)),
    "R5":  N(40.8, 26.6, "2", (40.8, 25.1375)),
    "R12": N(46.17, 37.5, "2", (45.345, 37.5)),
    "R2":  N(51.4, 39.9, "2", (49.9375, 39.9)),
    "R1":  N(56.4, 39.9, "1", (57.8625, 39.9)),
    # Optokoppler ueber dem Isolationsschlitz: Netzpins unten, 3,3-V-Pins oben
    "U3":  N(31.5, 44.2, "4", (28.96, 39.435)),              # Netzseite von links: 4, 5, 6; 3,3-V-Seite: 3, 2, 1
    "U2":  N(46.17, 44.465, "1", (44.9, 39.7)),
    "R3":  N(34.04, 51.9, "2", (34.04, 51.075)),
    "R4":  N(44.9, 52.2, "2", (44.9, 51.375)),
    "C3":  N(47.0, 52.2, "1", (47.0, 51.425)),
    # Arm und Verbindung (3,3 V)
    "U1":  (8.0, 54.0, "3", (2.1, 53.7)),                    # Antenne an der Oberkante
    "C1":  (24.0, 57.5, "1", (21.2, 57.5)),
    "R9":  (17.0, 60.7, "2", (16.175, 60.7)),
    "R6":  (17.0, 58.8, "2", (16.175, 58.8)),
    "C6":  (17.0, 56.9, "1", (16.225, 56.9)),
    "R7":  (17.0, 55.0, "2", (16.175, 55.0)),
    "R8":  (17.0, 53.1, "2", (16.175, 53.1)),
    "C5":  (11.5, 43.6, "1", (10.725, 43.6)),
    "R10": (11.5, 41.6, "2", (10.675, 41.6)),
    "R11": (11.5, 39.7, "2", (10.675, 39.7)),
    "C4":  (16.0, 33.0, "1", (15.05, 33.0)),
    "J1":  (6.0, 35.0, "1", (4.5, 38.175)),                  # Programmierflaechen (nicht bestueckt)
    # RGB-LED mit Vorwiderstaenden
    "D1":  (36.5, 58.6, "1", LED_PAD1),
    "R13": (31.5, 60.5, "1", (30.675, 60.5)),
    "R14": (31.5, 58.6, "1", (30.675, 58.6)),
    "R15": (31.5, 56.7, "1", (30.675, 56.7)),
    "U4":  (W - 4.8, H - 12.0, "1", (W - 5.5, H - 11.6)),    # Sensor ganz rechts auf der Insel
    "C7":  (W - 2.8, H - 12.0, "1", (W - 2.8, H - 12.775)),
}
PLACE = {}
for r_, (x_, y_, n_, tg_) in OBEN.items():
    PLACE[r_] = U(x_, y_) + (False, n_, U(*tg_))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from teile import TEILE
LCSC = dict((r_, v_[2]) for r_, v_ in TEILE.items() if v_[2])

fps = {}
for ref, c in comps.items():
    lib, name = c["fp"].split(":")
    path = PRJLIB if lib == "lueftersteuerung" else SYSLIB + lib + ".pretty"
    fp = pcbnew.FootprintLoad(path, name)
    assert fp is not None, c["fp"]
    fp.SetFPID(pcbnew.LIB_ID(lib, name))
    fp.SetReference(ref)
    fp.SetValue(c["value"])
    fp.SetPath(pcbnew.KIID_PATH("/" + c["uuid"]))
    board.Add(fp)
    x, y, bottom, pnum, target = PLACE[ref]
    fp.SetPosition(P(x, y))
    if bottom:
        fp.Flip(fp.GetPosition(), pcbnew.FLIP_DIRECTION_LEFT_RIGHT)
    best = None
    for rot in (0, 90, 180, 270):
        fp.SetOrientationDegrees(rot)
        q = [p_ for p_ in fp.Pads() if p_.GetNumber() == pnum][0].GetPosition()
        err = math.hypot(pcbnew.ToMM(q.x) - OX - target[0], pcbnew.ToMM(q.y) - OY - target[1])
        if best is None or err < best[0]:
            best = (err, rot)
    assert best[0] < 0.03, (ref, best)
    fp.SetOrientationDegrees(best[1])
    for pad in fp.Pads():
        n = padnet.get((ref, pad.GetNumber()))
        if n:
            pad.SetNet(net(n))
    if ref in LCSC:
        fp.SetField("LCSC", LCSC[ref])
        fp.GetField("LCSC").SetVisible(False)
    fps[ref] = fp

# R12 wird nur bei Bedarf bestueckt
fps["R12"].SetDNP(True)
fps["R12"].SetExcludedFromPosFiles(True)
fps["R12"].SetExcludedFromBOM(True)
# J1 sind unbestueckte Programmierpads
fps["J1"].SetExcludedFromPosFiles(True)
fps["J1"].SetExcludedFromBOM(True)
fps["J1"].SetDNP(True)

def pad(ref, num):
    for p in fps[ref].Pads():
        if p.GetNumber() == num:
            q = p.GetPosition()
            return (pcbnew.ToMM(q.x) - OX, pcbnew.ToMM(q.y) - OY)
    raise KeyError((ref, num))

# ---------------------------------------------------------------- Umriss, Schlitze
def edge_poly(pts, closed=True):
    n = len(pts)
    for i in range(n if closed else n - 1):
        a, b = pts[i], pts[(i + 1) % n]
        s = pcbnew.PCB_SHAPE(board)
        s.SetShape(pcbnew.SHAPE_T_SEGMENT)
        s.SetStart(P(*a)); s.SetEnd(P(*b))
        s.SetLayer(pcbnew.Edge_Cuts); s.SetWidth(mm(0.1))
        board.Add(s)

# Aussenkontur (y nach oben): Riegel, Netzreihe (rechts ueber dem Anschlussraum laenger), Isolationsschlitz
# nach rechts offen, Arm mit Thermoschlitz vor der Sensorinsel und abgeschraegter Ecke.
edge_poly([U(*q) for q in [(0, 0), (BW, 0), (BW, BH), (WU, BH), (WU, SLITZ0), (BRIDGE, SLITZ0), (BRIDGE, SLITZ1),
                           (SLOT_X, SLITZ1), (SLOT_X, H - 6.0), (SLOT_X + 1.0, H - 6.0), (SLOT_X + 1.0, SLITZ1),
                           (W, SLITZ1), (W, H - FASE), (W - FASE, H), (0, H)]])
for x_, y_ in LOCH:
    s = pcbnew.PCB_SHAPE(board); s.SetShape(pcbnew.SHAPE_T_CIRCLE)
    s.SetCenter(P(*U(x_, y_))); s.SetEnd(P(U(x_, y_)[0] + 3.3, U(x_, y_)[1]))
    s.SetLayer(pcbnew.Edge_Cuts); s.SetWidth(mm(0.1)); board.Add(s)
# Isolationsschlitz im Riegel unter dem Netzteil (2 mm breit, runde Enden)
def slot(x, y1, y2, w):
    r = w / 2.0
    for xx in (x - r, x + r):
        s = pcbnew.PCB_SHAPE(board); s.SetShape(pcbnew.SHAPE_T_SEGMENT)
        s.SetStart(P(xx, y1 + r)); s.SetEnd(P(xx, y2 - r)); s.SetLayer(pcbnew.Edge_Cuts); s.SetWidth(mm(0.1)); board.Add(s)
    for yc, (a0, a1) in ((y1 + r, (x - r, x + r)), (y2 - r, (x + r, x - r))):
        s = pcbnew.PCB_SHAPE(board); s.SetShape(pcbnew.SHAPE_T_ARC)
        mid_y = yc - r if yc < (y1 + y2) / 2 else yc + r
        s.SetArcGeometry(P(a0, yc), P(x, mid_y), P(a1, yc))
        s.SetLayer(pcbnew.Edge_Cuts); s.SetWidth(mm(0.1)); board.Add(s)
slot((ISO0 + ISO1) / 2, U(0, 24.5)[1], U(0, 4.5)[1], 2.0)

# ---------------------------------------------------------------- Sperrflaechen und Masse
def zone(pts, layers, netname=None, rule=None, name=""):
    z = pcbnew.ZONE(board)
    ls = pcbnew.LSET()
    for l in layers:
        ls.AddLayer(l)
    z.SetLayerSet(ls)
    o = z.Outline(); o.NewOutline()
    for x, y in pts:
        o.Append(mm(OX + x), mm(OY + y))
    z.SetZoneName(name)
    if rule:
        z.SetIsRuleArea(True)
        z.SetDoNotAllowTracks("tracks" in rule)
        z.SetDoNotAllowVias("vias" in rule)
        z.SetDoNotAllowZoneFills("fill" in rule)
        z.SetDoNotAllowPads(False)
        z.SetDoNotAllowFootprints(False)
    else:
        z.SetNet(net(netname))
        z.SetLocalClearance(mm(0.3))
        z.SetMinThickness(mm(0.25))
        z.SetPadConnection(pcbnew.ZONE_CONNECTION_FULL)       # alles SMD und Reflow: Pads voll anbinden
        z.SetThermalReliefGap(mm(0.3))
        z.SetThermalReliefSpokeWidth(mm(0.4))
        z.SetIslandRemovalMode(pcbnew.ISLAND_REMOVAL_MODE_ALWAYS)
        z.SetAssignedPriority(0)
    board.Add(z)
    return z

def rect(x1, y1, x2, y2):
    return [(x1, y1), (x2, y1), (x2, y2), (x1, y2)]

def urect(x1, y1, x2, y2):          # Rechteck in Koordinaten mit y nach oben
    return rect(x1, H - y2, x2, H - y1)
zone(urect(ISO0, 0, ISO1, SLITZ0), [F, B], rule=("tracks", "vias", "fill"), name="Isolation im Riegel")
zone(urect(ISO0, NETZ_OBEN, WU, KS_UNTEN), [F, B], rule=("tracks", "vias", "fill"), name="Isolation Netzreihe / Arm")
zone(rect(0, 0, 15.2, 6.3), [F, B], rule=("tracks", "vias", "fill"), name="Antenne U1")
zone(rect(SLOT_X, 0, W, H - SLITZ1), [F, B], rule=("fill",), name="Sensorinsel ohne Flaeche")
# Randstreifen fuer den Autorouter: keine Bahnen/Durchkontaktierungen dicht an Kanten und Loechern
RAND = [rect(15.2, 0, SLOT_X - 1.5, 0.45), rect(0, 6.3, 0.45, H), urect(0, 0, ISO0, 0.45),
        rect(SLOT_X - 0.45, 5.4, SLOT_X, H - SLITZ1), rect(SLOT_X - 0.45, 5.4, SLOT_X + 1.45, 6.0)]
RAND += [urect(x_ - 3.75, y_ - 3.75, x_ + 3.75, y_ + 3.75) for x_, y_ in LOCH]
for i_, r_ in enumerate(RAND):
    zone(r_, [F, B], rule=("tracks", "vias"), name="Rand %d" % (i_ + 1))
zone([U(*q) for q in [(0, 0), (ISO0 - 0.05, 0), (ISO0 - 0.05, SLITZ1), (W, SLITZ1), (W, H), (0, H)]],
     [F, B], netname="/GND", name="GND")

# ---------------------------------------------------------------- Leiterbahnen
def track(netname, pts, w, layer):
    for a, b in zip(pts, pts[1:]):
        if a == b:
            continue
        t = pcbnew.PCB_TRACK(board)
        t.SetStart(P(*a)); t.SetEnd(P(*b)); t.SetWidth(mm(w)); t.SetLayer(layer); t.SetNet(net(netname))
        board.Add(t)

def via(netname, xy, dia, drill):
    v = pcbnew.PCB_VIA(board)
    v.SetPosition(P(*xy)); v.SetViaType(pcbnew.VIATYPE_THROUGH); v.SetLayerPair(F, B)
    v.SetWidth(F, mm(dia)); v.SetDrill(mm(drill)); v.SetNet(net(netname))
    board.Add(v)

# --- Netzseite (von Hand, 1,0 mm; nach den 2 x 100 k duenner), Koordinaten mit y nach oben.
# Bestueckt ist nur die Oberseite; die Unterseite dient als zweite Verdrahtungsebene: von den Klemmen
# laufen N, Licht, Luefter und L unten nach oben in die Netzreihe.
# Alle Zahlen der Netzseite gelten im Rahmen des Netzteils (x ohne die Verschiebung SX).
def padu(ref, num):
    x_, y_ = pad(ref, num); return (x_ - SX, H - y_)
def tr(netname, pts, w, layer): track(netname, [U(q[0] + SX, q[1]) for q in pts], w, layer)
def vi(netname, xy, dia=1.2, drill=0.6): via(netname, U(xy[0] + SX, xy[1]), dia, drill)
PL, PLI, PN, PF = padu("X1", "4"), padu("X1", "3"), padu("X1", "2"), padu("X1", "1")   # L, Licht, N, Luefter
psn, psl = padu("PS1", "1"), padu("PS1", "2")
# Die bedrahteten Stifte verbinden beide Lagen. Von der Klemme laufen die Bahnen auf der Unterseite erst nach links
# und dann nebeneinander nach oben in die Netzreihe: Licht bei x = 45,6, N bei 41,9, Luefter bei 38,3.
# N: oben direkt zum Netzteil (AC unten), unten hoch zur Netzreihe -> Varistor, Optokoppler U2, R12
tr("/N", [PN, psn], 1.0, F)
vi("/N", (41.9, 37.6))
tr("/N", [PN, (41.9, PN[1]), (41.9, 37.6)], 1.0, B)
u21, rv2, r122 = padu("U2", "1"), padu("RV1", "2"), padu("R12", "2")
tr("/N", [(41.9, 37.6), (u21[0], 37.6), u21], 1.0, F)
tr("/N", [(u21[0], 37.6), (rv2[0], 36.4), rv2], 1.0, F)
tr("/N", [r122, (u21[0], 37.6)], 0.5, F)
# Lichteingang: Klemme -> unten hoch -> R1 -> R2 -> Optokoppler U2
vi("/L_LICHT", (59.8, 39.9))
tr("/L_LICHT", [PLI, (45.6, PLI[1]), (45.6, 37.3), (59.8, 37.3), (59.8, 39.9)], 1.0, B)
tr("/L_LICHT", [(59.8, 39.9), padu("R1", "1")], 1.0, F)
tr("/LICHT_A", [padu("R1", "2"), padu("R2", "1")], 1.0, F)
u22 = padu("U2", "2")
tr("/LICHT_B", [padu("R2", "2"), (u22[0] + 0.6, 39.9), u22], 0.4, F)
tr("/LICHT_B", [padu("R12", "1"), (u22[0], 38.4), u22], 0.4, F)
# L_FAN: Klemme -> unten nach links und hoch, unter der Oberkante des Netzteils weiter zur Kuehlfahne (OUT) von Q1;
# unterwegs ein Abzweig nach oben zum Snubber-Kondensator C2
vi("/L_FAN", (26.7, 26.9)); vi("/L_FAN", (38.3, 16.2), 1.0, 0.5)
tr("/L_FAN", [PF, (38.3, PF[1]), (38.3, 26.9), (26.7, 26.9)], 1.0, B)
tr("/L_FAN", [(26.7, 26.9), (26.7, 29.5)], 1.0, F)
tr("/L_FAN", [(38.3, 16.2), (39.2, 17.8), padu("C2", "2")], 1.0, F)
r162 = padu("R16", "2")
tr("/L_FAN", [r162, (r162[0], 34.5)], 0.8, F)
# Zuendkreis: Optotriac Pin 4 -> R16 -> OUT, Optotriac Pin 6 -> Gate, R17 vom Gate nach COM
tr("/OPTO_R", [padu("R16", "1"), padu("U3", "4")], 0.5, F)
qg, u34 = padu("Q1", "3"), padu("U3", "6")
tr("/TRIAC_G", [qg, (u34[0], 35.6), u34], 0.5, F)
tr("/TRIAC_G", [padu("R17", "1"), (u34[0], padu("R17", "1")[1])], 0.5, F)
# L: vom obersten Pol unten zur Sicherung
f11, f12 = padu("F1", "1"), padu("F1", "2")
vi("/L", (f11[0], 31.2))
tr("/L", [PL, (51.5, PL[1] + 1.5), (51.5, 29.9), (52.8, 31.2), (f11[0], 31.2)], 1.0, B)
tr("/L", [(f11[0], 31.2), f11], 1.0, F)
# L_F: Sicherung -> Varistor -> Snubber R5 -> COM von Q1 und Netzteil (AC oben)
rv1 = padu("RV1", "1")
r51, qc = padu("R5", "1"), padu("Q1", "1")
tr("/L_F", [f12, (50.6, 32.0), (50.6, 28.3), (34.5, 28.3), (psl[0], 26.7), psl], 1.0, F)
tr("/L_F", [(rv1[0], 28.3), rv1], 1.0, F)
tr("/L_F", [(r51[0], 28.3), r51], 1.0, F)
tr("/L_F", [(qc[0], 28.3), qc], 1.0, F)
r172 = padu("R17", "2")
tr("/L_F", [r172, (r172[0], 34.2)], 0.5, F)
# Snubber: R5 -> C2
tr("/SNUB", [padu("R5", "2"), padu("C2", "1")], 1.0, F)

# --- Sensorinsel (von Hand, 0,2 mm): vier Bahnen laufen oben ueber den Steg neben dem Thermoschlitz
sda, scl, vdd, vss = pad("U4", "1"), pad("U4", "2"), pad("U4", "3"), pad("U4", "4")
c71, c72 = pad("C7", "1"), pad("C7", "2")
XS = 59.5 + DXS                             # hier uebernimmt der Autorouter
# Pads des Sensors nur von aussen anfahren (Sperrflaeche des Footprints unter dem Sensor)
track("/SCL_IO7", [(XS, 4.8), (64.2 + DXS, 4.8), (64.2 + DXS, scl[1]), (66.3 + DXS, scl[1])], 0.2, F)
track("/SDA_IO6", [(XS, 4.1), (64.9 + DXS, 4.1), (64.9 + DXS, sda[1]), (66.3 + DXS, sda[1])], 0.2, F)
track("/GND", [(XS, 3.2), (66.0 + DXS, 3.2), (69.2 + DXS, 6.4), c72], 0.25, F)
track("/GND", [c72, (68.5 + DXS, c72[1]), (68.1 + DXS, vss[1])], 0.2, F)
track("/+3V3", [(XS, 2.3), (66.6 + DXS, 2.3), (70.6 + DXS, 6.3), (70.6 + DXS, 13.7), (69.2 + DXS, 13.7), c71], 0.25, F)
track("/+3V3", [c71, (68.5 + DXS, c71[1]), (68.1 + DXS, vdd[1])], 0.2, F)
via("/GND", (XS, 3.2), 0.6, 0.3)
# Masseflaeche unter dem WLAN-Modul ueber dessen Massepad (EPAD) an die Unterseite anbinden
via("/GND", (8.0, 11.7), 0.6, 0.3)
via("/GND", (9.975, 13.675), 0.6, 0.3)
# ---------------------------------------------------------------- Beschriftung
def text(s, x, y, layer, size=1.0, rot=0, mirror=False, thick=0.15):
    t = pcbnew.PCB_TEXT(board)
    t.SetText(s); t.SetPosition(P(x, y)); t.SetLayer(layer)
    t.SetTextSize(pcbnew.VECTOR2I(mm(size), mm(size))); t.SetTextThickness(mm(thick))
    t.SetTextAngleDegrees(rot); t.SetMirrored(mirror)
    board.Add(t)
    return t

# Referenzen nicht auf den Bestueckungsdruck (zu eng), sie stehen auf den Fab-Lagen und im Bestueckungsplan
for fp in board.GetFootprints():
    fp.Reference().SetVisible(False)
    fp.Value().SetVisible(False)
    for f_ in fp.GetFields():
        if f_.GetName() not in ("Reference", "Value"):
            f_.SetVisible(False)

# Klemmenbelegung: auf der Oberseite verdeckt das Klemmengehaeuse alles, deshalb auf der Unterseite neben den Stiften
for lab, num in (("L", "4"), ("Licht", "3"), ("N", "2"), ("Luefter", "1")):
    text(lab, XT + SX - 4.6, pad("X1", num)[1], pcbnew.B_SilkS, 1.0, 0, True)
text("230 V~", 12.0 + SX, U(0, 15.0)[1], pcbnew.F_SilkS, 1.5, 0, False, 0.25)
text("230 V~", 30.0 + SX, U(0, 15.0)[1], pcbnew.B_SilkS, 1.2, 0, True, 0.2)
text("Lueftersteuerung Bad v1.5", 40.0, U(0, 50.3)[1], pcbnew.B_SilkS, 0.8, 0, True, 0.12)
text("Sensor", W - 4.5, 16.0, pcbnew.F_SilkS, 0.8, 0, False, 0.12)

pcbnew.SaveBoard(PCB, board)
print("gespeichert:", PCB)
for ref in sorted(fps):
    print("  %-4s %s" % (ref, " ".join("%s=(%.2f,%.2f)" % (p_.GetNumber(), pcbnew.ToMM(p_.GetPosition().x) - OX, pcbnew.ToMM(p_.GetPosition().y) - OY) for p_ in list(fps[ref].Pads())[:8])))
