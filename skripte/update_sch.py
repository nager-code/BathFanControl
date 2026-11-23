# Passt den uebergebenen Schaltplan an die Datenblattpruefung an und erzeugt die Symbolbibliothek.
import re,sys
src,dst,symlib=sys.argv[1:4]
# SMD-Ersatztypen: Referenz -> (Footprint, neuer Wert oder None)
SMD = {
 "X1":  ("lueftersteuerung:WAGO_2061-602_2x_SMD", "2x WAGO 2061-602"),
 "F1":  ("lueftersteuerung:Fuse_SMD_10x3mm_Littelfuse443_UMT250", "T1A 250V 0443001.DR"),
 "RV1": ("lueftersteuerung:Varistor_TDK_CU3225", "CU3225K275G2"),
 "C1":  ("Capacitor_SMD:CP_Elec_6.3x5.4", "100u 16V"),
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
# 1) Netzteil als SMD-Ausfuehrung IRM-02-3.3S: Pins laut Datenblatt 1 = AC/L, 24 = AC/N, 12 = +Vo, 13 = -Vo
i=t.find('(symbol "Luefter:IRM-02-3.3"'); j=t.find('\n    (symbol "Luefter:',i+5)
blk=t[i:j]
for name,old,new_ in (("AC/L","1","1"),("AC/N","2","24"),("+Vo","4","12"),("-Vo","3","13")):
    blk=sub1(r'(\(name "%s"[^\n]*?\(number ")%s(")'%(re.escape(name),old),r'\g<1>%s\2'%new_,blk)
t=t[:i]+blk+t[j:]
i=t.find('(property "Reference" "PS1"'); s=t.rfind("(symbol (lib_id",0,i); e=t.find("(instances",s)
blk=t[s:e]
for old,new_ in (("2","24"),("4","12"),("3","13")):
    blk=sub1(r'\(pin "%s" '%old,'(pin "%s" '%new_,blk)
blk=blk.replace('"Value" "IRM-02-3.3"','"Value" "IRM-02-3.3S"')
t=t[:s]+blk+t[e:]
# 2) AQH3223A: Pins 1/4 intern an Kathode, Pin 5 = Gate
i=t.find('(symbol "Luefter:AQH3223A"'); j=t.find('\n    (symbol "Luefter:',i+5)
if j<0: j=t.find('\n  )',i)
blk=t[i:j]
for num,name in (("1","K_INT"),("4","K_INT"),("5","GATE_OFFEN")):
    blk=sub1(r'\(name "NC"([^\n]*?\(number "%s")'%num,r'(name "%s"\1'%name,blk)
t=t[:i]+blk+t[j:]
# 3) R3 150R -> 100R (LED-Strom AQH3223A: IFT max 10 mA, empfohlen 15-25 mA)
i=t.find('(property "Reference" "R3"'); k=t.find('"150R"',i); assert 0<k-i<300
t=t[:k]+'"100R"'+t[k+6:]
# 4) Footprints: Projektbibliothek und SMD-Ersatz fuer alle bedrahteten Bauteile
FP = {
 "RF_Module:ESP32-C3-MINI-1": "lueftersteuerung:ESP32-C3-MINI-1",
 "Package_DIP:SMDIP-8_W9.53mm": "lueftersteuerung:AQH3223A_SMD-8-N7",
 "Package_DIP:SMDIP-4_W9.53mm": "lueftersteuerung:LTV-814S_SMDIP-4_W9.53mm",
 "Converter_ACDC:Converter_ACDC_MeanWell_IRM-02-xx_THT": "Converter_ACDC:Converter_ACDC_MeanWell_IRM-02-xx_SMD",
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
