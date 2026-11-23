# Prueft das Gehaeuse gegen das 3D-Modell der bestueckten Platine.
# Aufruf: python3 pruefe_kollision.py <wanne.stl> <deckel_in_einbaulage.stl> <platine_bestueckt.stl>
import sys, numpy as np, trimesh
wanne, deckel, platine = (trimesh.load(p) for p in sys.argv[1:4])
for n, m in (("Wanne", wanne), ("Deckel", deckel)):
    print("%-7s geschlossen: %s, Volumen %.1f cm3, Aussenmasse %s mm" % (n, m.is_watertight, m.volume / 1000, np.round(m.extents, 1).tolist()))
# Bauteile ohne 3D-Modell als Huellquader (x0, y0, z0, x1, y1, z1), Y = 30 - y aus KiCad
HUELLEN = {
    "X1 Klemmen":    (1.8, 3.15, 1.6, 17.6, 26.85, 7.2),
    "F1 Sicherung":  (5.95, 1.55, -3.1, 16.05, 4.65, 0.0),
    "RV1 Varistor":  (10.15, 11.5, -4.5, 16.45, 19.5, 0.0),
    "C2 X2":         (21.45, 8.56, -1.5, 27.15, 14.26, 0.0),
    "U4 Sensor":     (65.65, 3.05, 1.6, 67.15, 4.55, 2.1),
}
# Punkte: alle Ecken und Dreiecksmitten der Platine, dazu ein Raster auf den Huellquadern
pts = [platine.vertices, platine.triangles_center]
for x0, y0, z0, x1, y1, z1 in HUELLEN.values():
    g = np.mgrid[x0:x1:12j, y0:y1:12j, z0:z1:6j].reshape(3, -1).T
    pts.append(g)
pts = np.vstack(pts)
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
sys.exit(0 if ok else 1)
