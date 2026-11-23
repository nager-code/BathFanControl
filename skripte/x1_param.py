# Geometrie der SMD-Klemme X1: 2 Stueck WAGO 2061-602/998-404 (je 2-polig, Raster 6 mm) direkt nebeneinander.
# Masse aus dem WAGO-Datenblatt 2061-602/998-404 (Stand 02.05.2019): je Pol zwei Loetflaechen gleichen
# Potentials, vorn 6,5 x 2,1 mm, hinten 4,5 x 2,4 mm, Gesamtlaenge des Loetbilds 17,0 mm.
# Die Lage der Flaechen zur Gehaeusekante ist aus der Zeichnung abgeleitet -> vor der Bestellung mit dem
# CAD-Footprint von WAGO vergleichen.
X1 = dict(
    name="WAGO_2061-602_2x_SMD",
    descr="2 x WAGO 2061-602/998-404, SMD-Leiterplattenklemme 2-polig, Raster 6 mm, 0,5-1,5 mm2, Leitereinfuehrung von links",
    pitch=6.0,
    # Pads je Pol, relativ zur Polmitte: (dx, dy, breite_x, hoehe_y)
    pads=[(-5.25, 0.0, 6.5, 2.1), (6.25, 0.0, 4.5, 2.4)],
    body=(-7.7, 8.1),          # Gehaeuse in x relativ zum Ursprung (Leitereinfuehrung bei x_min), mit Loetfahnen
    order=["2", "3", "4", "1"],  # Padnummern von oben nach unten: N, Licht, Luefter, L
)
X1X = 9.5                      # Ursprung der Klemme auf der Platine (x)
