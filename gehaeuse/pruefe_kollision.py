# Prueft das Gehaeuse gegen das 3D-Modell der bestueckten Platine.
# Aufruf: python3 pruefe_kollision.py <wanne.stl> <deckel_in_einbaulage.stl> <platine_bestueckt.stl>
import sys, numpy as np, trimesh
wanne, deckel, platine = (trimesh.load(p) for p in sys.argv[1:4])
for n, m in (("Wanne", wanne), ("Deckel", deckel)):
    print("%-7s geschlossen: %s, Volumen %.1f cm3, Aussenmasse %s mm" % (n, m.is_watertight, m.volume / 1000, np.round(m.extents, 1).tolist()))
# Bauteile ohne 3D-Modell als Huellquader (x0, y0, z0, x1, y1, z1) in den Koordinaten des 3D-Exports
HUELLEN = {
    "F1 Sicherung":  (51.15, 32.65, 1.6, 61.25, 35.75, 4.7),
    "RV1 Varistor":  (37.95, 29.95, 1.6, 45.95, 36.25, 6.1),
    "C2 X2":         (38.3, 17.65, 1.6, 43.3, 23.35, 3.6),
    "Q1 Triac":      (25.9, 28.3, 1.6, 36.1, 35.1, 4.1),
    "U4 Sensor":     (62.45, 55.25, 1.6, 63.95, 56.75, 2.5),
    "D1 LED":        (34.25, 62.55, 1.6, 36.35, 64.65, 2.6),
    "J2 USB-C":      (39.5, 62.4, 1.6, 48.5, 65.6, 9.1),
    "J2 Zapfen":     (39.4, 62.2, -0.8, 48.6, 65.8, 0.0),
    # Stifte der bedrahteten Teile unter der Platine (ungekuerzt): Netzteil 3,4 mm, Klemme 1,9 mm
    "PS1 Stifte AC": (33.3, 11.9, -3.4, 34.5, 18.1, 0.0),
    "PS1 Stifte DC": (4.2, 6.9, -3.4, 5.4, 23.1, 0.0),
    "X1 Stifte":     (49.3, 6.7, -1.9, 50.7, 23.3, 0.0),
}
# Punkte: alle Ecken und Dreiecksmitten der Platine, dazu ein Raster auf den Huellquadern
pts = [platine.vertices, platine.triangles_center]
for x0, y0, z0, x1, y1, z1 in HUELLEN.values():
    g = np.mgrid[x0:x1:12j, y0:y1:12j, z0:z1:6j].reshape(3, -1).T
    pts.append(g)
pts = np.vstack(pts)
pts[np.abs(pts[:, 2]) < 0.02, 2] = 0.02     # Platinenunterseite liegt auf den Leisten auf: nicht als Durchdringung werten
ok = True
for n, m in (("Wanne", wanne), ("Deckel", deckel)):
    inside = m.contains(pts)
    k = pts[inside]
    if len(k):
        ok = False
        print("KOLLISION %s: %d Punkte, Bereich x %.2f..%.2f  y %.2f..%.2f  z %.2f..%.2f" % (n, len(k), k[:,0].min(), k[:,0].max(), k[:,1].min(), k[:,1].max(), k[:,2].min(), k[:,2].max()))
    else:
        print("%-7s keine Durchdringung (%d Pruefpunkte)" % (n, len(pts)))
# kleinster Abstand der Pruefpunkte zur Gehaeuseoberflaeche (ohne Auflageflaechen der Platine selbst)
sel = pts[(pts[:, 2] > 1.75) | (pts[:, 2] < -0.05)]
sel = sel[np.random.default_rng(1).choice(len(sel), min(len(sel), 20000), replace=False)]
for n, m in (("Wanne", wanne), ("Deckel", deckel)):
    d = trimesh.proximity.closest_point(m, sel)[1]
    i = d.argmin()
    print("%-7s kleinster Abstand zu einem Bauteil: %.2f mm bei (%.1f, %.1f, %.1f)" % (n, d[i], *sel[i]))
# Wanne und Deckel duerfen sich gegenseitig nicht durchdringen
try:
    i = trimesh.boolean.intersection([wanne, deckel], engine="manifold")
    v = 0.0 if i.is_empty else float(i.volume)
    print("Ueberschneidung Wanne/Deckel: %.3f mm3" % v)
    ok = ok and v < 0.01
except Exception as e:
    print("Ueberschneidung Wanne/Deckel nicht geprueft:", e)
sys.exit(0 if ok else 1)
