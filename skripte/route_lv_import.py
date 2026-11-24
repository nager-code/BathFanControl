# Schritt 2 des Autoroutings: Ergebnis (Specctra-SES) in die Hilfsplatine laden und die Bahnen der
# 3,3-V-Signale in die eigentliche Platine uebernehmen. Danach Masseflaechen fuellen.
import sys, pcbnew
MAIN, TMP, SES = sys.argv[1:4]
tmp = pcbnew.LoadBoard(TMP)
print("SES:", pcbnew.ImportSpecctraSES(tmp, SES), flush=True)
b = pcbnew.LoadBoard(MAIN)
MAINS = ("/L", "/L_F", "/N", "/L_LICHT", "/LICHT_A", "/LICHT_B", "/L_FAN", "/SNUB", "/TRIAC_G", "/OPTO_R")
key = lambda t: (t.GetClass(), t.GetLayer(), t.GetStart().x, t.GetStart().y, t.GetEnd().x, t.GetEnd().y)
have = set(key(t) for t in b.GetTracks())
n = 0
for t in tmp.GetTracks():
    name = t.GetNetname()
    if name in MAINS or not name or key(t) in have:
        continue
    net = b.FindNet(name)
    if t.GetClass() == "PCB_VIA":
        v = pcbnew.PCB_VIA(b)
        v.SetPosition(t.GetPosition()); v.SetViaType(pcbnew.VIATYPE_THROUGH); v.SetLayerPair(pcbnew.F_Cu, pcbnew.B_Cu)
        v.SetWidth(pcbnew.F_Cu, t.GetWidth(pcbnew.F_Cu)); v.SetDrill(t.GetDrill()); v.SetNet(net)
        b.Add(v)
    else:
        s = pcbnew.PCB_TRACK(b)
        s.SetStart(t.GetStart()); s.SetEnd(t.GetEnd()); s.SetWidth(t.GetWidth()); s.SetLayer(t.GetLayer()); s.SetNet(net)
        b.Add(s)
    n += 1
print("uebernommen:", n, flush=True)
pcbnew.SaveBoard(MAIN, b)
