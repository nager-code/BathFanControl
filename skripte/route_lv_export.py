# Schritt 1 des Autoroutings der 3,3-V-Seite: Hilfsplatine ohne Netzseite und ohne Masse als Specctra-DSN ausgeben.
import sys, pcbnew
SRC, TMP, DSN = sys.argv[1:4]
STEP = int(sys.argv[4]) if len(sys.argv) > 4 else 9
b = pcbnew.LoadBoard(SRC)
MAINS = ("/L", "/L_F", "/N", "/L_LICHT", "/LICHT_A", "/LICHT_B", "/L_FAN", "/SNUB", "/TRIAC_G", "/OPTO_R")
drop = lambda n: n in MAINS or n.startswith("unconnected-")
print("geladen", flush=True)
if STEP >= 1:
    rm = [t for t in b.GetTracks() if drop(t.GetNetname())]
    for t in rm:
        b.Remove(t)
    print("Bahnen entfernt", len(rm), flush=True)
if STEP >= 2:
    rm = [z for z in b.Zones() if not z.GetIsRuleArea()]
    for z in rm:
        b.Remove(z)
    print("Zonen entfernt", len(rm), flush=True)
if STEP >= 4:
    pcbnew.SaveBoard(TMP, b)
    print("gespeichert", flush=True)
if STEP >= 5:
    ok = pcbnew.ExportSpecctraDSN(b, DSN)
    print("DSN:", ok, flush=True)
    # Netze der Netzseite aus der DSN-Datei streichen: deren Pads sind fuer den Router nur Hindernisse.
    import re
    s = open(DSN).read()
    def strip(m):
        name = m.group(1).strip('"')
        return ("(net %s (pins))\n    " % m.group(1)) if drop(name) else m.group(0)
    s2 = re.sub(r'\(net\s+("[^"]*"|\S+)\s*\(pins[^)]*\)\s*\)\s*', strip, s)
    open(DSN, "w").write(s2)
    print("Netze in DSN:", len(re.findall(r'\(net\s', s)), "->", len(re.findall(r'\(net\s', s2)))
