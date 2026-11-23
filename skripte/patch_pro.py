# Traegt Netzklassen und Entwurfsregeln in die Projektdatei ein (liegen bei KiCad nicht in der .kicad_pcb).
import json, sys, copy
p = sys.argv[1]
d = json.load(open(p))
ns = d["net_settings"]
base = ns["classes"][0]
base.update(clearance=0.2, track_width=0.25, via_diameter=0.6, via_drill=0.3)
def cls(name, prio, **kw):
    c = copy.deepcopy(base); c.update(name=name, priority=prio, **kw); return c
ns["classes"] = [base,
    cls("Netz", 0, clearance=0.5, track_width=1.0, via_diameter=1.2, via_drill=0.6),
    cls("Versorgung", 1, clearance=0.2, track_width=0.4, via_diameter=0.7, via_drill=0.3)]
mains = ["/L", "/L_F", "/N", "/L_LICHT", "/LICHT_A", "/LICHT_B", "/L_FAN", "/SNUB", "unconnected-(U3-GATE_OFFEN-Pad5)"]
ns["netclass_patterns"] = [{"netclass": "Netz", "pattern": n} for n in mains] + \
                          [{"netclass": "Versorgung", "pattern": n} for n in ("/+3V3", "/GND")]
r = d["board"]["design_settings"]["rules"]
r.update(min_clearance=0.15, min_copper_edge_clearance=0.3, min_hole_clearance=0.2, min_hole_to_hole=0.25,
         min_track_width=0.15, min_via_diameter=0.5, min_through_hole_diameter=0.3, min_via_annular_width=0.1,
         min_text_height=0.7, min_text_thickness=0.1)
json.dump(d, open(p, "w"), indent=2)
print("Projektdatei aktualisiert")
