# Prueft das Gehaeuse gegen das 3D-Modell der bestueckten Platine.
# Aufruf: python3 pruefe_kollision.py <wanne.stl> <deckel_in_einbaulage.stl> <platine_bestueckt.stl>
import sys, numpy as np, trimesh
wanne, deckel, platine = (trimesh.load(p) for p in sys.argv[1:4])
for n, m in (("Wanne", wanne), ("Deckel", deckel)):
    print("%-7s geschlossen: %s, Volumen %.1f cm3, Aussenmasse %s mm" % (n, m.is_watertight, m.volume / 1000, np.round(m.extents, 1).tolist()))
# Bauteile ohne 3D-Modell als Huellquader (x0, y0, z0, x1, y1, z1) in den Koordinaten des 3D-Exports
HUELLEN = {
    "X1 Klemmen":    (36.4, 3.15, 1.6, 52.2, 26.85, 7.2),
    "F1 Sicherung":  (37.95, 25.35, -3.1, 48.05, 28.45, 0.0),
    "RV1 Varistor":  (37.55, 10.5, -4.5, 43.85, 18.5, 0.0),
    "C2 X2":         (26.85, 15.74, -1.5, 32.55, 21.44, 0.0),
    "U4 Sensor":     (62.45, 45.25, 1.6, 63.95, 46.75, 2.5),
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
