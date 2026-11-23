// Gehaeuse fuer die Lueftersteuerung Bad (Platine v1.1, 70 x 30 mm) - Wanne und Deckel fuer den 3D-Druck
// Ausfuehrung fuer den Einbau hochkant in der linken unteren Ecke des Luefterkastens:
// Klemmen unten, Sensor oben rechts im Luftstrom, glatte Rueckseite und glatte linke Seite.
//
// Koordinaten wie im 3D-Export der Platine: X entlang der Platine (Klemmen bei X = 0, im Einbau unten),
// Y quer (Y = 30 - y aus KiCad; im Einbau zeigt Y = 0 nach rechts zum Luefter), Z = Platinenunterseite 0,
// Deckel bei +Z (im Einbau vorn).
//
// Aufruf:  openscad -D 'teil="wanne"'  -o wanne.stl  gehaeuse.scad
//          openscad -D 'teil="deckel"' -o deckel.stl gehaeuse.scad
// teil = "wanne" | "deckel" | "zusammen" | "offen" | "schnitt" | "einbau" | "einbau_offen"

teil = "zusammen";
mit_platine = true;      // Platine in den Ansichten einblenden

/* [Platine] */
pl = 70;  pb = 30;  pd = 1.6;     // Laenge, Breite, Dicke
h_oben  = 16.1;          // hoechstes Bauteil oben (Netzteil)
h_unten = 4.5;           // hoechstes Bauteil unten (Varistor)

/* [Gehaeuse] */
spiel   = 0.3;           // Luft rund um die Platine
wand    = 2.0;
boden   = 2.0;
decke   = 2.0;
kammer  = 20.5;          // Anschlussraum vor den Klemmen (im Einbau unten)
luft_u  = 1.0;           // Luft unter dem hoechsten Bauteil unten
luft_o  = 0.8;           // Luft ueber dem Netzteil
auflage = 1.2;           // Breite der Auflageleisten an den Laengsseiten
z_teil  = pd + 2.7;      // Trennebene = Hoehe der Leitereinfuehrung der Klemmen
falz    = 1.5;           // Hoehe der Ueberlappung zwischen Wanne und Deckel
fuge    = 0.2;

/* [Leitungen] */
ader_y   = [24, 18, 12, 6];                // Klemmen N, Licht, Luefter, L
ader_txt = ["N", "Licht", "Lüfter", "L"];
schlitz_h = 4.5;         // Hoehe der seitlichen Leitungsoeffnung
schlitz_l = 10.5;        // Laenge der Leitungsoeffnung

/* [Verschraubung: zwei Schrauben im Anschlussraum, oben ist der Deckel eingehaengt] */
dom_ab    = 3.0;         // Abstand der Schraubenmitte von den Innenwaenden
dom_r     = 3.0;         // Dom in der Wanne
rohr_r    = 3.6;         // Schraubrohr im Deckel
schr_kern = 2.5;         // Kernloch fuer Kunststoffschraube 3 mm
schr_durch = 3.4;
schr_kopf = 5.8;

/* [Einhaengenase am oberen Ende] */
nase_y  = [0.6, 8.2];    // Bereich in Y (dort sitzt am Platinenrand kein Bauteil)
nase_t  = 0.8;           // Eingriff in die Stirnwand der Wanne

// ---- abgeleitete Masse
xi0 = -kammer - spiel;   xi1 = pl + spiel;        // Innenraum in X
yi0 = -spiel;            yi1 = pb + spiel;        // Innenraum in Y
zi0 = -h_unten - luft_u; zi1 = pd + h_oben + luft_o;   // Innenraum in Z
xa0 = xi0 - wand; xa1 = xi1 + wand; ya0 = yi0 - wand; ya1 = yi1 + wand;
za0 = zi0 - boden; za1 = zi1 + decke;
z_falz = z_teil - falz;
dom_x = xi0 + dom_ab;
dom_ys = [yi0 + dom_ab, yi1 - dom_ab];
schlitz_x0 = dom_x + rohr_r + 0.6;                // Leitungsoeffnung beginnt hinter dem Schraubrohr
$fn = 48;

module quader(x0, y0, z0, x1, y1, z1) { translate([x0, y0, z0]) cube([x1 - x0, y1 - y0, z1 - z0]); }

// seitliche Leitungsoeffnung in der rechten Laengswand (Y = 0), je zur Haelfte in Wanne und Deckel
module leitungsschlitz() {
    hull() for (x = [schlitz_x0 + schlitz_h / 2, schlitz_x0 + schlitz_l - schlitz_h / 2])
        translate([x, ya0 - 1, z_teil]) rotate([-90, 0, 0]) cylinder(d = schlitz_h, h = wand + 2);
}

module dom(r, z0, z1) {          // Schraubdom in den beiden unteren Ecken, mit der Wand verschmolzen
    for (y = dom_ys) {
        translate([dom_x, y, z0]) cylinder(r = r, h = z1 - z0);
        quader(xi0 - 0.5, y < 15 ? yi0 - 0.5 : y, z0, dom_x, y < 15 ? y : yi1 + 0.5, z1);
        quader(xi0 - 0.5, y - r, z0, dom_x, y + r, z1);
        quader(dom_x - r, y < 15 ? yi0 - 0.5 : y, z0, dom_x + r, y < 15 ? y : yi1 + 0.5, z1);
    }
}

// ------------------------------------------------------------------ Wanne
module wanne() {
    difference() {
        union() {
            difference() {
                quader(xa0, ya0, za0, xa1, ya1, z_teil);
                quader(xi0, yi0, zi0, xi1, yi1, z_teil + 1);
                // Falz: aeussere Wandhaelfte oben abnehmen (nicht an der oberen Stirnwand, dort haengt der Deckel ein)
                difference() {
                    quader(xa0 - 1, ya0 - 1, z_falz, xi1, ya1 + 1, z_teil + 1);
                    quader(xa0 + wand / 2, ya0 + wand / 2, z_falz - 1, xi1 + 1, ya1 - wand / 2, z_teil + 2);
                }
            }
            // Auflageleisten fuer die Platine (nur an den Laengskanten, dort sitzt unten kein Bauteil)
            quader(-spiel, yi0, zi0, xi1, yi0 + auflage, 0);
            quader(-spiel, yi1 - auflage, zi0, xi1, yi1, 0);
            // Anschlaege: die Platine kann nicht in den Anschlussraum rutschen
            quader(-spiel - 2, yi0, zi0, -spiel, yi0 + 2.7, pd);
            quader(-spiel - 2, yi1 - 2.7, zi0, -spiel, yi1, pd);
            dom(dom_r, zi0, z_teil);
        }
        leitungsschlitz();
        for (y = dom_ys) translate([dom_x, y, z_teil - 9]) cylinder(d = schr_kern, h = 10);
        // Tasche fuer die Einhaengenase des Deckels
        quader(xi1 - 0.1, nase_y[0] - 0.3, pd, xi1 + nase_t + 0.25, nase_y[1] + 0.3, pd + 1.5);
    }
}

// ------------------------------------------------------------------ Deckel
module rippe(x0, x1, seite) {      // Niederhalter an der Laengswand, drueckt auf den Platinenrand
    y0 = seite < 0 ? yi0 + 0.2 : yi1 - 1.2;
    quader(x0, y0, pd + 0.15, x1, y0 + 1.0, zi1 + 0.1);
    quader(x0, seite < 0 ? yi0 - 0.1 : yi1 - 0.9, z_teil, x1, seite < 0 ? yi0 + 0.9 : yi1 + 0.1, zi1 + 0.1);
}

module einhaengenase() {
    // Steg innen an der oberen Stirnwand, reicht bis knapp ueber die Platine; die Nase greift in die Wanne.
    quader(xi1 - 1.1, nase_y[0], pd + 0.2, xi1 - 0.15, nase_y[1], 6.5);
    quader(xi1 - 1.1, nase_y[0], z_teil, xi1 + 0.1, nase_y[1], 6.5);
    translate([0, nase_y[1], 0]) rotate([90, 0, 0]) linear_extrude(nase_y[1] - nase_y[0])
        polygon([[xi1 - 0.2, pd + 0.2], [xi1 + nase_t, pd + 0.2], [xi1 + nase_t, pd + 0.4], [xi1 - 0.2, pd + 0.6 + nase_t]]);
}

module deckel() {
    difference() {
        union() {
            difference() {
                union() {
                    quader(xa0, ya0, z_teil, xa1, ya1, za1);
                    // Falz: aeussere Wandhaelfte greift ueber die Wanne (nicht an der oberen Stirnwand)
                    difference() {
                        quader(xa0, ya0, z_falz + fuge, xi1 - fuge, ya1, z_teil + 0.01);
                        quader(xa0 + wand / 2 - fuge, ya0 + wand / 2 - fuge, z_falz - 1, xi1 + 1, ya1 - wand / 2 + fuge, z_teil + 1);
                    }
                }
                quader(xi0, yi0, z_teil - 1, xi1, yi1, zi1);
            }
            dom(rohr_r, z_teil, zi1 + 0.1);
            einhaengenase();
            // Niederhalter fuer die Platine
            for (s = [-1, 1]) { rippe(0.2, 2.2, s); rippe(53, 55, s); }
            rippe(68.0, 69.8, -1);
            // Trennwaende der Sensorkammer (0,5 mm ueber der Platine, am Rand als Niederhalter)
            quader(60.2, 9.7, pd + 0.5, 69.2, 10.7, zi1 + 0.1);
            quader(69.2, 9.7, pd + 0.15, xi1 - 0.2, 10.7, zi1 + 0.1);
            quader(69.2, 9.7, z_teil, xi1 + 0.1, 10.7, zi1 + 0.1);
            quader(60.2, yi0 + 0.2, pd + 0.5, 61.2, 10.7, zi1 + 0.1);
            quader(60.2, yi0 - 0.1, z_teil, 61.2, 10.7, zi1 + 0.1);
        }
        leitungsschlitz();
        // Schrauben: Durchgangsloch und Senkung fuer den Kopf von oben
        for (y = dom_ys) translate([dom_x, y, 0]) { cylinder(d = schr_durch, h = za1 + 1); translate([0, 0, z_teil + 2.5]) cylinder(d = schr_kopf, h = za1); }
        // Lueftungsschlitze der Sensorkammer: rechte Laengswand, obere Stirnwand, Decke
        for (x = [62.8, 65.0, 67.2]) quader(x - 0.75, ya0 - 1, 6, x + 0.75, yi0 + 0.15, 15);
        for (y = [2.0, 4.5, 7.0]) quader(xi1 - 0.15, y - 0.75, 8, xa1 + 1, y + 0.75, 15);
        for (x = [63.0, 65.5, 68.0]) quader(x - 0.75, 2, zi1 - 1, x + 0.75, 8, za1 + 1);
        // Beschriftung (vertieft): Klemmenbelegung, Warnhinweis, Einbaurichtung
        for (i = [0 : 3]) translate([dom_x + rohr_r + 1.2, ader_y[i], za1 - 0.6]) linear_extrude(1)
            text(ader_txt[i], size = 3.4, font = "DejaVu Sans:style=Bold", valign = "center");
        translate([20, 18.5, za1 - 0.6]) linear_extrude(1) text("230 V~", size = 5.5, font = "DejaVu Sans:style=Bold", valign = "center");
        translate([20, 10, za1 - 0.6]) linear_extrude(1) text("OBEN >", size = 4.2, font = "DejaVu Sans:style=Bold", valign = "center");
    }
}

module platine() {
    if (mit_platine) {
        color([0.1, 0.45, 0.2]) import("platine_bestueckt.stl");
        // Bauteile ohne 3D-Modell als Quader in den Datenblattmassen
        color([0.6, 0.62, 0.65]) for (y = [3.15, 15.15]) quader(1.8, y, pd, 17.0, y + 11.7, pd + 5.6);   // 2 x WAGO 2061-602
        color([0.9, 0.88, 0.8]) quader(5.95, 1.55, -3.1, 16.05, 4.65, 0);                               // Sicherung
        color([0.1, 0.25, 0.5]) quader(10.15, 11.5, -4.5, 16.45, 19.5, 0);                              // Varistor
        color([0.55, 0.4, 0.25]) quader(21.45, 8.56, -1.5, 27.15, 14.26, 0);                            // X2-Kondensator
    }
}

// Einbaulage: X nach oben, Deckel zum Betrachter, Y = 0 (Sensorseite) nach rechts
module einbaulage() { multmatrix([[0, -1, 0, 0], [0, 0, -1, 0], [1, 0, 0, 0]]) children(); }

c_w = [0.85, 0.85, 0.82];  c_d = [0.75, 0.78, 0.8];
if (teil == "wanne") wanne();
if (teil == "deckel") translate([0, 0, za1]) rotate([180, 0, 0]) deckel();     // Druckrichtung: Decke auf dem Bett
if (teil == "deckel_lage") deckel();                                           // Einbaulage (fuer Pruefungen)
if (teil == "zusammen") { color(c_w) wanne(); color(c_d) deckel(); }
if (teil == "offen") { color(c_w) wanne(); platine(); }
if (teil == "einbau") einbaulage() { color(c_w) wanne(); color(c_d) deckel(); }
if (teil == "einbau_offen") einbaulage() { color(c_w) wanne(); platine(); }
if (teil == "schnitt") {
    difference() { union() { color(c_w) wanne(); color(c_d) deckel(); }
                   translate([-100, -100, -50]) cube([300, 100 + 4.5, 100]); }
    platine();
}
