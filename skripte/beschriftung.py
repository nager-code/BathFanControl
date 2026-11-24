# Ergaenzt den Bestueckungsdruck der fertig gerouteten Platine um Beschriftungen und stellt sicher, dass kein Text
# kleiner als das Mindestmass des Fertigers ist (JLCPCB: Schrifthoehe 1,0 mm, Strichstaerke 0,15 mm).
# Aufruf im KiCad-Python: python3 beschriftung.py <platine.kicad_pcb>
import sys, pcbnew
pcb = sys.argv[1]
OX = OY = 100.0
H = 68.0                               # Oberkante der Platine ueber y = 0 (Unterkante des Netzteil-Riegels)
HMIN, DMIN = 1.0, 0.15
mm = pcbnew.FromMM
b = pcbnew.LoadBoard(pcb)
NEU = []                               # (Text, x, y, Unterseite, Groesse, Drehung, rechtsbuendig)
def text(s, x, y, unten=False, size=1.0, rot=0, rechts=False):
    NEU.append((s, x, y, unten, size, rot, rechts))
# ---- Oberseite (x, Hoehe y ueber der Unterkante des Riegels)
# Klemmenbelegung: je Pol ein Name direkt hinter der Klemme, sichtbar bei eingelegter Platine und offenem Deckel
for name, y in (("L", 22.62), ("Licht", 17.54), ("N", 12.46), ("Lüfter", 7.38)):
    text(name, 44.3, y, size=1.1, rechts=True)
TITEL = "Lüftersteuerung Bad V1.0"
text(TITEL, 19.6, -2.6)
text("BOOT", 21.5, 50.3); text("RST", 25.6, 50.3)
text("USB", 37.9, 64.0, rot=90)
text("LED", 35.3, 61.2)
text("F1 T1A", 56.2, 37.5)
text("Q1", 21.8, 31.7)
text("U3", 26.3, 46.4); text("U2", 50.5, 46.4)
text("C1", 24.0, 58.2)
text("U5", 40.2, 54.2)
text("3,3 V", 5.0, 35.5, size=1.2)
# ---- Unterseite: Stifte des Netzteils, Bereiche
text("AC N", 29.8, 12.5, True); text("AC L", 29.8, 17.5, True)
text("GND", 8.8, 7.5, True); text("+3V3", 9.2, 22.5, True)
text("3,3 V", 6.5, 36.0, True, 1.2)
text("USB", 44.0, 60.6, True); text("Sensor", 63.6, 59.5, True)
# Die Liste der Zeichnungselemente nur einmal holen: nach Remove/Add liefert die KiCad-Schnittstelle sie nicht mehr.
texte = [d for d in b.GetDrawings() if d.GetClass() == "PCB_TEXT" and d.GetLayer() in (pcbnew.F_SilkS, pcbnew.B_SilkS)]
schon = set((t_[0], pcbnew.B_SilkS if t_[3] else pcbnew.F_SilkS) for t_ in NEU)
alt = [d for d in texte if (d.GetText(), d.GetLayer()) in schon]          # Texte eines frueheren Laufs
# Mindestmass und einheitliche Schreibweise fuer die uebrigen Texte (aus build_board.py)
n = 0
for d in texte:
    if d in alt: continue
    if d.GetText().startswith("Lüftersteuerung Bad") or d.GetText().startswith("Lueftersteuerung Bad"):   # Titel mit altem Versionsstand
        if d.GetLayer() == pcbnew.F_SilkS: alt.append(d); continue
        d.SetText(TITEL)
    if "Lueft" in d.GetText(): d.SetText(d.GetText().replace("Lueft", "Lüft"))
    if d.GetText() == "230 V~" and d.GetLayer() == pcbnew.B_SilkS:
        d.SetPosition(pcbnew.VECTOR2I(mm(OX + 31.0), mm(OY + H + 2.3)))       # unten im Streifen, nicht zwischen den Stiften
    sz = d.GetTextSize()
    if pcbnew.ToMM(sz.y) < HMIN or pcbnew.ToMM(sz.x) < HMIN:
        d.SetTextSize(pcbnew.VECTOR2I(mm(max(HMIN, pcbnew.ToMM(sz.x))), mm(max(HMIN, pcbnew.ToMM(sz.y))))); n += 1
    if pcbnew.ToMM(d.GetTextThickness()) < DMIN:
        d.SetTextThickness(mm(DMIN))
for d in alt:
    b.Remove(d)
for s_, x, y, unten, size, rot, rechts in NEU:
    t = pcbnew.PCB_TEXT(b)
    t.SetText(s_); t.SetPosition(pcbnew.VECTOR2I(mm(OX + x), mm(OY + H - y)))
    t.SetLayer(pcbnew.B_SilkS if unten else pcbnew.F_SilkS)
    t.SetTextSize(pcbnew.VECTOR2I(mm(size), mm(size))); t.SetTextThickness(mm(max(DMIN, size * 0.15)))
    t.SetTextAngleDegrees(rot); t.SetMirrored(unten)
    if rechts: t.SetHorizJustify(pcbnew.GR_TEXT_H_ALIGN_RIGHT)
    b.Add(t)
pcbnew.SaveBoard(pcb, b)
print("Beschriftung: %d Texte gesetzt, %d vergroessert" % (len(NEU), n))
