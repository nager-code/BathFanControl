# Setzt Masse-Durchkontaktierungen auf der 3,3-V-Seite: Raster abfahren und nur Positionen nehmen,
# die zu allen Pads, Bahnen, Durchkontaktierungen, Kanten und Sperrflaechen genug Abstand haben.
# Aufruf im KiCad-Python: python3 stitch.py <platine>
import sys, math, pcbnew
pcb = sys.argv[1]
OX = OY = 100.0
mm, tomm = pcbnew.FromMM, pcbnew.ToMM
R, CLR, PITCH = 0.3, 0.3, 3.0        # Via-Radius (0,6 mm), Abstand, Mindestabstand der Vias untereinander
b = pcbnew.LoadBoard(pcb)
gnd = b.FindNet("/GND")
segs, circs, boxes = [], [], []
for t in b.GetTracks():
    if t.GetClass() == "PCB_VIA":
        p = t.GetPosition(); circs.append((tomm(p.x) - OX, tomm(p.y) - OY, tomm(t.GetWidth(pcbnew.F_Cu)) / 2, t.GetNetname()))
    else:
        s, e = t.GetStart(), t.GetEnd()
        segs.append((tomm(s.x) - OX, tomm(s.y) - OY, tomm(e.x) - OX, tomm(e.y) - OY, tomm(t.GetWidth()) / 2, t.GetNetname()))
for fp in b.GetFootprints():
    for p in fp.Pads():
        bb = p.GetBoundingBox()
        boxes.append((tomm(bb.GetLeft()) - OX, tomm(bb.GetTop()) - OY, tomm(bb.GetRight()) - OX, tomm(bb.GetBottom()) - OY))
def dseg(px, py, x1, y1, x2, y2):
    dx, dy = x2 - x1, y2 - y1
    l2 = dx * dx + dy * dy
    u = 0 if l2 == 0 else max(0, min(1, ((px - x1) * dx + (py - y1) * dy) / l2))
    return math.hypot(px - x1 - u * dx, py - y1 - u * dy)
def ok(x, y):
    # 3,3-V-Bereiche der Platine v1.2: Arm oben, Verbindung links, linker Teil des Riegels
    arm = 0.8 <= x <= 57.2 and 0.8 <= y <= 17.2
    steg = 0.8 <= x <= 13.2 and 17.2 < y <= 28.5
    riegel = 0.8 <= x <= 13.0 and 28.5 < y <= 57.2
    if not (arm or steg or riegel): return False
    if x < 16.0 and y < 7.1: return False                       # Antenne
    for x1, y1, x2, y2 in boxes:
        if x1 - R - CLR < x < x2 + R + CLR and y1 - R - CLR < y < y2 + R + CLR: return False
    for x1, y1, x2, y2, w, n in segs:
        if n != "/GND" and dseg(x, y, x1, y1, x2, y2) < R + w + CLR: return False
    for cx, cy, r, n in circs:
        if math.hypot(x - cx, y - cy) < R + r + (CLR if n != "/GND" else 1.0): return False
    return True
placed = []
y = 1.0
while y < 57.5:
    x = 1.0
    while x < 57.5:
        if ok(x, y) and all(math.hypot(x - px, y - py) >= PITCH for px, py in placed):
            placed.append((x, y))
        x += 0.5
    y += 0.5
for x, y in placed:
    v = pcbnew.PCB_VIA(b)
    v.SetPosition(pcbnew.VECTOR2I(mm(OX + x), mm(OY + y))); v.SetViaType(pcbnew.VIATYPE_THROUGH)
    v.SetLayerPair(pcbnew.F_Cu, pcbnew.B_Cu); v.SetWidth(pcbnew.F_Cu, mm(2 * R)); v.SetDrill(mm(0.3)); v.SetNet(gnd)
    b.Add(v)
print("Masse-Durchkontaktierungen gesetzt:", len(placed))
pcbnew.ZONE_FILLER(b).Fill(b.Zones())
pcbnew.SaveBoard(pcb, b)
