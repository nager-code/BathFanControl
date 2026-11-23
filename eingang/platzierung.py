# Grobplatzierung fuer die Lueftersteuerung (70 x 30 mm)
# Aufruf: KiCad Platineneditor -> Werkzeuge -> Skripting-Konsole ->
#   exec(open(r"PFAD/platzierung.py").read())
# Vorher die Netzliste importieren. Die Positionen sind Richtwerte (Bauteilmitte),
# je nach Footprint-Ursprung muss von Hand nachgeschoben werden.
import pcbnew

OX, OY = 100.0, 100.0  # linke obere Platinenecke in mm
board = pcbnew.GetBoard()
mm = pcbnew.FromMM

def pt(x, y):
    return pcbnew.VECTOR2I(mm(OX + x), mm(OY + y))

# Referenz: (x, y, Drehung in Grad, Unterseite)
PLACE = {
    "X1": (4.5, 15.0, 270, False),
    "F1": (15.0, 5.5, 0, False),
    "RV1": (15.0, 14.5, 0, False),
    "R1": (12.5, 20.5, 0, False),
    "R2": (17.5, 20.5, 0, False),
    "R12": (15.0, 24.0, 0, True),
    "PS1": (38.0, 11.5, 0, False),
    "C2": (28.5, 26.5, 0, False),
    "R5": (15.0, 27.0, 0, False),
    "C1": (50.0, 26.5, 0, False),
    "U3": (38.0, 7.0, 0, True),
    "U2": (38.0, 17.5, 180, True),
    "R3": (47.0, 5.0, 90, True),
    "R4": (47.0, 16.0, 90, True),
    "C3": (50.0, 16.0, 90, True),
    "U1": (62.6, 8.8, 0, False),
    "C4": (58.0, 19.5, 0, False),
    "C5": (62.0, 19.5, 0, False),
    "R6": (57.0, 8.0, 90, True),
    "C6": (59.5, 8.0, 90, True),
    "R7": (62.0, 12.0, 90, True),
    "R8": (64.5, 12.0, 90, True),
    "R9": (67.0, 12.0, 90, True),
    "J1": (58.5, 25.0, 90, False),
    "U4": (67.0, 27.0, 0, False),
    "C7": (67.0, 24.0, 0, False),
    "R10": (57.0, 17.0, 0, True),
    "R11": (57.0, 19.5, 0, True),
}

missing = []
for ref, (x, y, rot, bottom) in PLACE.items():
    fp = board.FindFootprintByReference(ref)
    if fp is None:
        missing.append(ref)
        continue
    if bottom and not fp.IsFlipped():
        fp.Flip(fp.GetPosition(), False)
    fp.SetPosition(pt(x, y))
    fp.SetOrientationDegrees(rot)

def line(x1, y1, x2, y2, layer, width=0.1):
    s = pcbnew.PCB_SHAPE(board)
    s.SetShape(pcbnew.SHAPE_T_SEGMENT)
    s.SetStart(pt(x1, y1))
    s.SetEnd(pt(x2, y2))
    s.SetLayer(layer)
    s.SetWidth(mm(width))
    board.Add(s)

# Platinenumriss 70 x 30 mm
for a, b in (((0, 0), (70, 0)), ((70, 0), (70, 30)), ((70, 30), (0, 30)), ((0, 30), (0, 0))):
    line(a[0], a[1], b[0], b[1], pcbnew.Edge_Cuts)

# Hilfslinien auf User.Drawings: Trennlinie Netz / 3,3 V und Schlitze (als Fraesung nachzeichnen)
D = pcbnew.Dwgs_User
line(38.0, 0.5, 38.0, 29.5, D, 0.2)   # Isolationsgrenze unter U2/U3, Schlitz zwischen den Pinreihen
line(62.0, 30.0, 62.0, 21.0, D, 0.2)  # Thermoschlitz Sensor, senkrecht
line(62.0, 21.0, 66.0, 21.0, D, 0.2)  # Thermoschlitz Sensor, waagrecht (Steg rechts stehen lassen)

pcbnew.Refresh()
print("Platziert. Fehlende Referenzen:", missing)
