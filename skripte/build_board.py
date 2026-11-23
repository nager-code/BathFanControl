# Erzeugt die Platine der Lueftersteuerung (v1.2, 68 x 58 mm, 2 Lagen) aus der Schaltplan-Netzliste.
# Form: unten ein Riegel 54 x 30 mm mit Netzteil und Klemmen (Leitungen von rechts), darueber - durch einen
# 10 mm breiten Spalt getrennt - ein Arm 68 x 18 mm mit WLAN-Modul links und Feuchtesensor ganz rechts.
# Aufruf im KiCad-10-Python:  python3 build_board.py <netzliste.net> <projektordner>
# Ergebnis: <projektordner>/lueftersteuerung.kicad_pcb  (Bauteile platziert, Netzseite geroutet,
# Sperrflaechen, Masseflaechen; die 3,3-V-Seite wird danach mit route_lv.py geroutet)
import sys, re, os, math
import pcbnew

NETLIST, PRJ = sys.argv[1], sys.argv[2]
PCB = os.path.join(PRJ, "lueftersteuerung.kicad_pcb")
SYSLIB = "/usr/share/kicad/footprints/"
PRJLIB = os.path.join(PRJ, "lueftersteuerung.pretty")
OX, OY = 100.0, 100.0          # linke obere Platinenecke im KiCad-Koordinatensystem
W, H = 68.0, 58.0               # Umriss gesamt
BW, BH = 54.0, 30.0             # Riegel unten (Netzteil, Klemmen)
SH = 18.0                       # Hoehe des Arms oben
GAP = H - BH - SH               # Spalt zwischen Arm und Riegel
BRIDGE = 14.0                   # Breite der Verbindung links
FASE = 6.0                      # abgeschraegte Ecke oben rechts (zeigt zum Luefter-Einlass)
SLOT_X = W - 9.5                # Thermoschlitz vor der Sensorinsel (1 mm breit)
DXS = W - 72.0                  # Verschiebung der Sensorinsel gegenueber dem ersten Entwurf
mm = pcbnew.FromMM
F, B = pcbnew.F_Cu, pcbnew.B_Cu
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from x1_param import X1, X1X
X1LABELX = X1X + X1["body"][1] + 0.2

def P(x, y):
    return pcbnew.VECTOR2I(mm(OX + x), mm(OY + y))

def T(x, y):
    """Riegel-Koordinaten (wie Platine v1.1: Klemmen bei x = 0, y nach unten) -> Platinenkoordinaten.
    Der Riegel ist um 180 Grad gedreht: Klemmen rechts, Leitereinfuehrung nach rechts."""
    return (BW - x, H - y)

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
assert len(comps) == 28, len(comps)

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
# ref: (Ursprung x, y, Unterseite, Pad-Nr., Soll-Lage dieses Pads) - die Drehung wird daraus bestimmt
RIEGEL = {   # in Riegel-Koordinaten, werden mit T() umgerechnet
    # Oberseite
    "X1":  (X1X, 15.0, False, "2", (X1X - 5.25, 6.0)),
    "PS1": (35.6, 15.0, False, "24", (21.63, 1.765)),
    # Unterseite Netz
    "F1":  (11.0, 26.9, True, "1", (6.325, 26.9)),
    "RV1": (13.3, 14.5, True, "2", (13.3, 10.85)),
    "R1":  (23.1, 11.3, True, "1", (21.64, 11.3)),
    "R2":  (27.8, 11.3, True, "1", (26.34, 11.3)),
    "R12": (29.9, 8.0, True, "2", (29.9, 7.175)),
    "C2":  (24.3, 18.59, True, "2", (24.3, 15.69)),
    "R5":  (24.3, 24.85, True, "2", (24.3, 23.39)),
    "U2":  (36.9, 8.0, True, "2", (32.135, 6.73)),
    "U3":  (36.9, 19.5, True, "8", (32.55, 15.69)),
    # Unterseite 3,3 V
    "R4":  (45.2, 9.27, True, "2", (44.375, 9.27)),
    "C3":  (45.2, 11.4, True, "1", (44.425, 11.4)),
    "R3":  (44.4, 18.23, True, "2", (43.575, 18.23)),
    "J1":  (49.5, 22.0, True, "1", (51.0, 18.825)),
}
PLACE = {    # Arm oben, in Platinenkoordinaten
    "U1":  (8.0, 9.0, False, "3", (2.1, 9.3)),              # Antenne an der Oberkante
    "C1":  (20.5, 9.0, False, "1", (17.7, 9.0)),
    "U4":  (W - 4.8, 12.0, False, "1", (W - 5.5, 11.6)),          # Sensor ganz rechts auf der Insel
    "C7":  (W - 2.8, 12.0, False, "1", (W - 2.8, 12.775)),
    "C5":  (5.2, 8.2, True, "1", (4.425, 8.2)),
    "C4":  (5.2, 10.4, True, "1", (4.25, 10.4)),
    "R9":  (11.0, 8.2, True, "2", (10.175, 8.2)),
    "R6":  (11.0, 10.3, True, "2", (10.175, 10.3)),
    "C6":  (11.0, 12.4, True, "1", (10.225, 12.4)),
    "R10": (17.0, 15.6, True, "2", (16.175, 15.6)),
    "R11": (17.0, 13.6, True, "2", (16.175, 13.6)),
    "R8":  (17.0, 11.6, True, "2", (16.175, 11.6)),
    "R7":  (17.0, 9.6, True, "2", (16.175, 9.6)),
}
for r_, (x_, y_, b_, n_, tg_) in RIEGEL.items():
    PLACE[r_] = T(x_, y_) + (b_, n_, T(*tg_))
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

# Aussenkontur: Arm oben mit abgeschraegter Ecke und Thermoschlitz vor der Sensorinsel (nach unten offen),
# Verbindung links, Riegel unten. Der Spalt zwischen Arm und Riegel ist nach rechts offen.
edge_poly([(0, 0), (W - FASE, 0), (W, FASE), (W, SH), (SLOT_X + 1.0, SH), (SLOT_X + 1.0, 6.0), (SLOT_X, 6.0),
           (SLOT_X, SH), (BRIDGE, SH), (BRIDGE, SH + GAP), (BW, SH + GAP), (BW, H), (0, H)])
# Isolationsschlitz zwischen den Pinreihen von U2/U3 (2 mm breit, runde Enden)
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
sx_, sy1_ = T(36.9, 24.5); sy2_ = T(36.9, 4.5)[1]
slot(sx_, sy1_, sy2_, 2.0)

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

ISO0, ISO1 = BW - 40.05, BW - 33.75        # kupferfreier Streifen im Riegel zwischen Netz und 3,3 V
zone(rect(ISO0, SH + GAP, ISO1, H), [F, B], rule=("tracks", "vias", "fill"), name="Isolation Netz / 3,3 V")
zone(rect(0, 0, 15.2, 6.3), [F, B], rule=("tracks", "vias", "fill"), name="Antenne U1")
zone(rect(SLOT_X, 0, W, SH), [F, B], rule=("fill",), name="Sensorinsel ohne Flaeche")
# Randstreifen fuer den Autorouter: keine Bahnen/Durchkontaktierungen dicht an den Kanten
for i_, r_ in enumerate((rect(15.2, 0, SLOT_X - 1.5, 0.45), rect(BRIDGE, SH - 0.45, SLOT_X, SH), rect(0, 6.3, 0.45, H),
                         rect(0, H - 0.45, ISO0, H), rect(BRIDGE - 0.45, SH, BRIDGE, SH + GAP), rect(SLOT_X - 0.45, 5.4, SLOT_X, SH),
                         rect(SLOT_X - 0.45, 5.4, SLOT_X + 1.45, 6.0))):
    zone(r_, [F, B], rule=("tracks", "vias"), name="Rand %d" % (i_ + 1))
zone([(0, 0), (W, 0), (W, SH), (BRIDGE, SH), (BRIDGE, SH + GAP), (ISO0 - 0.05, SH + GAP), (ISO0 - 0.05, H), (0, H)],
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

# --- Netzseite (von Hand, 1,0 mm; nach den 2 x 100 k duenner), gerechnet in Riegel-Koordinaten
def padb(ref, num): return T(*pad(ref, num))
def trackb(netname, pts, w, layer): track(netname, [T(*q) for q in pts], w, layer)
def viab(netname, xy, dia, drill): via(netname, T(*xy), dia, drill)
# Oberseite: Klemme und Netzteil. Unterseite: Sicherung, Varistor, Snubber, Optokoppler.
# An der Klemme liegen von oben nach unten L, Luefter, Licht, N - so kreuzt auf keiner Lage etwas.
def xpads(num):
    ps = [T(pcbnew.ToMM(p_.GetPosition().x) - OX, pcbnew.ToMM(p_.GetPosition().y) - OY) for p_ in fps["X1"].Pads() if p_.GetNumber() == num]
    return sorted(ps)
(NF, NR), (LLF, LLR), (LFF, LFR), (LF_, LR_) = xpads("2"), xpads("3"), xpads("4"), xpads("1")
for n_, a_, b_ in (("/N", NF, NR), ("/L_LICHT", LLF, LLR), ("/L_FAN", LFF, LFR), ("/L", LF_, LR_)):
    trackb(n_, [a_, b_], 1.0, F)            # vordere und hintere Loetflaeche jedes Pols verbinden
VN, VLL, VLF, VLFT, VL = (19.0, 4.0), (20.2, 11.3), (20.3, 15.69), (23.4, 27.9), (9.0, 24.0)
# N: Klemme -> Netzteil AC/N (oben), Durchkontaktierung, unten zu Varistor und Optokoppler
psn, psl = padb("PS1", "24"), padb("PS1", "1")
trackb("/N", [NR, (17.6, 6.0), VN, (psn[0], 2.3), psn], 1.0, F)
viab("/N", VN, 1.2, 0.6)
u22 = padb("U2", "2")
trackb("/N", [VN, (19.6, 3.4), (28.8, 3.4), (30.9, 5.5), (30.9, u22[1]), u22], 1.0, B)
rv2 = padb("RV1", "2")
trackb("/N", [rv2, (rv2[0], 4.6), (rv2[0] + 1.2, 3.4), (19.6, 3.4)], 1.0, B)
trackb("/N", [padb("R12", "2"), (30.9, u22[1])], 0.5, B)
# Lichteingang: Klemme (oben) -> Durchkontaktierung -> R1 -> R2 -> Optokoppler (unten)
trackb("/L_LICHT", [LLR, (18.5, 12.0), VLL], 1.0, F)
viab("/L_LICHT", VLL, 1.2, 0.6)
trackb("/L_LICHT", [VLL, padb("R1", "1")], 1.0, B)
trackb("/LICHT_A", [padb("R1", "2"), padb("R2", "1")], 1.0, B)
u21 = padb("U2", "1")
r22 = padb("R2", "2")
trackb("/LICHT_B", [r22, (r22[0] + 1.14, 10.16), (31.3, u21[1]), u21], 0.4, B)
trackb("/LICHT_B", [padb("R12", "1"), (31.0, u21[1]), u21], 0.4, B)
# L_FAN: Klemme (oben) -> Durchkontaktierung -> Snubber-Kondensator -> Triac (unten)
trackb("/L_FAN", [LFR, (18.5, 18.0), VLF], 1.0, F)
viab("/L_FAN", VLF, 1.2, 0.6)
trackb("/L_FAN", [VLF, padb("C2", "2"), padb("U3", "8")], 1.0, B)
# L: Durchkontaktierung unter der Klemme -> Sicherung (unten)
viab("/L", VL, 1.2, 0.6)
f11 = padb("F1", "1")
trackb("/L", [VL, (f11[0] + 0.6, 26.2), f11], 1.0, B)
# L_F: Sicherung -> Varistor, Snubber-Widerstand, Triac (unten) und Netzteil AC/L (oben)
f12 = padb("F1", "2")
u36 = padb("U3", "6")
trackb("/L_F", [f12, (f12[0] + 0.6, 26.3), (29.9, 26.3), (29.9, u36[1] + 1.03), (30.93, u36[1]), u36], 1.0, B)
r51 = padb("R5", "1")
trackb("/L_F", [r51, (r51[0], 26.3)], 1.0, B)
rv1 = padb("RV1", "1")
trackb("/L_F", [rv1, (rv1[0], 23.4), (f12[0], 25.775), f12], 1.0, B)
trackb("/L_F", [(23.4, 26.3), VLFT], 1.0, B)
viab("/L_F", VLFT, 1.2, 0.6)
trackb("/L_F", [VLFT, psl], 1.0, F)
# Snubber: C2 -> R5
trackb("/SNUB", [padb("C2", "1"), padb("R5", "2")], 1.0, B)

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
# Massepad der Programmierpads direkt durchkontaktieren (unbestueckt, daher unkritisch)
j12 = padb("J1", "2")
viab("/GND", (j12[0] - 1.0, j12[1]), 0.6, 0.3)

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

# Klemmenbelegung: auf der Oberseite verdeckt das Klemmengehaeuse alles, deshalb auf der Unterseite
for lab, num in (("L", "1"), ("Luefter", "4"), ("Licht", "3"), ("N", "2")):
    text(lab, BW - 4.6, pad("X1", num)[1], pcbnew.B_SilkS, 1.0, 0, True)
text("230 V~", 34.0, 43.0, pcbnew.F_SilkS, 1.5, 0, False, 0.25)
text("230 V~", 39.5, 36.5, pcbnew.B_SilkS, 1.0, 0, True, 0.15)
text("Lueftersteuerung Bad v1.2", 42.0, 12.5, pcbnew.B_SilkS, 0.8, 0, True, 0.12)
text("Sensor", W - 4.5, 16.0, pcbnew.F_SilkS, 0.8, 0, False, 0.12)

pcbnew.SaveBoard(PCB, board)
print("gespeichert:", PCB)
for ref in sorted(fps):
    print("  %-4s %s" % (ref, " ".join("%s=(%.2f,%.2f)" % (p_.GetNumber(), pcbnew.ToMM(p_.GetPosition().x) - OX, pcbnew.ToMM(p_.GetPosition().y) - OY) for p_ in list(fps[ref].Pads())[:8])))
