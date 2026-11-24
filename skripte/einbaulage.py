# Zeichnet die Einbaulage im Luefterkasten als SVG: wo das Gehaeuse sitzt und wo der Feuchtesensor liegt.
# Die Lage von Einlass, Wartungsoeffnung und Kabeltasche ist aus einem Foto geschaetzt (+-10 %); das Foto selbst
# liegt nicht im Repo. Aufruf: python3 einbaulage.py <ausgabe.svg>
import sys, html, math
out = sys.argv[1]
# ---- Masse in mm, Ursprung = innere Ecke unten links im Luefterkasten, y nach oben
GB, GH, GT = 72.6, 77.1, 25.7          # Gehaeuse: Breite, Hoehe, Tiefe
FASE = 7.35                             # abgeschraegte Ecke oben rechts
SENSOR = (65.5, 62.8)                   # Feuchtesensor im Gehaeuse
KAMMER_X, KAMMER_Y = 60.5, 49.3         # Sensorkammer: ab hier nach rechts / oben
RAUM = (85.0, 140.0, 40.0)              # frei laut Messung: Breite, Hoehe, Tiefe
EINLASS = (110.0, 101.0)                # Mitte der Ansaugoeffnung (aus Foto)
R_OEFFNUNG, R_RAND, R_NABE = 40.0, 53.0, 31.0
KLAPPE = (50.0, 76.0, 69.0, 105.0)      # Wartungsoeffnung der Rueckstauklappe (aus Foto)
TASCHE = (78.0, 2.0, 150.0, 50.0)       # Kabeltasche mit den Leitungen (aus Foto)
ADERN = [("L", 29.4), ("Licht", 24.3), ("N", 19.3), ("Lüfter", 14.2)]
BX, BY = 165.0, 160.0                   # gezeichneter Ausschnitt des Kastens
K = 1.55                                # Zeichenmassstab
OX, OY = 26.0, 24.0
def X(x): return OX + x * K
def Y(y): return OY + (BY - y) * K
S = []
def add(s): S.append(s)
def text(x, y, t, fs=3.0, col="#222", anchor="start", bold=False, extra=""):
    add('<text x="%.1f" y="%.1f" font-size="%.1f" text-anchor="%s" fill="%s"%s%s>%s</text>' % (x, y, fs, anchor, col, ' font-weight="bold"' if bold else "", extra, html.escape(t)))
TW, TH = X(BX) + 96, Y(0) + 24
add('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %.0f %.0f" width="%.0fmm" height="%.0fmm" font-family="DejaVu Sans, Arial, sans-serif">' % (TW, TH, TW, TH))
add('<defs><marker id="pf" markerUnits="userSpaceOnUse" markerWidth="5" markerHeight="5" refX="4" refY="2.5" orient="auto"><path d="M0,0.3 L4.6,2.5 L0,4.7 z" fill="#2a7fbf"/></marker>'
    '<pattern id="sch" width="3" height="3" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="3" height="3" fill="#d9f2df"/><line x1="0" y1="0" x2="0" y2="3" stroke="#1b7a3d" stroke-width="0.7"/></pattern></defs>')
add('<rect width="100%" height="100%" fill="#ffffff"/>')
text(8, 10, "Einbaulage im Lüfterkasten: wo der Feuchtesensor sitzt", 4.6, bold=True)
text(8, 16, "Blick von vorn in den geöffneten Kasten (Frontabdeckung abgenommen), unten links die Steuerung", 3.0, "#555")
# ---- Kasten
add('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="#f3efe6"/>' % (X(0), Y(BY), BX * K, BY * K))
add('<path d="M%.1f %.1f L%.1f %.1f L%.1f %.1f" fill="none" stroke="#6b5f4f" stroke-width="2.4" stroke-linejoin="miter"/>' % (X(0), Y(BY), X(0), Y(0), X(BX), Y(0)))
text(X(0) - 2.5, Y(BY / 2), "linke Kastenwand", 2.7, "#6b5f4f", "middle", extra=' transform="rotate(-90 %.1f %.1f)"' % (X(0) - 2.5, Y(BY / 2)))
text(X(BX) - 1, Y(0) + 5.2, "Kastenboden", 2.7, "#6b5f4f", "end")
# ---- Lueftergehaeuse: Rand, Ansaugoeffnung, Nabe
cx, cy = X(EINLASS[0]), Y(EINLASS[1])
add('<clipPath id="kasten"><rect x="%.1f" y="%.1f" width="%.1f" height="%.1f"/></clipPath><g clip-path="url(#kasten)">' % (X(0), Y(BY), BX * K, BY * K))
add('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#e9e3d6" stroke="#b9ae99" stroke-width="0.6"/>' % (cx, cy, R_RAND * K))
add('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#3b3b3b"/>' % (cx, cy, R_OEFFNUNG * K))
for i in range(8):
    a = math.radians(22.5 + 45 * i)
    add('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#d8d0c0" stroke-width="1.6"/>' % (cx + R_NABE * K * math.cos(a), cy + R_NABE * K * math.sin(a), cx + (R_OEFFNUNG + 4) * K * math.cos(a), cy + (R_OEFFNUNG + 4) * K * math.sin(a)))
add('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#4f79c7"/>' % (cx, cy, R_NABE * K))
add('</g>')
text(cx, cy - 2, "Lüfter", 3.4, "#fff", "middle", True)
text(cx, cy + 3.2, "Ansaugöffnung", 2.8, "#fff", "middle")
# ---- Wartungsoeffnung und Kabeltasche
x0, y0, x1, y1 = KLAPPE
add('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="5" fill="#ece6d8" stroke="#a89c86" stroke-width="0.6"/>' % (X(x0), Y(y1), (x1 - x0) * K, (y1 - y0) * K))
text(X((x0 + x1) / 2), Y((y0 + y1) / 2) + 1, "Wartungsöffnung", 2.3, "#7a6e5a", "middle", extra=' transform="rotate(-90 %.1f %.1f)"' % (X((x0 + x1) / 2), Y((y0 + y1) / 2) + 1))
x0, y0, x1, y1 = TASCHE
add('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="6" fill="#e6dfd0" stroke="#a89c86" stroke-width="0.6" stroke-dasharray="2.5 1.6"/>' % (X(x0), Y(y1), (x1 - x0) * K, (y1 - y0) * K))
text(X(x1) - 3, Y(y0) - 3, "Kabeltasche mit den Leitungen", 2.6, "#7a6e5a", "end")
# ---- freier Raum laut Messung
add('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="none" stroke="#d07000" stroke-width="0.7" stroke-dasharray="3 2"/>' % (X(0), Y(RAUM[1]), RAUM[0] * K, RAUM[1] * K))
text(X(2), Y(RAUM[1]) + 5, "freier Raum laut Messung: %.0f x %.0f mm, %.0f mm tief" % RAUM, 2.7, "#d07000")
# ---- Gehaeuse
g = [(0, 0), (GB, 0), (GB, GH - FASE), (GB - FASE, GH), (0, GH)]
add('<polygon points="%s" fill="#cfd6dc" stroke="#2b3238" stroke-width="1.0"/>' % " ".join("%.1f,%.1f" % (X(x), Y(y)) for x, y in g))
k = [(KAMMER_X, KAMMER_Y), (GB, KAMMER_Y), (GB, GH - FASE), (GB - FASE, GH), (KAMMER_X, GH)]
add('<polygon points="%s" fill="url(#sch)" stroke="#1b7a3d" stroke-width="0.8"/>' % " ".join("%.1f,%.1f" % (X(x), Y(y)) for x, y in k))
text(X(GB / 2 - 6), Y(30), "Lüftersteuerung", 3.6, "#2b3238", "middle", True)
text(X(GB / 2 - 6), Y(30) + 4.6, ("Gehäuse %.1f x %.1f x %.1f mm" % (GB, GH, GT)).replace(".", ","), 2.6, "#2b3238", "middle")
text(X(GB / 2 - 6), Y(30) + 8.6, "geschlossen bis auf die Sensorkammer", 2.6, "#2b3238", "middle")
for n, y in ADERN:
    add('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#b3261e" stroke-width="1.0"/>' % (X(GB), Y(y), X(GB + 9), Y(y)))
text(X(GB + 1.5), Y(ADERN[0][1] + 4.5), "Adern: L, Licht, N, Lüfter", 2.6, "#b3261e")
# ---- Sensor
sx, sy = X(SENSOR[0]), Y(SENSOR[1])
add('<circle cx="%.1f" cy="%.1f" r="2.4" fill="#1b7a3d" stroke="#fff" stroke-width="0.7"/>' % (sx, sy))
lx, ly = X(8), Y(GH) - 14
add('<path d="M%.1f %.1f L%.1f %.1f" stroke="#1b7a3d" stroke-width="0.7" fill="none"/>' % (lx + 44, ly + 1.5, sx - 2.6, sy - 1.6))
add('<rect x="%.1f" y="%.1f" width="48" height="12.5" rx="1.5" fill="#fff" stroke="#1b7a3d" stroke-width="0.7"/>' % (lx - 2, ly - 5.5))
text(lx, ly, "Feuchtesensor (SHT40)", 3.2, "#1b7a3d", bold=True)
text(lx, ly + 4.4, "in der offenen Sensorkammer", 2.6, "#1b7a3d")
# Abstand Sensor - Rand der Ansaugoeffnung
d = math.hypot(EINLASS[0] - SENSOR[0], EINLASS[1] - SENSOR[1])
ux, uy = (EINLASS[0] - SENSOR[0]) / d, (EINLASS[1] - SENSOR[1]) / d
ex, ey = SENSOR[0] + ux * (d - R_OEFFNUNG), SENSOR[1] + uy * (d - R_OEFFNUNG)
add('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#1b7a3d" stroke-width="0.6" stroke-dasharray="1.6 1.2"/>' % (sx + 2.6 * ux, sy - 2.6 * uy, X(ex), Y(ey)))
text(X((SENSOR[0] + ex) / 2) + 3, Y((SENSOR[1] + ey) / 2) + 5, "ca. %.0f mm" % (d - R_OEFFNUNG), 2.6, "#1b7a3d")
# ---- Luftstrom
def pfeil(pts):
    add('<path d="M%.1f %.1f Q%.1f %.1f %.1f %.1f" fill="none" stroke="#2a7fbf" stroke-width="1.1" marker-end="url(#pf)" opacity="0.9"/>' % (X(pts[0][0]), Y(pts[0][1]), X(pts[1][0]), Y(pts[1][1]), X(pts[2][0]), Y(pts[2][1])))
pfeil([(40, 124), (60, 121), (78, 110)])
pfeil([(84, 52), (80, 64), (88, 74)])
pfeil([(152, 150), (144, 138), (134, 126)])
pfeil([(155, 62), (150, 74), (140, 82)])
text(X(20), Y(126), "Badluft strömt zur Ansaugöffnung", 2.7, "#2a7fbf")
# ---- Masse
ym = Y(0) + 9.5
add('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#222" stroke-width="0.4"/>' % (X(0), ym, X(GB), ym))
for x in (0, GB): add('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#222" stroke-width="0.4"/>' % (X(x), ym - 1.8, X(x), ym + 1.8))
text(X(GB / 2), ym + 4.6, ("%.1f mm" % GB).replace(".", ","), 2.8, "#222", "middle", True)
xm = X(0) - 9
add('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#222" stroke-width="0.4"/>' % (xm, Y(0), xm, Y(GH)))
for y in (0, GH): add('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#222" stroke-width="0.4"/>' % (xm - 1.8, Y(y), xm + 1.8, Y(y)))
text(xm - 2, Y(GH / 2), ("%.1f mm" % GH).replace(".", ","), 2.8, "#222", "middle", True, ' transform="rotate(-90 %.1f %.1f)"' % (xm - 2, Y(GH / 2)))
# ---- Erlaeuterung
tx, ty = X(BX) + 8, Y(BY) + 6
def zl(t, fs=2.9, col="#222", bold=False):
    global ty
    text(tx, ty, t, fs, col, bold=bold); ty += fs * 1.6
zl("Warum dort", 3.5, bold=True); ty += 1
zl("Der Sensor sitzt in der oberen rechten")
zl("Ecke des Gehäuses, der Ansaugöffnung")
zl("zugewandt. Die Badluft streicht auf dem")
zl("Weg zum Lüfter an ihm vorbei.")
ty += 3
zl("Sensorkammer", 3.5, "#1b7a3d", True); ty += 1
zl("Schraffiert: der einzige offene Teil")
zl("des Gehäuses. Sie ist vom Raum mit")
zl("Netzteil und Elektronik abgeschottet.")
ty += 3
zl("Genauigkeit", 3.5, "#d07000", True); ty += 1
zl("Gehäuse und freier Raum: gemessen.")
zl("Ansaugöffnung, Wartungsöffnung und")
zl("Kabeltasche: aus einem Foto geschätzt,")
zl("etwa ±10 %.")
add("</svg>")
open(out, "w", encoding="utf-8").write("\n".join(S) + "\n")
print("Einbaulage:", out)
