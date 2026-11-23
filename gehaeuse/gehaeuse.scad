// Gehaeuse fuer die Lueftersteuerung Bad (Platine v1.1, 70 x 30 mm) - Wanne und Deckel fuer den 3D-Druck
//
// Koordinaten wie im 3D-Export der Platine: X entlang der Platine (Klemmen bei X = 0), Y quer
// (Y = 30 - y aus KiCad), Z nach oben, Platinenunterseite bei Z = 0.
//
// Aufruf:  openscad -D 'teil="wanne"'  -o wanne.stl  gehaeuse.scad
//          openscad -D 'teil="deckel"' -o deckel.stl gehaeuse.scad
// teil = "wanne" | "deckel" | "zusammen" | "offen" | "schnitt"

teil = "zusammen";
laschen = true;          // Befestigungslaschen an den Stirnseiten
mit_platine = true;      // Platine in den Ansichten "offen" und "schnitt" einblenden

/* [Platine] */
pl = 70;  pb = 30;  pd = 1.6;     // Laenge, Breite, Dicke
h_oben  = 16.1;          // hoechstes Bauteil oben (Netzteil)
h_unten = 4.5;           // hoechstes Bauteil unten (Varistor)

/* [Gehaeuse] */
spiel   = 0.3;           // Luft rund um die Platine
wand    = 2.0;
boden   = 2.0;
decke   = 2.0;
kammer  = 15;            // Anschlussraum vor den Klemmen
luft_u  = 1.0;           // Luft unter dem hoechsten Bauteil unten
luft_o  = 0.8;           // Luft ueber dem Netzteil
auflage = 1.2;           // Breite der Auflageleisten an den Laengsseiten
z_teil  = pd + 2.7;      // Trennebene = Hoehe der Leitereinfuehrung der Klemmen
falz    = 1.5;           // Hoehe der Ueberlappung zwischen Wanne und Deckel
fuge    = 0.2;

/* [Leitungen] */
ader_y  = [24, 18, 12, 6];                 // N, Licht, Luefter, L
ader_txt = ["N", "Licht", "Lüfter", "L"];
ader_d  = 4.5;           // Oeffnung je Ader (1,5 mm2 mit Isolierung ca. 3 mm)

/* [Verschraubung] */
dom_x   = [-9, 57];      // Lage der Schraubdome an den Laengsseiten
dom_r   = 3.8;
dom_ab  = 2.4;           // Mitte der Schraube ausserhalb der Wand
schr_kern = 2.5;         // Kernloch fuer Kunststoffschraube 3 mm
schr_durch = 3.4;
schr_kopf = 6.0;

// ---- abgeleitete Masse
xi0 = -kammer - spiel;   xi1 = pl + spiel;        // Innenraum in X
yi0 = -spiel;            yi1 = pb + spiel;        // Innenraum in Y
zi0 = -h_unten - luft_u; zi1 = pd + h_oben + luft_o;   // Innenraum in Z
xa0 = xi0 - wand; xa1 = xi1 + wand; ya0 = yi0 - wand; ya1 = yi1 + wand;
za0 = zi0 - boden; za1 = zi1 + decke;
z_falz = z_teil - falz;
$fn = 48;

module quader(x0, y0, z0, x1, y1, z1) { translate([x0, y0, z0]) cube([x1 - x0, y1 - y0, z1 - z0]); }

module aderloecher() {
    for (y = ader_y) translate([xa0 - 1, y, z_teil]) rotate([0, 90, 0]) cylinder(d = ader_d, h = wand + 2);
}

module dom_stellen() { for (x = dom_x) for (y = [ya0 - dom_ab, ya1 + dom_ab]) translate([x, y, 0]) children(); }

module dom_koerper(z0, z1) {
    dom_stellen() translate([0, 0, z0]) cylinder(r = dom_r, h = z1 - z0);
    for (x = dom_x) {                      // Verbindung zur Wand
        quader(x - dom_r, ya0 - dom_ab, z0, x + dom_r, ya0 + 0.5, z1);
        quader(x - dom_r, ya1 - 0.5, z0, x + dom_r, ya1 + dom_ab, z1);
    }
}

// ------------------------------------------------------------------ Wanne
module wanne() {
    difference() {
        union() {
            difference() {
                quader(xa0, ya0, za0, xa1, ya1, z_teil);
                quader(xi0, yi0, zi0, xi1, yi1, z_teil + 1);
                // Falz: aeussere Wandhaelfte oben abnehmen
                difference() {
                    quader(xa0 - 1, ya0 - 1, z_falz, xa1 + 1, ya1 + 1, z_teil + 1);
                    quader(xa0 + wand / 2, ya0 + wand / 2, z_falz - 1, xa1 - wand / 2, ya1 - wand / 2, z_teil + 2);
                }
            }
            // Auflageleisten fuer die Platine (nur an den Laengskanten, dort sitzt unten kein Bauteil)
            quader(-spiel, yi0, zi0, xi1, yi0 + auflage, 0);
            quader(-spiel, yi1 - auflage, zi0, xi1, yi1, 0);
            // Anschlaege links: die Platine kann nicht in den Anschlussraum rutschen
            quader(-spiel - 2, yi0, zi0, -spiel, yi0 + 2.7, pd);
            quader(-spiel - 2, yi1 - 2.7, zi0, -spiel, yi1, pd);
            dom_koerper(za0, z_falz);
            if (laschen) for (x = [[xa0 - 11, xa0], [xa1, xa1 + 11]]) difference() {
                quader(x[0], 15 - 8, za0, x[1], 15 + 8, za0 + 3);
                translate([(x[0] + x[1]) / 2, 15, za0 - 1]) cylinder(d = 4.5, h = 5);
            }
        }
        aderloecher();
        dom_stellen() translate([0, 0, z_falz - 9]) cylinder(d = schr_kern, h = 10);
    }
}

// ------------------------------------------------------------------ Deckel
module rippe(x0, x1, seite) {      // Niederhalter an der Laengswand, drueckt auf den Platinenrand
    y0 = seite < 0 ? yi0 + 0.2 : yi1 - 1.2;
    quader(x0, y0, pd + 0.15, x1, y0 + 1.0, zi1 + 0.1);
    quader(x0, seite < 0 ? yi0 - 0.1 : yi1 - 0.9, z_teil, x1, seite < 0 ? yi0 + 0.9 : yi1 + 0.1, zi1 + 0.1);
}

module deckel() {
    difference() {
        union() {
            difference() {
                union() {
                    quader(xa0, ya0, z_teil, xa1, ya1, za1);
                    // Falz: aeussere Wandhaelfte greift ueber die Wanne
                    difference() {
                        quader(xa0, ya0, z_falz + fuge, xa1, ya1, z_teil + 0.01);
                        quader(xa0 + wand / 2 + fuge, ya0 + wand / 2 + fuge, z_falz - 1, xa1 - wand / 2 - fuge, ya1 - wand / 2 - fuge, z_teil + 1);
                    }
                }
                quader(xi0, yi0, z_teil - 1, xi1, yi1, zi1);
            }
            dom_koerper(z_falz + fuge, za1);
            // Niederhalter fuer die Platine
            for (s = [-1, 1]) { rippe(0.2, 2.2, s); rippe(53, 55, s); }
            rippe(68.0, 69.8, -1);
            // Trennwaende der Sensorkammer (0,5 mm ueber der Platine, am rechten Rand als Niederhalter)
            quader(60.2, 9.7, pd + 0.5, 69.2, 10.7, zi1 + 0.1);
            quader(69.2, 9.7, pd + 0.15, xi1 + 0.1, 10.7, zi1 + 0.1);
            quader(60.2, yi0 - 0.1, pd + 0.5, 61.2, 10.7, zi1 + 0.1);
        }
        aderloecher();
        // Schrauben: Durchgangsloch und Senkung fuer den Kopf von oben
        dom_stellen() { translate([0, 0, 0]) cylinder(d = schr_durch, h = za1 + 1); translate([0, 0, z_teil + 2.5]) cylinder(d = schr_kopf, h = za1); }
        // Lueftungsschlitze der Sensorkammer: Laengswand, Stirnwand, Decke
        for (x = [62.8, 65.0, 67.2]) quader(x - 0.75, ya0 - 1, 6, x + 0.75, yi0 + 0.15, 14);
        for (y = [2.0, 4.5, 7.0]) quader(xi1 - 0.15, y - 0.75, 6, xa1 + 1, y + 0.75, 14);
        for (x = [63.0, 65.5, 68.0]) quader(x - 0.75, 2, zi1 - 1, x + 0.75, 8, za1 + 1);
        // Beschriftung der Adern und Warnhinweis (vertieft)
        for (i = [0 : 3]) translate([xa0 + 2.5, ader_y[i], za1 - 0.6]) linear_extrude(1)
            text(ader_txt[i], size = 3.6, font = "DejaVu Sans:style=Bold", valign = "center");
        translate([24, 15, za1 - 0.6]) linear_extrude(1) text("230 V~", size = 6, font = "DejaVu Sans:style=Bold", valign = "center");
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

if (teil == "wanne") wanne();
if (teil == "deckel") translate([0, 0, za1]) rotate([180, 0, 0]) deckel();     // Druckrichtung: Decke auf dem Bett
if (teil == "deckel_lage") deckel();                                           // Einbaulage (fuer Pruefungen)
if (teil == "zusammen") { color([0.85, 0.85, 0.82]) wanne(); color([0.75, 0.78, 0.8]) deckel(); }
if (teil == "offen") { color([0.85, 0.85, 0.82]) wanne(); platine(); }
if (teil == "schnitt") {
    difference() { union() { color([0.85, 0.85, 0.82]) wanne(); color([0.75, 0.78, 0.8]) deckel(); }
                   translate([-100, -100, -50]) cube([300, 100 + 11.5, 100]); }
    platine();
}
