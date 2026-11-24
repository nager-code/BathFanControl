# Gehäuse

[← Zur Übersicht](../README.md)

**Version V1.0 für Platine V1.0 – noch nicht gedruckt.**

Zweiteiliges Gehäuse aus Wanne und Deckel für den Einbau unten links im Lüfterkasten, vor dem Lüftergehäuse. Netzteil und Klemme liegen unten, die Leitungen kommen von rechts, der Feuchtesensor sitzt oben rechts hinter der abgeschrägten Ecke zum Lüfter-Einlass. Das Modell ist parametrisch in OpenSCAD aufgebaut und ohne Stützmaterial druckbar.

![Gehäuse geschlossen und geöffnet](bilder/gehaeuse_beide.png?v=1.0)

| Wanne mit Platine von vorn | Seite mit Leitungsöffnungen und Lüftungsschlitzen |
|---|---|
| ![Wanne mit Platine von vorn](bilder/gehaeuse_offen_von_vorn.png?v=1.0) | ![Seite mit Leitungsöffnungen und Lüftungsschlitzen](bilder/gehaeuse_leitungsseite.png?v=1.0) |

![Wanne und Deckel von innen: Sensorkammer oben rechts, Anschlussraum mit Innenwand unten rechts](bilder/gehaeuse_kammern.png?v=1.0)

## Maße

| | |
|---|---|
| Außen | 72,6 breit x 77,1 hoch x 25,7 mm tief |
| Wandstärke | 2 mm |
| Druckvolumen | Wanne 19,3 cm³, Deckel 20,2 cm³ |
| Werkstoff | flammhemmend nach UL 94 V-0, z. B. entsprechend ausgewiesenes PETG, ABS oder PC – **kein normales PLA** (Brandschutz und feuchtwarme Luft im Kasten) |
| Schrauben | 2 Kunststoffschrauben 3 x 10 mm, am besten mit Senkkopf |
| Druck | keine besonderen Einstellungen vorgegeben; ohne Stützmaterial drucken. Geprüft mit Düse 0,4 mm und Schichthöhen 0,15 bis 0,3 mm |

## Aufbau

### Grundidee

Luft und Feuchte sollen **nur an den Sensor** kommen. Deshalb hat das Gehäuse Öffnungen nur an der Sensorkammer; der Raum mit Netzteil, Klemme und Elektronik ist ringsum geschlossen.

Dicht im Sinne einer Schutzart ist das Gehäuse nicht: Trennfuge, Aderöffnungen und Schraubdome haben keine Dichtung.

### Einbaulage

Von vorn gesehen wie in den Bildern: linke Seite an der Kastenwand, Unterseite auf dem Kastenboden, Rückseite vor dem Lüftergehäuse. Rückseite, linke Seite und Unterseite sind glatt – in den Lüfterkasten wird nicht gebohrt.

### Platine im Gehäuse

- Die Platine liegt **4 mm über dem Boden** auf Leisten der Wanne. Darunter ist Platz für die Lötstifte von Netzteil (bis 3,4 mm) und Klemme.
- **Zwei Dome** der Wanne gehen durch die Bohrungen der Platine (unten links unter dem Netzteil und oben rechts im Arm) und halten sie in Position.
- **Rippen im Deckel** drücken die Platine an acht Stellen auf die Leisten.

### Kammern

| Kammer | Lage | Aufbau |
|---|---|---|
| **Sensorkammer** | oben rechts | möglichst offen: zwei Fenster 3,6 mm in der abgeschrägten Ecke zum Einlass, vier Fenster 3,0 mm in der rechten Wand, eines oben, dazu drei Öffnungen 2,0 mm in der Deckelfläche. In der Kammer liegt nur die Sensorinsel der Platine (3,3 V). |
| **Anschlussraum** | unten rechts, 11,9 mm tief | im Ausschnitt der Platine vor der Schraubklemme. Die vier Adern kommen von rechts durch je eine Öffnung (3,4 mm, Raster 5,08 mm) in der Außenwand und eine zweite in der Innenwand direkt vor der Klemme. Beide Öffnungen liegen in der Trennfuge und umfassen die Adern beim Schließen. |
| **Geräteraum** | Rest | Netzteil, Netzseite und Controller, ringsum geschlossen |

**Abschottung der Sensorkammer:** Links vom Thermoschlitz reicht eine Wand des Deckels bis 0,1 mm an die Platine, darunter steht eine Wand der Wanne bis an die Platinenunterseite. Nach unten schließt der Steg im Isolationsschlitz ab. Die vier Leiterbahnen zum Sensor laufen über den schmalen Platinensteg oben unter der Wand hindurch. Wer den Restspalt schließen will, legt beim Zusammenbau eine dünne Raupe neutral vernetzendes Silikon auf die Platine.

### Weitere Details

- **Trennung Netz / 3,3 V:** Im 2 mm breiten Isolationsschlitz der Platine steht ein Steg der Wanne. Eine Rippe des Deckels setzt ihn bis zur Decke fort – überall außer unter den beiden Optokopplern.
- **Klemme:** Die Schrauben sind nur bei abgenommenem Deckel erreichbar. Belegung von oben nach unten: L, Licht, N, Lüfter. Sie steht auf der Platine direkt hinter der Klemme (sichtbar bei abgenommenem Deckel) und ist außen in den Deckel eingeprägt.
- **USB-C-Buchse:** Sie steht 7,5 mm hoch auf der Platine und liegt unter dem geschlossenen Deckel. Eine Öffnung dafür gibt es nicht; zum Programmieren den Deckel abnehmen (Netzspannung vorher abschalten).
- **Lichtschacht der RGB-LED:** Ein Rohr im Deckel (innen 3,6 mm) reicht bis 2 mm über die LED. In der Deckelfläche bleibt ein 0,6 mm dünnes Fenster stehen; das Licht ist nur mit hellem oder transparentem Filament zu sehen. Mit `led_fenster = 0` wird daraus ein offenes Loch.
- **Verschluss:** zwei Kunststoffschrauben 3 x 10 mm von vorn in die Dome (Kernloch 2,5 mm, 10 mm tief), dazu rundum ein Falz mit 1,5 mm Überlappung. Der Schraubensitz im Deckel ist ein 45°-Kegel (Senkung 90°, Durchmesser 5,8 mm): Er passt für Senkkopfschrauben; Linsenkopfschrauben liegen auf dem Rand auf. Öffnen nur mit Werkzeug. Beide Schrauben sitzen im 3,3-V-Bereich, mehr als 10 mm vom Netzkupfer entfernt.

## Dateien

| Datei | Inhalt |
|---|---|
| `gehaeuse.scad` | OpenSCAD-Modell mit allen Maßen als Parameter |
| `wanne.stl`, `deckel.stl` | Druckdateien; der Deckel liegt schon mit der Deckelfläche nach unten. Beide ohne Stützmaterial drucken |
| `platine_bestueckt.stl` | 3D-Modell der bestückten Platine aus KiCad (nur zur Kontrolle und für die Bilder) |
| `pruefe_kollision.py` | prüft Wanne und Deckel gegen die Platine und gegeneinander |
| `bilder/` | Ansichten für diese Doku |

### Wichtige Parameter in `gehaeuse.scad`

| Parameter | Bedeutung |
|---|---|
| `ader_d` | Durchmesser der Aderöffnungen (3,4 mm) |
| `z_teil` | Höhe der Trennebene = Höhe der Aderöffnungen |
| `st0`, `st1` | Lage des Stegs im Isolationsschlitz |
| `led_fenster` | Reststärke über dem LED-Schacht (0,6 mm; 0 = offen) |

### STL-Dateien neu erzeugen

```bash
openscad -D 'teil="wanne"' -o wanne.stl gehaeuse.scad
```

```bash
openscad -D 'teil="deckel"' -o deckel.stl gehaeuse.scad
```

## Geprüft

**Druckbarkeit:** Beide STL-Dateien sind geschlossene Körper und laufen in PrusaSlicer 2.7 (Düse 0,4 mm, Schichthöhen 0,15 bis 0,3 mm, ohne Stützen) ohne Warnung durch. Dafür ist die eingeprägte Schrift auf der Deckelfläche als V-Nut mit 45°-Flanken ausgeführt und der Schraubensitz als Kegel. Senkrechte Nuten und ein flacher Sitz müssten über dem Druckbett frei überbrückt werden; der Slicer meldet das als „Long bridging extrusions“.

**Passform:** Rechnerische Kontrolle gegen das 3D-Modell der Platine: **keine Durchdringung**, Wanne und Deckel überschneiden sich nicht.

- Kleinster Abstand in der Wanne: 0,6 mm (Boden zu den ungekürzten Stiften des Netzteils).
- Kleinster Abstand im Deckel: 0,6 mm (Innenwand zur Vorderseite der Klemme).

Netzteil und Klemme gingen mit ihren KiCad-3D-Modellen in die Prüfung ein. Sicherung, Varistor, X2-Kondensator, Triac, LED, USB-Buchse und Sensor wurden als Quader in den Datenblattmaßen angenommen.

## Offen und vor dem Druck zu klären

### Vor dem Druck

1. **Lage im Kasten.** Am Einbauort sind höchstens 85 mm Breite, 40 mm Tiefe und 140 mm Höhe frei (gemessen am 24.11.2026). Das Gehäuse braucht 72,6 x 25,7 x 77,1 mm; es bleiben 12,4 mm in der Breite für die rechts austretenden Adern, 14,3 mm in der Tiefe und 62,9 mm in der Höhe.
   Die Lage von Ansaugöffnung, Wartungsöffnung und Kabeltasche ist nur aus einem Foto geschätzt (±10 %), siehe [Einbaulage](../doku/einbaulage.svg). Danach reicht die Oberkante des Gehäuses bis an die Unterkante der Wartungsöffnung der Rückstauklappe (etwa 76 mm über dem Kastenboden), und die abgeschrägte Ecke liegt rund 19 mm vor dem Rand der Ansaugöffnung.
   **→ Mit einer Pappschablone 73 x 77 mm prüfen, ob die Wartungsöffnung frei bleibt.** Ob Rippen oder der Filter der Frontabdeckung in den Raum ragen, ist nicht geprüft.
2. **Aderöffnungen.** Der Durchmesser 3,4 mm (`ader_d`) ist angenommen, die Adern im Kasten sind nicht vermessen. An den Außendurchmesser anpassen, damit möglichst wenig Luft durchkommt; den Rest bei Bedarf mit dauerelastischer Dichtmasse schließen.
3. **Höhe der Aderöffnungen.** Sie sitzen 3,6 mm über der Platine (`z_teil`). Das Maß stammt aus dem KiCad-3D-Modell der MKDS 1,5 (Öffnung 2,4 bis 4,9 mm über der Platine); das Datenblatt bemaßt die Höhe der Leitereinführung nicht.

### Beim Probedruck prüfen

4. **Leitungsaustritt.** Die Adern verlassen das Gehäuse waagrecht nach rechts in Richtung Kabeltasche. Mit den flexiblen Litzen im Kasten geht das, mit starren Adern wird es eng.
5. **Verschraubung.** Die Ecken unten rechts (Anschlussraum) und oben links sind am weitesten von beiden Schrauben entfernt. Ob der Deckel dort sauber anliegt, zeigt erst ein Probedruck.
6. **Steg im Isolationsschlitz.** Er ist 1,2 mm stark und hat zu beiden Seiten 0,4 mm Luft zur Platine. Wenn die Platine beim Einlegen klemmt: `st0`/`st1` anpassen.
7. **Lichtschacht.** Ob die LED durch das 0,6-mm-Fenster hell genug ist, hängt vom Filament ab und ist nicht erprobt.

### Für den Einbau

8. **Werkstoff.** Flammhemmend nach UL 94 V-0 (siehe [Maße](#maße)).
9. **Befestigung.** Doppelseitiges Klebeband auf der linken Seite (zur Kastenwand) oder auf der Rückseite; Flächen vorher entstauben und entfetten.
10. **Feuchte.** Durch den Kasten strömt die Badluft. Die Platine sollte einen Schutzlack bekommen, siehe [Aufbau → Platine lackieren](../doku/aufbau.md#platine-lackieren).
11. **Keine Normprüfung.** Das ist ein Entwurf ohne Schutzart, kein geprüftes Installationsgehäuse.
