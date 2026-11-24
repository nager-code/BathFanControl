# Passt den uebergebenen Schaltplan an die Datenblattpruefung an und erzeugt die Symbolbibliothek.
import re,sys
src,dst,symlib=sys.argv[1:4]
# Ersatztypen: Referenz -> (Footprint, neuer Wert oder None). Alles SMD ausser Netzklemme X1 und Netzteil PS1 (bedrahtet).
X1_FP, X1_VAL = "lueftersteuerung:Klemme_4pol_P5.08mm_Horizontal_THT", "Schraubklemme 4-pol 5,08"
PS1_FP, PS1_VAL = "Converter_ACDC:Converter_ACDC_Hi-Link_HLK-PMxx", "HLK-PM03"
SMD = {
 "X1":  (X1_FP, X1_VAL),
 "F1":  ("lueftersteuerung:Fuse_SMD_10x3mm_Littelfuse443_UMT250", "T1A 250V 0443001.DR"),
 "RV1": ("lueftersteuerung:Varistor_TDK_CU3225", "CU3225K275G2"),
 "C1":  ("Capacitor_SMD:CP_Elec_6.3x5.8", "100u 25V Hybrid"),
 "C2":  ("lueftersteuerung:C_2220_Murata_GA355_X2", "10n X2 250VAC"),
 "J1":  ("Connector_PinHeader_1.27mm:PinHeader_1x06_P1.27mm_Vertical_SMD_Pin1Left", None),
 "U1":  (None, "ESP32-C3-MINI-1-H4X"),
 "U4":  (None, "SHT40-AD1F"),
}
t=open(src).read()
def sub1(pat,rep,s,flags=0):
    s2,n=re.subn(pat,rep,s,flags=flags)
    assert n>=1,pat
    return s2
# 1) Netzteil bedrahtet, Hi-Link HLK-PM03: Pins laut Datenblatt 1 und 2 = AC (gleichwertig), 3 = -Vo, 4 = +Vo.
#    Im Layout liegt Pin 2 oben (L hinter der Sicherung) und Pin 1 unten (N): deshalb AC/L = 2, AC/N = 1.
i=t.find('(symbol "Luefter:IRM-02-3.3"'); j=t.find('\n    (symbol "Luefter:',i+5)
blk=t[i:j]
for name,old,new_ in (("AC/L","1","2"),("AC/N","2","1")):
    blk=sub1(r'(\(name "%s"[^\n]*?\(number ")%s(")'%(re.escape(name),old),r'\g<1>%s\2'%new_,blk)
t=t[:i]+blk+t[j:]
i=t.find('(property "Reference" "PS1"'); s=t.rfind("(symbol (lib_id",0,i); e=t.find("(instances",s)
blk=t[s:e].replace('"Value" "IRM-02-3.3"','"Value" "%s"'%PS1_VAL)
t=t[:s]+blk+t[e:]
# 1b) Klemme X1: die Pins liegen bei Leitereinfuehrung nach rechts von unten nach oben 1..4.
#     Gewuenschte Reihenfolge von oben: L, Licht, N, Luefter -> L = 4, L_LICHT = 3, N = 2, L_LUEFTER = 1
i=t.find('(symbol "Luefter:KLEMME_4"'); j=t.find('\n    (symbol "Luefter:',i+5)
blk=t[i:j]
for name,old,new_ in (("L","1","4"),("L_LUEFTER","4","1")):
    blk=sub1(r'(\(name "%s"[^\n]*?\(number ")%s(")'%(re.escape(name),old),r'\g<1>%s\2'%new_,blk)
t=t[:i]+blk+t[j:]
# 2) Luefterstufe: statt des Photo-Triacs AQH3223A ein Optotriac MOC3052S (U3), der den Triac ACST410-8B (Q1) zuendet.
#    MOC3052S laut Datenblatt: 1 = Anode, 2 = Kathode, 3 = nicht belegt, 4 und 6 = Ausgang, 5 = Substrat (nicht anschliessen).
#    Das Symbol des AQH3223A wird dazu umnummeriert; der Ausgang geht nicht mehr an L_F / L_FAN, sondern an
#    TRIAC_G (Pin 6, Gate von Q1) und OPTO_R (Pin 4, ueber R16 an L_FAN). Q1, R16 und R17 kommen in Schritt 6 dazu.
i=t.find('(symbol "Luefter:AQH3223A"'); j=t.find('\n    (symbol "Luefter:',i+5)
if j<0: j=t.find('\n  )',i)
PINMAP = {("A","2"):("A","1"), ("K","3"):("K","2"), ("NC","1"):("NC","3"), ("NC","4"):None,
          ("T2","8"):("MT_A","6"), ("T1","6"):("MT_B","4"), ("NC","5"):("SUB","5")}
out=[]; n_=0
for ln in t[i:j].split("\n"):
    m=re.search(r'\(pin passive line .*\(name "([^"]*)".*\(number "([^"]*)"',ln)
    if m:
        neu=PINMAP[(m.group(1),m.group(2))]; n_+=1
        if neu is None: continue
        ln=ln.replace('(name "%s"'%m.group(1),'(name "%s"'%neu[0]).replace('(number "%s"'%m.group(2),'(number "%s"'%neu[1])
    out.append(ln)
assert n_==7
t=t[:i]+"\n".join(out).replace("AQH3223A","MOC3052")+t[j:]
i=t.find('(property "Reference" "U3"'); s=t.rfind("(symbol (lib_id",0,i); e=t.find("(instances",s)
blk=t[s:e].replace('"Luefter:AQH3223A"','"Luefter:MOC3052"').replace('"Value" "AQH3223A"','"Value" "MOC3052S"')
blk=sub1(r'    \(pin "4" \(uuid "[^"]+"\)\)\n','',blk)
for old,new_ in (("2","@1"),("3","@2"),("1","@3"),("8","@6"),("6","@4")):
    blk=sub1(r'\(pin "%s" '%old,'(pin "%s" '%new_,blk)
blk=blk.replace('(pin "@','(pin "')
t=t[:s]+blk+t[e:]
t=sub1(r'  \(no_connect \(at 99\.06 140\.97\) \(uuid "[^"]+"\)\)\n','',t)
# Die beiden Ausgangspins sind gleichwertig; fuer ein kreuzungsfreies Layout geht Pin 6 ans Gate und Pin 4 an R16.
t=sub1(re.escape('(label "L_FAN" (at 127.00 133.35 0)'),'(label "TRIAC_G" (at 127.00 133.35 0)',t)
t=sub1(re.escape('(label "L_F" (at 127.00 135.89 0)'),'(label "OPTO_R" (at 127.00 135.89 0)',t)
# 2b) LTV-814: die beiden AC-Eingangspins sind gleichwertig; getauscht, damit das Layout ohne Kreuzung auskommt
i=t.find('(symbol "Luefter:LTV-814S"'); j=t.find('\n    (symbol "Luefter:',i+5)
if j<0: j=t.find('\n  )',i)
blk=t[i:j]
blk=re.sub(r'(\(number ")1(")', r'\g<1>@@\2', blk); blk=re.sub(r'(\(number ")2(")', r'\g<1>1\2', blk); blk=blk.replace('(number "@@"','(number "2"')
t=t[:i]+blk+t[j:]
# 3) R3 150R -> 100R (LED-Strom des Optotriacs: IFT max 10 mA, hier rund 20 mA)
i=t.find('(property "Reference" "R3"'); k=t.find('"150R"',i); assert 0<k-i<300
t=t[:k]+'"100R"'+t[k+6:]
# 4) Footprints: Projektbibliothek und SMD-Ersatz fuer alle bedrahteten Bauteile
FP = {
 "RF_Module:ESP32-C3-MINI-1": "lueftersteuerung:ESP32-C3-MINI-1",
 "Package_DIP:SMDIP-8_W9.53mm": "lueftersteuerung:MOC3052S_SMDIP-6_W9.53mm",
 "Package_DIP:SMDIP-4_W9.53mm": "lueftersteuerung:LTV-814S_SMDIP-4_W9.53mm",
 "Converter_ACDC:Converter_ACDC_MeanWell_IRM-02-xx_THT": PS1_FP,
 "TerminalBlock_Phoenix:TerminalBlock_Phoenix_MKDS-1,5-4-5.08_1x04_P5.08mm_Horizontal": SMD["X1"][0],
 "Fuse:Fuse_Littelfuse_395Series": SMD["F1"][0],
 "Varistor:RV_Disc_D7mm_W3.4mm_P5mm": SMD["RV1"][0],
 "Capacitor_THT:CP_Radial_D5.0mm_P2.00mm": SMD["C1"][0],
 "Capacitor_THT:C_Rect_L13.0mm_W5.0mm_P10.00mm_FKS3_FKP3_MKS4": SMD["C2"][0],
 "Connector_PinHeader_1.27mm:PinHeader_1x06_P1.27mm_Vertical": SMD["J1"][0],
}
for a,b in FP.items():
    t=sub1(re.escape('"'+a+'"'),'"'+b+'"',t)
# Werte der ersetzten Bauteile
for ref,(fp,val) in SMD.items():
    if val is None: continue
    i=t.find('(property "Reference" "%s"'%ref); k=t.find('(property "Value" "',i); assert 0<k-i<300
    k2=t.find('"',k+len('(property "Value" "'))
    t=t[:k]+'(property "Value" "'+val+t[k2:]
# 5) Nicht bestueckte Teile: R12 (nur bei Bedarf) und J1 (Programmierpads)
for ref in ("R12","J1"):
    i=t.find('(property "Reference" "%s"'%ref); s=t.rfind("(symbol (lib_id",0,i)
    head=t[s:i]
    head2=head.replace("(in_bom yes)","(in_bom no)").replace("(dnp no)","(dnp yes)")
    assert head!=head2
    t=t[:s]+head2+t[i:]
# 6) RGB-LED D1 (gemeinsame Anode an +3V3) mit Vorwiderstaenden R13..R15 an IO4 / IO5 / IO1.
#    Die GPIOs ziehen die Kathoden nach Masse (LED an bei Pegel 0); beim Start sind sie hochohmig, die LED ist aus.
import uuid as _uuid
def uid(tag): return str(_uuid.uuid5(_uuid.NAMESPACE_DNS, "lueftersteuerung-led-" + tag))
ROOT = re.search(r'\(kicad_sch[^\n]*\(uuid "([^"]+)"', t).group(1)
FONT = '(effects (font (size 1.27 1.27)))'
def wire(x1, y1, x2, y2, tag):
    return '  (wire (pts (xy %.2f %.2f) (xy %.2f %.2f)) (stroke (width 0) (type default)) (uuid "%s"))\n' % (x1, y1, x2, y2, uid("w" + tag))
def label(name, x, y, links, tag):
    return '  (label "%s" (at %.2f %.2f %d) (effects (font (size 1.27 1.27)) (justify %s bottom)) (uuid "%s"))\n' % (
        name, x, y, 180 if links else 0, "right" if links else "left", uid("l" + tag))
def inst(lib, ref, val, fp, x, y, pins):
    o = '  (symbol (lib_id "Luefter:%s") (at %.2f %.2f 0) (unit 1) (exclude_from_sim no) (in_bom yes) (on_board yes) (dnp no) (uuid "%s")\n' % (lib, x, y, uid(ref))
    o += '    (property "Reference" "%s" (at %.2f %.2f 0) %s)\n' % (ref, x, y - 8.89 if lib != "R" else y - 6.35, FONT)
    o += '    (property "Value" "%s" (at %.2f %.2f 0) %s)\n' % (val, x, y - 6.35 if lib != "R" else y - 3.81, FONT)
    o += '    (property "Footprint" "%s" (at %.2f %.2f 0) (effects (font (size 1.27 1.27)) (hide yes)))\n' % (fp, x, y)
    o += '    (property "Datasheet" "" (at %.2f %.2f 0) (effects (font (size 1.27 1.27)) (hide yes)))\n' % (x, y)
    for n in pins:
        o += '    (pin "%s" (uuid "%s"))\n' % (n, uid(ref + "p" + n))
    o += '    (instances (project "lueftersteuerung" (path "/%s" (reference "%s") (unit 1))))\n  )\n' % (ROOT, ref)
    return o
# Symbol der LED: links die gemeinsame Anode, rechts die drei Kathoden (Pin-Nummern laut Datenblatt, siehe LED_PINS)
# FM-B2020RGBA-HG laut Datenblatt: 3 = gemeinsame Anode, 1 = rot, 4 = gruen, 2 = blau
LED_PINS = {"A": "3", "RK": "1", "GK": "4", "BK": "2"}
LED_FP, LED_VAL = "lueftersteuerung:LED_RGB_NationStar_FM-B2020", "FM-B2020RGBA-HG"
# Vorwiderstaende rot, gruen, blau fuer je etwa 2-3 mA an 3,3 V (UF typ. 2,0 / 2,7 / 2,8 V; gruen und blau bis 3,2 V)
LED_R = ("680R", "220R", "150R")
def pin(name, x, y, rot): return ('        (pin passive line (at %.2f %.2f %d) (length 2.54) (name "%s" %s) (number "%s" %s))\n'
                                  % (x, y, rot, name, FONT, LED_PINS[name], FONT))
ledsym = ('    (symbol "Luefter:LED_RGB" (pin_names (offset 1.016)) (exclude_from_sim no) (in_bom yes) (on_board yes)\n'
          '      (property "Reference" "D" (at 0 8.89 0) %s)\n      (property "Value" "LED_RGB" (at 0 6.35 0) %s)\n'
          '      (property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))\n'
          '      (property "Datasheet" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))\n'
          '      (symbol "LED_RGB_0_1" (rectangle (start -7.62 5.08) (end 7.62 -5.08) (stroke (width 0.254) (type default)) (fill (type background))))\n'
          '      (symbol "LED_RGB_1_1"\n' % (FONT, FONT)
          + pin("A", -10.16, 0, 0) + pin("RK", 10.16, 2.54, 180) + pin("GK", 10.16, 0, 180) + pin("BK", 10.16, -2.54, 180)
          + '      )\n    )\n')
# Symbol des Triacs ACST410-8B (DPAK): 1 = COM, 2 = OUT (Kuehlfahne), 3 = G
def tpin(name, num, x, y, rot): return ('        (pin passive line (at %.2f %.2f %d) (length 2.54) (name "%s" %s) (number "%s" %s))\n'
                                        % (x, y, rot, name, FONT, num, FONT))
triacsym = ('    (symbol "Luefter:ACST" (pin_names (offset 1.016)) (exclude_from_sim no) (in_bom yes) (on_board yes)\n'
            '      (property "Reference" "Q" (at 0 8.89 0) %s)\n      (property "Value" "ACST" (at 0 6.35 0) %s)\n'
            '      (property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))\n'
            '      (property "Datasheet" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))\n'
            '      (symbol "ACST_0_1" (rectangle (start -7.62 5.08) (end 7.62 -5.08) (stroke (width 0.254) (type default)) (fill (type background))))\n'
            '      (symbol "ACST_1_1"\n' % (FONT, FONT)
            + tpin("G", "3", -10.16, 0, 0) + tpin("OUT", "2", 10.16, 2.54, 180) + tpin("COM", "1", 10.16, -2.54, 180)
            + '      )\n    )\n')
i = t.find('\n    (symbol "Luefter:R"')
t = t[:i + 1] + ledsym + triacsym + t[i + 1:]
# freie Pins des Moduls: IO1 (y 191.77), IO4 (194.31), IO5 (196.85) bekommen statt des Kreuzes ein Netz
neu_el = ""
for y, name in ((194.31, "LED_R_IO4"), (196.85, "LED_G_IO5"), (191.77, "LED_B_IO1")):
    t = sub1(r'  \(no_connect \(at 63\.50 %s\) \(uuid "[^"]+"\)\)\n' % ("%.2f" % y).replace(".", r"\."), "", t)
    neu_el += wire(63.50, y, 66.04, y, name) + label(name, 66.04, y, False, "u1" + name)
# Vorwiderstaende und LED in einer Reihe unter den Pull-ups
YL = 213.36
for x, ref, val, io, k in ((111.76, "R13", LED_R[0], "LED_R_IO4", "LED_RK"), (172.72, "R14", LED_R[1], "LED_G_IO5", "LED_GK"),
                           (233.68, "R15", LED_R[2], "LED_B_IO1", "LED_BK")):
    neu_el += inst("R", ref, val, "Resistor_SMD:R_0603_1608Metric", x, YL, ("1", "2"))
    neu_el += wire(x - 6.35, YL, x - 8.89, YL, ref + "a") + label(io, x - 8.89, YL, True, ref + "a")
    neu_el += wire(x + 6.35, YL, x + 8.89, YL, ref + "b") + label(k, x + 8.89, YL, False, ref + "b")
XD = 294.64
neu_el += inst("LED_RGB", "D1", LED_VAL, LED_FP, XD, YL, (LED_PINS["A"], LED_PINS["RK"], LED_PINS["GK"], LED_PINS["BK"]))
neu_el += wire(XD - 10.16, YL, XD - 12.70, YL, "d1a") + label("+3V3", XD - 12.70, YL, True, "d1a")
for dy, k in ((-2.54, "LED_RK"), (0, "LED_GK"), (2.54, "LED_BK")):
    neu_el += wire(XD + 10.16, YL + dy, XD + 12.70, YL + dy, "d1" + k) + label(k, XD + 12.70, YL + dy, False, "d1" + k)
# Triacstufe des Luefters: R16 begrenzt den Zuendstrom (Spitze 358 V / 390 Ohm = 0,92 A, Optotriac vertraegt 1 A),
# R17 leitet Leckstrom am Gate ab. Q1: COM an L_F (hinter der Sicherung), OUT an L_FAN (zur Klemme).
YT_ = 152.40
neu_el += inst("R", "R16", "390R", "Resistor_SMD:R_1206_3216Metric", 172.72, YT_, ("1", "2"))
neu_el += wire(166.37, YT_, 163.83, YT_, "r16a") + label("OPTO_R", 163.83, YT_, True, "r16a")
neu_el += wire(179.07, YT_, 181.61, YT_, "r16b") + label("L_FAN", 181.61, YT_, False, "r16b")
neu_el += inst("R", "R17", "390R", "Resistor_SMD:R_0603_1608Metric", 233.68, YT_, ("1", "2"))
neu_el += wire(227.33, YT_, 224.79, YT_, "r17a") + label("TRIAC_G", 224.79, YT_, True, "r17a")
neu_el += wire(240.03, YT_, 242.57, YT_, "r17b") + label("L_F", 242.57, YT_, False, "r17b")
neu_el += inst("ACST", "Q1", "ACST410-8B", "lueftersteuerung:DPAK_ST_ACST4", 294.64, YT_, ("3", "2", "1"))
neu_el += wire(284.48, YT_, 281.94, YT_, "q1g") + label("TRIAC_G", 281.94, YT_, True, "q1g")
neu_el += wire(304.80, YT_ - 2.54, 307.34, YT_ - 2.54, "q1o") + label("L_FAN", 307.34, YT_ - 2.54, False, "q1o")
neu_el += wire(304.80, YT_ + 2.54, 307.34, YT_ + 2.54, "q1c") + label("L_F", 307.34, YT_ + 2.54, False, "q1c")
neu_el += ('  (text "Optotriac U3 zuendet Triac Q1; Snubber R5/C2 parallel zu Q1" (exclude_from_sim no) (at 157.48 144.78 0) '
           '(effects (font (size 1.27 1.27)) (justify left bottom)) (uuid "%s"))\n' % uid("text2"))
neu_el += ('  (text "Anzeige: RGB-LED (leuchtet bei Pegel 0)" (exclude_from_sim no) (at 96.52 205.74 0) '
           '(effects (font (size 1.27 1.27)) (justify left bottom)) (uuid "%s"))\n' % uid("text"))
i = t.rfind("\n  (sheet_instances")
if i < 0: i = t.rstrip().rfind("\n)")
t = t[:i + 1] + neu_el + t[i + 1:]
open(dst,"w").write(t)
# Symbolbibliothek aus den eingebetteten Symbolen
i=t.find('(lib_symbols'); depth=0
for k in range(i,len(t)):
    if t[k]=='(': depth+=1
    elif t[k]==')':
        depth-=1
        if depth==0: break
body=t[i+len('(lib_symbols'):k].replace('(symbol "Luefter:','(symbol "')
open(symlib,"w").write('(kicad_symbol_lib (version 20231120) (generator "kicad_symbol_editor") (generator_version "8.0")'+body+')\n')
print("ok")
