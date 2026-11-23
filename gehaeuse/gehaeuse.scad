// Gehaeuse fuer die Lueftersteuerung Bad, Platine v1.2 (68 x 58 mm) - Wanne und Deckel fuer den 3D-Druck
//
// Einbau unten links im Luefterkasten, vor dem Lueftergehaeuse: Netzteil und Klemmen unten, die Leitungen
// kommen von rechts, der Feuchtesensor sitzt oben rechts hinter der abgeschraegten Ecke zum Luefter-Einlass.
//
// Koordinaten wie im 3D-Export der Platine und wie in der Einbaulage von vorn gesehen:
// X nach rechts (linke Kastenwand bei X = 0), Y nach oben (Kastenboden bei Y = 0), Z zum Betrachter
// (Platinenunterseite Z = 0, Deckel vorn).
//
// Aufruf:  openscad -D 'teil="wanne"'  -o wanne.stl  gehaeuse.scad
//          openscad -D 'teil="deckel"' -o deckel.stl gehaeuse.scad
// teil = "wanne" | "deckel" | "zusammen" | "offen" | "schnitt"

teil = "zusammen";
mit_platine = true;      // Platine in den Ansichten einblenden

/* [Platine v1.2] */
pw = 68;  ph = 58;  pd = 1.6;    // Breite, Hoehe, Dicke
bw = 54;  bh = 30;               // Riegel unten (Netzteil, Klemmen)
ah = 18;                         // Hoehe des Arms oben
steg = 14;                       // Breite der Verbindung links
fase = 6;                        // abgeschraegte Ecke oben rechts
schlitz_x = pw - 9.5;            // Thermoschlitz vor der Sensorinsel
h_oben  = 16.1;                  // hoechstes Bauteil oben (Netzteil)
h_unten = 4.5;                   // hoechstes Bauteil unten (Varistor)

/* [Gehaeuse] */
spiel   = 0.3;           // Luft rund um die Platine
wand    = 2.0;
boden   = 2.0;
decke   = 2.0;
luft_u  = 1.0;           // Luft unter dem hoechsten Bauteil unten
luft_o  = 0.8;           // Luft ueber dem Netzteil
auflage = 1.2;           // Breite der Auflageleisten
z_teil  = pd + 2.7;      // Trennebene = Hoehe der Leitereinfuehrung der Klemmen
falz    = 1.5;           // Hoehe der Ueberlappung zwischen Wanne und Deckel
fuge    = 0.2;
zw      = 1.6;           // Staerke der Zwischenwaende

/* [Leitungen: von rechts in den Anschlussraum] */
ader_y   = [24, 18, 12, 6];                // Klemmen von oben nach unten
ader_txt = ["L", "Lüfter", "Licht", "N"];
ader_d   = 4.5;

/* [Verschraubung: zwei Schrauben im Kanal zwischen Riegel und Arm] */
dom_x     = [26, 60];
dom_r     = 3.0;         // Dom in der Wanne
rohr_r    = 3.6;         // Schraubrohr im Deckel
schr_kern = 2.5;         // Kernloch fuer Kunststoffschraube 3 mm
schr_durch = 3.4;
schr_kopf = 5.8;

// ---- abgeleitete Masse
ay  = ph - ah;                           // Unterkante des Arms (40)
t   = spiel + wand;
xa0 = -t; xa1 = pw + t; ya0 = -t; ya1 = ph + t;
xi0 = -spiel; xi1 = pw + spiel; yi0 = -spiel; yi1 = ph + spiel;
zi0 = -h_unten - luft_u; zi1 = pd + h_oben + luft_o;
za0 = zi0 - boden; za1 = zi1 + decke;
z_falz = z_teil - falz;
fa  = fase + t * (2 - sqrt(2));          // Fase der Aussenkontur, parallel zur Platinenfase
w1a = bh + spiel; w1b = w1a + zw;        // Zwischenwand ueber dem Riegel
w2b = ay - spiel; w2a = w2b - zw;        // Zwischenwand unter dem Arm
dom_y = (w1b + w2a) / 2;
$fn = 48;

module quader(x0, y0, z0, x1, y1, z1) { translate([x0, y0, z0]) cube([x1 - x0, y1 - y0, z1 - z0]); }
module aussen2d() { polygon([[xa0, ya0], [xa1, ya0], [xa1, ya1 - fa], [xa1 - fa, ya1], [xa0, ya1]]); }
module innen2d() { offset(delta = -wand) aussen2d(); }
module prisma(z0, z1) { translate([0, 0, z0]) linear_extrude(z1 - z0) children(); }
module im_innenraum(z0, z1) { intersection() { prisma(z0, z1) offset(delta = 0.02) innen2d(); children(); } }

module aderloecher() {
    for (y = ader_y) translate([xi1 - 1, y, z_teil]) rotate([0, 90, 0]) cylinder(d = ader_d, h = wand + 2);
}
module zwischenwaende(z0, z1) {      // doppelte Wand zwischen Netzteil/Anschlussraum und Sensorarm
    quader(steg + spiel, w1a, z0, xi1 + 0.1, w1b, z1);
    quader(steg + spiel, w2a, z0, xi1 + 0.1, w2b, z1);
    quader(steg + spiel, w1a, z0, steg + spiel + zw, w2b, z1);
}

// ------------------------------------------------------------------ Wanne
module wanne() {
    difference() {
        union() {
            difference() {
                prisma(za0, z_teil) aussen2d();
                prisma(zi0, z_teil + 1) innen2d();
                // Falz: aeussere Wandhaelfte oben abnehmen
                prisma(z_falz, z_teil + 1) difference() { offset(delta = 1) aussen2d(); offset(delta = -wand / 2) aussen2d(); }
            }
            im_innenraum(zi0, z_teil) union() {
                // Auflageleisten unter den Platinenkanten
                quader(xi0, yi0, zi0, xi0 + auflage, yi1, 0);                         // links
                quader(xi0, yi0, zi0, bw, yi0 + auflage, 0);                          // Riegel unten
                quader(xi0, yi1 - auflage, zi0, pw - fase, yi1, 0);                   // Arm oben
                quader(xi1 - auflage, ay, zi0, xi1, ph - fase, 0);                    // Arm rechts
                quader(steg + spiel, w1a - auflage, zi0, bw, w1a, 0);                 // Riegel oben
                quader(steg + spiel, w2b, zi0, schlitz_x - 0.3, w2b + auflage, 0);    // Arm unten
                zwischenwaende(zi0, z_teil);
                // Anschlaege am rechten Ende des Riegels
                quader(bw + spiel, yi0, zi0, bw + spiel + 2, yi0 + 2.7, pd);
                quader(bw + spiel, bh - 2.4, zi0, bw + spiel + 2, w1a, pd);
                for (x = dom_x) translate([x, dom_y, zi0]) cylinder(r = dom_r, h = z_teil - zi0);
            }
        }
        aderloecher();
        for (x = dom_x) translate([x, dom_y, z_teil - 9]) cylinder(d = schr_kern, h = 10);
    }
}

// ------------------------------------------------------------------ Deckel
module nh(x0, y0, x1, y1) { quader(x0, y0, pd + 0.15, x1, y1, zi1 + 0.1); }      // Niederhalter auf dem Platinenrand

module deckel() {
    difference() {
        union() {
            difference() {
                union() {
                    prisma(z_teil, za1) aussen2d();
                    // Falz: aeussere Wandhaelfte greift ueber die Wanne
                    prisma(z_falz + fuge, z_teil + 0.01) difference() { aussen2d(); offset(delta = -wand / 2 + fuge) aussen2d(); }
                }
                prisma(z_teil - 1, zi1) innen2d();
            }
            im_innenraum(pd, zi1 + 0.1) union() {
                zwischenwaende(z_teil, zi1 + 0.1);
                for (x = dom_x) translate([x, dom_y, z_teil]) cylinder(r = rohr_r, h = zi1 + 0.1 - z_teil);
                // Niederhalter: an den Aussenwaenden und an den Zwischenwaenden
                nh(16, yi0 + 0.2, 18, 1.0); nh(44, yi0 + 0.2, 46, 1.0);                 // Riegel unten
                nh(xi0 + 0.2, 10, 1.0, 12); nh(xi0 + 0.2, 33, 1.0, 35);                 // links
                nh(30, ph - 1.0, 32, yi1 - 0.2); nh(50, ph - 1.0, 52, yi1 - 0.2);       // Arm oben
                nh(pw - 1.0, 44, xi1 - 0.2, 46);                                        // Arm rechts
                nh(16, bh - 1.0, 18, w1a - 0.2); nh(44, bh - 1.0, 46, w1a - 0.2);       // Riegel oben
                nh(30, w2b + 0.2, 32, ay + 1.0); nh(50, w2b + 0.2, 52, ay + 1.0);       // Arm unten
                // Anbindung der Niederhalter an die Aussenwaende oberhalb der Trennebene
                quader(16, yi0 - 0.1, z_teil, 18, 1.0, zi1); quader(44, yi0 - 0.1, z_teil, 46, 1.0, zi1);
                quader(xi0 - 0.1, 10, z_teil, 1.0, 12, zi1); quader(xi0 - 0.1, 33, z_teil, 1.0, 35, zi1);
                quader(30, ph - 1.0, z_teil, 32, yi1 + 0.1, zi1); quader(50, ph - 1.0, z_teil, 52, yi1 + 0.1, zi1);
                quader(pw - 1.0, 44, z_teil, xi1 + 0.1, 46, zi1);
                quader(16, bh - 1.0, z_teil, 18, w1a + 0.1, zi1); quader(44, bh - 1.0, z_teil, 46, w1a + 0.1, zi1);
                quader(30, w2b - 0.1, z_teil, 32, ay + 1.0, zi1); quader(50, w2b - 0.1, z_teil, 52, ay + 1.0, zi1);
                // Trennwand der Sensorkammer links vom Thermoschlitz (0,5 mm ueber der Platine)
                quader(schlitz_x - 1.4, w2b + 0.2, pd + 0.5, schlitz_x - 0.6, yi1 - 0.2, zi1 + 0.1);
                quader(schlitz_x - 1.4, w2b - 0.1, z_teil, schlitz_x - 0.6, yi1 + 0.1, zi1 + 0.1);
            }
        }
        aderloecher();
        // Schrauben: Durchgangsloch und Senkung fuer den Kopf von vorn
        for (x = dom_x) translate([x, dom_y, 0]) { cylinder(d = schr_durch, h = za1 + 1); translate([0, 0, z_teil + 2.5]) cylinder(d = schr_kopf, h = za1); }
        // Lueftungsschlitze der Sensorkammer: Fase zum Einlass, rechte Wand, Oberseite, Deckelflaeche
        translate([xa1 - fa / 2, ya1 - fa / 2, 0]) rotate([0, 0, -45]) for (d = [-2.4, 0, 2.4]) quader(d - 0.75, -3, 6, d + 0.75, 3, 15);
        for (y = [43.0, 45.5, 48.0]) quader(xi1 - 0.15, y - 0.75, 6, xa1 + 1, y + 0.75, 15);
        for (x = [60.0, 62.5]) quader(x - 0.75, yi1 - 0.15, 6, x + 0.75, ya1 + 1, 15);
        for (x = [60.5, 63.0, 65.5]) quader(x - 0.75, 43, zi1 - 1, x + 0.75, 50, za1 + 1);
        // Beschriftung (vertieft): Klemmenbelegung, Warnhinweis, Sensor
        for (i = [0 : 3]) translate([xi1 - 0.5, ader_y[i], za1 - 0.6]) linear_extrude(1)
            text(ader_txt[i], size = 3.4, font = "DejaVu Sans:style=Bold", valign = "center", halign = "right");
        translate([6, 15, za1 - 0.6]) linear_extrude(1) text("230 V~", size = 6, font = "DejaVu Sans:style=Bold", valign = "center");
        translate([30, 52.5, za1 - 0.6]) linear_extrude(1) text("Sensor >", size = 3.6, font = "DejaVu Sans:style=Bold", valign = "center");
    }
}

module platine() {
    if (mit_platine) {
        color([0.1, 0.45, 0.2]) import("platine_bestueckt.stl");
        // Bauteile ohne 3D-Modell als Quader in den Datenblattmassen
        color([0.6, 0.62, 0.65]) for (y = [3.15, 15.15]) quader(37.0, y, pd, 52.2, y + 11.7, pd + 5.6);   // 2 x WAGO 2061-602
        color([0.9, 0.88, 0.8]) quader(37.95, 25.35, -3.1, 48.05, 28.45, 0);                             // Sicherung
        color([0.1, 0.25, 0.5]) quader(37.55, 10.5, -4.5, 43.85, 18.5, 0);                               // Varistor
        color([0.55, 0.4, 0.25]) quader(26.85, 15.74, -1.5, 32.55, 21.44, 0);                            // X2-Kondensator
        color([0.95, 0.95, 0.95]) quader(pw - 5.55, 45.25, pd, pw - 4.05, 46.75, pd + 0.9);              // Feuchtesensor
    }
}

c_w = [0.85, 0.85, 0.82];  c_d = [0.75, 0.78, 0.8];
if (teil == "wanne") wanne();
if (teil == "deckel") translate([0, 0, za1]) rotate([180, 0, 0]) deckel();     // Druckrichtung: Deckelflaeche auf dem Bett
if (teil == "deckel_lage") deckel();                                           // Einbaulage (fuer Pruefungen)
if (teil == "zusammen") { color(c_w) wanne(); color(c_d) deckel(); }
if (teil == "offen") { color(c_w) wanne(); platine(); }
if (teil == "schnitt") {
    difference() { union() { color(c_w) wanne(); color(c_d) deckel(); }
                   translate([-100, -100, 9]) cube([300, 300, 100]); }
    platine();
}
