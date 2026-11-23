# Erzeugt die Platine der Lueftersteuerung (70 x 30 mm, 2 Lagen) aus der Schaltplan-Netzliste.
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
W, H = 70.0, 30.0
mm = pcbnew.FromMM
F, B = pcbnew.F_Cu, pcbnew.B_Cu
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from x1_param import X1, X1X
X1LABELX = X1X + X1["body"][1] + 0.2

def P(x, y):
    return pcbnew.VECTOR2I(mm(OX + x), mm(OY + y))

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
PLACE = {
    # ref: (Ursprung x, y, Unterseite, Pad-Nr., Soll-Lage dieses Pads) - die Drehung wird daraus bestimmt
    # Oberseite: Klemme, Netzteil, WLAN-Modul, Elko, Sensor
    "X1":  (X1X, 15.0, False, "2", (X1X - 5.25, 6.0)),          # von oben: N, Licht, Luefter, L
    "PS1": (35.6, 15.0, False, "24", (21.63, 1.765)),          # AC links (N oben, L unten), 3,3 V rechts
    "U1":  (62.6, 8.8, False, "3", (56.7, 9.1)),
    "C1":  (56.4, 24.9, False, "1", (56.4, 22.1)),
    "U4":  (66.4, 26.2, False, "1", (65.7, 25.8)),
    "C7":  (68.4, 26.2, False, "1", (68.4, 26.975)),
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
    "R3":  (44.8, 18.23, True, "2", (43.975, 18.23)),
    "J1":  (50.1, 22.0, True, "1", (51.6, 18.825)),
    "C5":  (55.2, 9.1, True, "1", (55.975, 9.1)),
    "C4":  (55.2, 11.4, True, "1", (56.15, 11.4)),
    "R9":  (59.6, 10.1, True, "2", (58.775, 10.1)),
    "R6":  (59.6, 12.5, True, "2", (58.775, 12.5)),
    "C6":  (59.6, 14.6, True, "1", (58.825, 14.6)),
    "R10": (61.4, 18.7, True, "2", (61.4, 17.875)),
    "R11": (63.2, 18.7, True, "2", (63.2, 17.875)),
    "R8":  (65.0, 18.7, True, "2", (65.0, 17.875)),
    "R7":  (66.8, 18.7, True, "2", (66.8, 17.875)),
}
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

# Aussenkontur mit Thermoschlitz um den Sensor (1 mm breit, senkrecht bei x = 62, waagrecht bei y = 21,
# rechts bleibt ein Steg von x = 66 bis 70)
edge_poly([(0, 0), (W, 0), (W, H), (62.5, H), (62.5, 21.5), (66.0, 21.5), (66.0, 20.5),
           (61.5, 20.5), (61.5, H), (0, H)])
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
slot(36.9, 4.5, 24.5, 2.0)

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

zone(rect(33.75, 0, 40.05, H), [F, B], rule=("tracks", "vias", "fill"), name="Isolation Netz / 3,3 V")
zone(rect(55.6, 0, W, 6.1), [F, B], rule=("tracks", "vias", "fill"), name="Antenne U1")
zone(rect(62.5, 20.0, W, H), [F, B], rule=("fill",), name="Sensorinsel ohne Flaeche")
# Randstreifen fuer den Autorouter: keine Bahnen/Durchkontaktierungen dicht an Kante und Thermoschlitz
for i_, r_ in enumerate((rect(69.65, 6.1, W, 30.0), rect(40.05, 0.0, 55.6, 0.45), rect(40.05, 29.55, 61.5, H),
                         rect(61.0, 20.0, 66.45, 22.0), rect(61.0, 22.0, 63.0, H))):
    zone(r_, [F, B], rule=("tracks", "vias"), name="Rand %d" % (i_ + 1))
zone(rect(40.1, 0.0, W, H), [F, B], netname="/GND", name="GND")

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

# --- Netzseite (von Hand, 1,0 mm; nach den 2 x 100 k duenner)
# Oberseite: Klemme und Netzteil. Unterseite: Sicherung, Varistor, Snubber, Optokoppler.
# An der Klemme liegen von oben nach unten N, Licht, Luefter, L - so kreuzt auf keiner Lage etwas.
def xpads(num):
    ps = sorted([p_.GetPosition() for p_ in fps["X1"].Pads() if p_.GetNumber() == num], key=lambda q: q.x)
    return [(pcbnew.ToMM(q.x) - OX, pcbnew.ToMM(q.y) - OY) for q in ps]
(NF, NR), (LLF, LLR), (LFF, LFR), (LF_, LR_) = xpads("2"), xpads("3"), xpads("4"), xpads("1")
for n_, a_, b_ in (("/N", NF, NR), ("/L_LICHT", LLF, LLR), ("/L_FAN", LFF, LFR), ("/L", LF_, LR_)):
    track(n_, [a_, b_], 1.0, F)            # vordere und hintere Loetflaeche jedes Pols verbinden
VN, VLL, VLF, VLFT, VL = (19.0, 4.0), (20.2, 11.3), (20.3, 15.69), (23.4, 27.9), (9.0, 24.0)
# N: Klemme -> Netzteil AC/N (oben), Durchkontaktierung, unten zu Varistor und Optokoppler
psn, psl = pad("PS1", "24"), pad("PS1", "1")
track("/N", [NR, (17.6, 6.0), VN, (psn[0], 2.3), psn], 1.0, F)
via("/N", VN, 1.2, 0.6)
u22 = pad("U2", "2")
track("/N", [VN, (19.6, 3.4), (28.8, 3.4), (30.9, 5.5), (30.9, u22[1]), u22], 1.0, B)
rv2 = pad("RV1", "2")
track("/N", [rv2, (rv2[0], 4.6), (rv2[0] + 1.2, 3.4), (19.6, 3.4)], 1.0, B)
track("/N", [pad("R12", "2"), (30.9, u22[1])], 0.5, B)
# Lichteingang: Klemme (oben) -> Durchkontaktierung -> R1 -> R2 -> Optokoppler (unten)
track("/L_LICHT", [LLR, (18.5, 12.0), VLL], 1.0, F)
via("/L_LICHT", VLL, 1.2, 0.6)
track("/L_LICHT", [VLL, pad("R1", "1")], 1.0, B)
track("/LICHT_A", [pad("R1", "2"), pad("R2", "1")], 1.0, B)
u21 = pad("U2", "1")
r22 = pad("R2", "2")
track("/LICHT_B", [r22, (r22[0] + 1.14, 10.16), (31.3, u21[1]), u21], 0.4, B)
track("/LICHT_B", [pad("R12", "1"), (31.0, u21[1]), u21], 0.4, B)
# L_FAN: Klemme (oben) -> Durchkontaktierung -> Snubber-Kondensator -> Triac (unten)
track("/L_FAN", [LFR, (18.5, 18.0), VLF], 1.0, F)
via("/L_FAN", VLF, 1.2, 0.6)
track("/L_FAN", [VLF, pad("C2", "2"), pad("U3", "8")], 1.0, B)
# L: Durchkontaktierung unter der Klemme -> Sicherung (unten)
via("/L", VL, 1.2, 0.6)
f11 = pad("F1", "1")
track("/L", [VL, (f11[0] + 0.6, 26.2), f11], 1.0, B)
# L_F: Sicherung -> Varistor, Snubber-Widerstand, Triac (unten) und Netzteil AC/L (oben)
f12 = pad("F1", "2")
u36 = pad("U3", "6")
track("/L_F", [f12, (f12[0] + 0.6, 26.3), (29.9, 26.3), (29.9, u36[1] + 1.03), (30.93, u36[1]), u36], 1.0, B)
r51 = pad("R5", "1")
track("/L_F", [r51, (r51[0], 26.3)], 1.0, B)
rv1 = pad("RV1", "1")
track("/L_F", [rv1, (rv1[0], 23.4), (f12[0], 25.775), f12], 1.0, B)
track("/L_F", [(23.4, 26.3), VLFT], 1.0, B)
via("/L_F", VLFT, 1.2, 0.6)
track("/L_F", [VLFT, psl], 1.0, F)
# Snubber: C2 -> R5
track("/SNUB", [pad("C2", "1"), pad("R5", "2")], 1.0, B)

# --- Sensorinsel (von Hand, 0,2 mm, durch den Steg rechts vom Thermoschlitz)
sda, scl, vdd, vss = pad("U4", "1"), pad("U4", "2"), pad("U4", "3"), pad("U4", "4")
c71, c72 = pad("C7", "1"), pad("C7", "2")
# Pads des Sensors nur von aussen anfahren (Sperrflaeche des Footprints unter dem Sensor)
track("/SCL_IO7", [(66.6, 19.6), (66.6, 22.0), (64.4, 24.2), (64.4, scl[1]), (65.5, scl[1])], 0.2, F)
track("/SDA_IO6", [(67.1, 19.6), (67.1, 22.4), (64.95, 24.55), (64.95, sda[1]), (65.5, sda[1])], 0.2, F)
track("/GND", [(67.9, 18.4), (67.9, 24.3), (68.4, 24.8), c72], 0.25, F)
track("/GND", [c72, (67.7, c72[1]), (67.3, vss[1])], 0.2, F)
track("/+3V3", [(69.3, 19.2), (69.3, 27.7), (69.0, 28.0), (68.4, 28.0), c71], 0.25, F)
track("/+3V3", [c71, (67.7, c71[1]), (67.3, vdd[1])], 0.2, F)
via("/GND", (67.9, 18.4), 0.6, 0.3)
# Masseflaeche unter dem WLAN-Modul ueber dessen Massepad (EPAD) an die Unterseite anbinden
via("/GND", (62.6, 11.5), 0.6, 0.3)
via("/GND", (64.575, 13.475), 0.6, 0.3)
# Massepad der Programmierpads direkt durchkontaktieren (unbestueckt, daher unkritisch)
j12 = pad("J1", "2")
via("/GND", (j12[0] - 1.0, j12[1]), 0.6, 0.3)
# 3,3 V der Sensorinsel haengt am Pull-up R7 (Unterseite)
via("/+3V3", (69.3, 19.2), 0.6, 0.3)
r71 = pad("R7", "1")
track("/+3V3", [(69.3, 19.2), (68.6, 19.9), (67.5, 19.9), (67.0, r71[1] + 0.2), r71], 0.25, B)

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
for lab, p_ in (("N", NF), ("Licht", LLF), ("Luefter", LFF), ("L", (LF_[0], LF_[1] - 2.2))):
    text(lab, 4.6, p_[1], pcbnew.B_SilkS, 1.0, 0, True)
text("230 V~", 18.2, 21.3, pcbnew.B_SilkS, 1.0, 90, True, 0.15)
text("230 V~", 27.3, 15.0, pcbnew.F_SilkS, 1.5, 0, False, 0.25)
text("Lueftersteuerung Bad v1.1", 50.0, 4.2, pcbnew.B_SilkS, 0.8, 0, True, 0.12)
text("3V3 GND TX RX IO9 EN", 54.4, 22.0, pcbnew.B_SilkS, 0.7, 90, True, 0.12)

pcbnew.SaveBoard(PCB, board)
print("gespeichert:", PCB)
for ref in sorted(fps):
    print("  %-4s %s" % (ref, " ".join("%s=(%.2f,%.2f)" % (p_.GetNumber(), pcbnew.ToMM(p_.GetPosition().x) - OX, pcbnew.ToMM(p_.GetPosition().y) - OY) for p_ in list(fps[ref].Pads())[:8])))
