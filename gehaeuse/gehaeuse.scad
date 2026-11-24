// Gehaeuse fuer die Lueftersteuerung Bad, Platine v1.3 (76 x 63 mm, einseitig bestueckt) - Wanne und Deckel fuer den 3D-Druck
//
// Einbau unten links im Luefterkasten, vor dem Lueftergehaeuse: Netzteil und Klemmen unten, die Leitungen
// kommen von rechts in den Anschlussraum (Ausschnitt der Platine unten rechts), der Feuchtesensor sitzt oben
// rechts hinter der abgeschraegten Ecke zum Luefter-Einlass. Alle Bauteile sitzen auf der Platinenoberseite.
// Der untere Teil (Netzteil, Klemmen, Anschlussraum) ist 8 mm breiter als der Arm mit dem Sensor.
// Netzteil und Klemme sind bedrahtet: unter der Platine bleiben 4 mm Platz fuer ihre Loetstifte.
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

/* [Platine v1.3] */
pw = 68;  ph = 63;  pd = 1.6;    // Breite des Arms oben, Hoehe, Dicke
pu = 76;                         // Breite des unteren Teils (bis zum Isolationsschlitz)
bw = 62.6; bh = 30;              // Riegel unten (Netzteil, Klemmen); rechts daneben der Ausschnitt fuer die Leitungen
iso_y0 = 43.2; iso_y1 = 45.2;    // Isolationsschlitz zwischen Netzteil (unten) und 3,3-V-Teil (oben)
steg = 22;                       // Breite der Verbindung links
fase = 6;                        // abgeschraegte Ecke oben rechts
schlitz_x = pw - 9.5;            // Thermoschlitz vor der Sensorinsel
h_oben  = 15.3;                  // hoechstes Bauteil oben (Netzteil 15,1 mm)
h_unten = 3.4;                   // Stifte des bedrahteten Netzteils unter der Platine (Klemme 1,9 mm)
loch    = [[4.8, 5.5], [46.5, 56.0]];   // Bohrungen 6,6 mm in der Platine fuer die Schraubdome
// Abschnitte des Isolationsschlitzes, in denen keine Optokoppler sitzen: dort steht ein Steg im Schlitz
iso_frei = [[22.6, 34.6], [44.4, 50.4], [58.0, 68.4]];
led     = [36.5, 58.6];          // Lage der RGB-LED: darueber sitzt der Lichtschacht im Deckel

/* [Gehaeuse] */
spiel   = 0.3;           // Luft rund um die Platine
wand    = 2.0;
boden   = 2.0;
decke   = 2.0;
luft_u  = 0.6;           // Luft unter den Stiften der bedrahteten Bauteile
luft_o  = 0.8;           // Luft ueber dem Netzteil
auflage = 1.2;           // Breite der Auflageleisten
z_teil  = pd + 3.6;      // Trennebene = Mitte der Leitereinfuehrung der Klemme (aus dem 3D-Modell der MKDS 1,5 gemessen)
falz    = 1.5;           // Hoehe der Ueberlappung zwischen Wanne und Deckel
fuge    = 0.2;
zw      = 1.6;           // Staerke der Zwischenwaende

/* [Leitungen: von rechts in den Anschlussraum] */
ader_y   = [22.62, 17.54, 12.46, 7.38];    // Pole der Klemme von oben nach unten (Raster 5,08 mm)
ader_txt = ["L", "Licht", "N", "Lüfter"];
ader_d   = 4.0;

/* [Verschraubung: zwei Dome der Wanne gehen durch die Bohrungen der Platine] */
dom_r     = 3.0;         // Dom in der Wanne
rohr_r    = 3.6;         // Schraubrohr im Deckel
schr_kern = 2.5;         // Kernloch fuer Kunststoffschraube 3 mm
schr_durch = 3.4;
schr_kopf = 5.8;

/* [Lichtschacht der RGB-LED] */
ls_da = 6.0;  ls_di = 3.6;       // Aussen- und Innendurchmesser
led_fenster = 0.6;               // Reststaerke der Deckelflaeche ueber dem Schacht (helles/transparentes Filament); 0 = offen

/* [Lueftung der Sensorkammer] */
ls_b  = 2.0;             // Schlitzbreite
ls_z0 = pd + 0.8;        // Unterkante der Schlitze: knapp ueber der Platine, damit die Luft ueber den Sensor streicht
ls_z1 = 16.0;            // Oberkante der Schlitze in den Waenden

// ---- abgeleitete Masse
t   = spiel + wand;
xa0 = -t; xa1 = pw + t; ya0 = -t; ya1 = ph + t;
xi0 = -spiel; xi1 = pw + spiel; yi0 = -spiel; yi1 = ph + spiel;
xu1 = pu + spiel; xb1 = pu + t;          // unterer Teil: Innen- und Aussenkante rechts
ys  = iso_y0 + t;                        // Oberkante der Stufe rechts (Aussenwand ueber dem unteren Teil)
zi0 = -h_unten - luft_u; zi1 = pd + h_oben + luft_o;
za0 = zi0 - boden; za1 = zi1 + decke;
z_falz = z_teil - falz;
fa  = fase + t * (2 - sqrt(2));          // Fase der Aussenkontur, parallel zur Platinenfase
ar0 = bh - spiel - zw; ar1 = bh - spiel; // Wand zwischen Anschlussraum und Platine darueber
st0 = iso_y0 + 0.4; st1 = iso_y1 - 0.4;  // Steg im Isolationsschlitz
$fn = 48;

module quader(x0, y0, z0, x1, y1, z1) { translate([x0, y0, z0]) cube([x1 - x0, y1 - y0, z1 - z0]); }
module aussen2d() { polygon([[xa0, ya0], [xb1, ya0], [xb1, ys], [xa1, ys], [xa1, ya1 - fa], [xa1 - fa, ya1], [xa0, ya1]]); }
module innen2d() { offset(delta = -wand) aussen2d(); }
module prisma(z0, z1) { translate([0, 0, z0]) linear_extrude(z1 - z0) children(); }
module im_innenraum(z0, z1) { intersection() { prisma(z0, z1) offset(delta = 0.02) innen2d(); children(); } }

module aderloecher() {
    for (y = ader_y) translate([xu1 - 1, y, z_teil]) rotate([0, 90, 0]) cylinder(d = ader_d, h = wand + 2);
}
// Lueftungsschlitze in den Waenden der Sensorkammer: in der Fase zum Einlass, rechts und oben.
// Sie laufen durch Wanne und Deckel, von knapp ueber der Platine bis ls_z1.
module wandschlitze() {
    translate([xa1 - fa / 2, ya1 - fa / 2, 0]) rotate([0, 0, -45])
        for (d = [-3.2, 0, 3.2]) quader(d - ls_b / 2, -3, ls_z0, d + ls_b / 2, 3, ls_z1);
    for (y = [47.4, 50.6, 55.4]) quader(xi1 - 0.15, y - ls_b / 2, ls_z0, xa1 + 1, y + ls_b / 2, ls_z1);
    for (x = [59.6, 61.9]) quader(x - 0.8, yi1 - 0.15, ls_z0, x + 0.8, ya1 + 1, ls_z1);
}
// Trennung Netzspannung / Kleinspannung: Steg im Isolationsschlitz (ausser unter den Optokopplern)
module isosteg(z0, z1) { for (a = iso_frei) quader(a[0], st0, z0, a[1], st1, z1); }
// Wand zwischen dem Anschlussraum (Platinenausschnitt unten rechts) und dem Platinenteil darueber
module raumwand(z0, z1) { quader(bw + spiel, ar0, z0, xu1 + 0.1, ar1, z1); }

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
                quader(bw - auflage, yi0, zi0, bw, bh, 0);                            // Riegel rechts (am Anschlussraum)
                quader(bw - auflage, bh, zi0, xu1, bh + auflage, 0);                  // ueber dem Anschlussraum
                quader(xu1 - auflage, bh, zi0, xu1, iso_y0, 0);                       // rechts, Netzteil
                quader(xi1 - auflage, iso_y1, zi0, xi1, ph - fase, 0);                // rechts, Sensorarm
                quader(xi0, yi1 - auflage, zi0, pw - fase, yi1, 0);                   // oben
                quader(steg + 0.6, iso_y0 - auflage, zi0, xu1, iso_y0, 0);            // unter dem Schlitz
                quader(steg + 0.6, iso_y1, zi0, schlitz_x - 0.3, iso_y1 + auflage, 0);// ueber dem Schlitz
                isosteg(zi0, z_teil);
                raumwand(zi0, z_teil);
                for (p = loch) translate([p[0], p[1], zi0]) {
                    cylinder(r = dom_r + 1.5, h = -zi0);                              // Auflage rund um die Bohrung
                    cylinder(r = dom_r, h = z_teil - zi0);
                }
            }
        }
        aderloecher();
        wandschlitze();
        for (p = loch) translate([p[0], p[1], za0 + 1.0]) cylinder(d = schr_kern, h = z_teil - za0);
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
                isosteg(z_teil, zi1 + 0.1);
                raumwand(z_teil, zi1 + 0.1);
                for (p = loch) translate([p[0], p[1], z_teil]) cylinder(r = rohr_r, h = zi1 + 0.1 - z_teil);
                // Niederhalter an den Aussenwaenden, oberhalb der Trennebene an die Wand angebunden
                for (x = [14, 46]) { nh(x, yi0 + 0.2, x + 2, 1.0); quader(x, yi0 - 0.1, z_teil, x + 2, 1.0, zi1); }                 // unten
                for (y = [16, 41]) { nh(xi0 + 0.2, y, 1.0, y + 2); quader(xi0 - 0.1, y, z_teil, 1.0, y + 2, zi1); }                 // links
                for (x = [30, 54]) { nh(x, ph - 1.0, x + 2, yi1 - 0.2); quader(x, ph - 1.0, z_teil, x + 2, yi1 + 0.1, zi1); }       // oben
                nh(pw - 1.0, 52.2, xi1 - 0.2, 53.8); quader(pw - 1.0, 52.2, z_teil, xi1 + 0.1, 53.8, zi1);                          // rechts, Sensorarm
                nh(pu - 1.0, 36, xu1 - 0.2, 38); quader(pu - 1.0, 36, z_teil, xu1 + 0.1, 38, zi1);                                  // rechts, Netzteil
                // Lichtschacht ueber der RGB-LED (endet 2 mm ueber der Platine)
                translate([led[0], led[1], pd + 2.0]) cylinder(d = ls_da, h = zi1 + 0.1 - pd - 2.0);
                // Trennwand der Sensorkammer links vom Thermoschlitz (0,5 mm ueber der Platine)
                quader(schlitz_x - 1.1, iso_y1 + 0.2, pd + 0.5, schlitz_x - 0.3, yi1 - 0.2, zi1 + 0.1);
                quader(schlitz_x - 1.1, st0, z_teil, schlitz_x - 0.3, yi1 + 0.1, zi1 + 0.1);
            }
        }
        aderloecher();
        // Schrauben: Durchgangsloch und Senkung fuer den Kopf von vorn
        for (p = loch) translate([p[0], p[1], 0]) { cylinder(d = schr_durch, h = za1 + 1); translate([0, 0, z_teil + 2.5]) cylinder(d = schr_kopf, h = za1); }
        // Lichtschacht: innen hohl, in der Deckelflaeche bleibt ein duennes Fenster stehen (led_fenster = 0: offenes Loch)
        translate([led[0], led[1], pd + 1.9]) cylinder(d = ls_di, h = za1 - led_fenster - pd - 1.9);
        // Lueftungsschlitze der Sensorkammer: in den Waenden und drei lange Schlitze in der Deckelflaeche
        wandschlitze();
        for (x = [60.0, 63.0, 66.0]) quader(x - ls_b / 2, 46.5, zi1 - 1, x + ls_b / 2, 58.0, za1 + 1);
        // Beschriftung (vertieft): Klemmenbelegung, Warnhinweis, Sensor
        for (i = [0 : 3]) translate([xu1 - 0.5, ader_y[i], za1 - 0.6]) linear_extrude(1)
            text(ader_txt[i], size = 3.4, font = "DejaVu Sans:style=Bold", valign = "center", halign = "right");
        translate([14, 15, za1 - 0.6]) linear_extrude(1) text("230 V~", size = 6, font = "DejaVu Sans:style=Bold", valign = "center");
        translate([26, 50.5, za1 - 0.6]) linear_extrude(1) text("Sensor >", size = 3.6, font = "DejaVu Sans:style=Bold", valign = "center");
    }
}

module platine() {
    if (mit_platine) {
        color([0.1, 0.45, 0.2]) import("platine_bestueckt.stl");
        // Bauteile ohne 3D-Modell als Quader in den Datenblattmassen
        color([0.9, 0.88, 0.8]) quader(59.15, 32.65, pd, 69.25, 35.75, pd + 3.1);                        // Sicherung
        color([0.1, 0.25, 0.5]) quader(45.95, 29.95, pd, 53.95, 36.25, pd + 4.5);                        // Varistor
        color([0.55, 0.4, 0.25]) quader(46.3, 17.65, pd, 51.3, 23.35, pd + 2.0);                         // X2-Kondensator
        color([0.15, 0.15, 0.15]) quader(33.95, 28.4, pd, 41.05, 35.0, pd + 2.3);                        // Triac (DPAK)
        color([0.95, 0.95, 0.95]) quader(pw - 5.55, ph - 12.75, pd, pw - 4.05, ph - 11.25, pd + 0.9);    // Feuchtesensor
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
