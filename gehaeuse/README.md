# Gehäuse (Entwurf v4 für Platine v1.3, noch nicht gedruckt)

Zweiteiliges Gehäuse aus Wanne und Deckel für den Einbau unten links im Lüfterkasten, vor dem Lüftergehäuse. Netzteil und Klemmen liegen unten, die Leitungen kommen von rechts, der Feuchtesensor sitzt oben rechts hinter der abgeschrägten Ecke zum Lüfter-Einlass. Parametrisches OpenSCAD-Modell, druckbar ohne Stützmaterial.

![Gehäuse geschlossen und geöffnet](bilder/gehaeuse_beide.png)
![Wanne mit Platine von vorn](bilder/gehaeuse_offen_von_vorn.png)
![Seite mit Leitungsöffnungen und Lüftungsschlitzen](bilder/gehaeuse_leitungsseite.png)

## Maße

| | |
|---|---|
| Außen | 80,6 breit x 67,6 hoch x 23,5 mm tief; der obere Teil mit dem Sensor ist nur 72,6 mm breit (Stufe rechts ab 45,5 mm Höhe) |
| Wandstärke | 2 mm |
| Druckvolumen | Wanne 14,0 cm³, Deckel 20,2 cm³ |

## Aufbau

- **Einbaulage** wie in den Bildern von vorn gesehen: linke Seite an der Kastenwand, Unterseite auf dem Kastenboden, Rückseite vor dem Lüftergehäuse. Rückseite, linke Seite und Unterseite sind glatt; in den Lüfterkasten wird nicht gebohrt.
- **Platine** ist nur oben bestückt und liegt 1 mm über dem Boden auf Leisten der Wanne. Zwei Dome der Wanne gehen durch die Bohrungen der Platine (unten links und oben im Arm) und halten sie in Position. Rippen im Deckel drücken sie an acht Stellen auf die Leisten.
- **Anschlussraum unten rechts**, 14 mm tief, im Ausschnitt der Platine. Die vier Adern kommen gerade von rechts durch je eine Öffnung (4,5 mm) in der Trennfuge und werden beim Schließen umfasst. Klemmenbelegung im Deckel eingeprägt, von oben nach unten: L, Lüfter, Licht, N. Eine Wand trennt den Anschlussraum vom Platinenteil darüber.
- **Trennung Netz / 3,3 V:** im 2 mm breiten Isolationsschlitz der Platine steht ein Steg der Wanne, den eine Rippe des Deckels bis zur Decke fortsetzt – überall außer unter den beiden Optokopplern.
- **Sensorkammer oben rechts:** eine Trennwand schottet die Sensorinsel ab. Lüftungsschlitze nur dort (2 mm breit, von knapp über der Platine bis 16 mm Höhe): drei in der abgeschrägten Ecke zum Einlass, drei in der rechten Wand, zwei oben und drei lange in der Deckelfläche. Sie liegen ausschließlich auf der 3,3-V-Seite.
- **Lichtschacht der RGB-LED:** ein Rohr im Deckel (innen 3,6 mm) reicht bis 2 mm über die LED. In der Deckelfläche bleibt ein 0,6 mm dünnes Fenster stehen; das Licht ist nur mit hellem oder transparentem Filament zu sehen. Mit `led_fenster = 0` wird daraus ein offenes Loch.
- **Verschluss:** zwei Kunststoffschrauben 3 x 8 mm von vorn in die Dome (Kernloch 2,5 mm, 6,3 mm tief), dazu rundum ein Falz mit 1,5 mm Überlappung. Öffnen nur mit Werkzeug. Beide Schrauben sitzen im 3,3-V-Bereich, mehr als 10 mm vom Netzkupfer entfernt.

## Dateien

| Datei | Inhalt |
|---|---|
| `gehaeuse.scad` | Modell mit allen Maßen als Parameter |
| `wanne.stl`, `deckel.stl` | Druckdateien; der Deckel liegt schon mit der Deckelfläche nach unten |
| `platine_bestueckt.stl` | 3D-Modell der bestückten Platine aus KiCad (nur zur Kontrolle und für die Bilder) |
| `pruefe_kollision.py` | prüft Wanne und Deckel gegen die Platine und gegeneinander |

Neu erzeugen:

```bash
openscad -D 'teil="wanne"' -o wanne.stl gehaeuse.scad
```

```bash
openscad -D 'teil="deckel"' -o deckel.stl gehaeuse.scad
```

## Geprüft

Rechnerische Kontrolle gegen das 3D-Modell der Platine: keine Durchdringung, Wanne und Deckel überschneiden sich nicht. Der kleinste Abstand zu einem Bauteil beträgt 1,3 mm in der Wanne (Steg im Isolationsschlitz zum Varistor) und 0,8 mm im Deckel (Trennwand der Sensorkammer zum Optokoppler U2). Klemme, Sicherung, Varistor, X2-Kondensator, LED und Sensor gingen als Quader in den Datenblattmaßen in die Prüfung ein.

## Offen und vor dem Druck zu klären

1. **Lage im Kasten.** Bis zur Frontabdeckung sind laut Messung etwa 50 mm Tiefe frei, das Gehäuse braucht 23,5 mm. Die Lage von Kabeltasche, Wartungsklappe und Einlass ist dagegen nur aus Fotos geschätzt (±10 %): danach reicht der untere, 81 mm breite Teil bis an die Kabeltasche oder knapp hinein, oben bleiben etwa 7 mm bis zur Wartungsklappe. Vor der Bestellung der Platine mit einer Pappschablone 81 x 68 mm (oben rechts 8 mm schmaler) im Kasten prüfen; ob Rippen oder der Filter der Frontabdeckung in den Raum ragen, ist nicht geprüft.
2. **Höhe der Aderöffnungen.** Sie sitzen 2,7 mm über der Platine auf Höhe der angenommenen Leitereinführung der WAGO 2061; das Maß ist nicht aus dem Datenblatt belegt (`z_teil`).
3. **Leitungsaustritt.** Die Adern verlassen das Gehäuse waagrecht nach rechts in Richtung Kabeltasche. Mit den flexiblen Litzen im Kasten geht das, mit starren Adern wäre es eng.
4. **Verschraubung.** Zwei Schrauben, unten links und oben im Arm. Die Ecke unten rechts am Anschlussraum ist am weitesten von beiden entfernt; ob der Deckel dort sauber anliegt, zeigt erst ein Probedruck.
5. **Steg im Isolationsschlitz.** Er ist 1,2 mm stark und hat zu beiden Seiten 0,4 mm Luft zur Platine. Wenn die Platine beim Einlegen klemmt, `st0`/`st1` anpassen.
6. **Lichtschacht.** Ob die LED durch das 0,6-mm-Fenster hell genug ist, hängt vom Filament ab und ist nicht erprobt.
7. **Werkstoff.** Flammhemmendes Material nehmen (UL 94 V-0), z. B. entsprechend ausgewiesenes PETG, ABS oder PC. Normales PLA ist ungeeignet, auch wegen der feuchtwarmen Luft im Lüfterkasten.
8. **Befestigung.** Vorgesehen ist doppelseitiges Klebeband auf der linken Seite (zur Kastenwand) oder auf der Rückseite; Flächen vorher entstauben und entfetten.
9. **Feuchte.** Durch den Kasten strömt die Badluft. Die Platine sollte einen Schutzlack bekommen; Sensor (Membran), Klemmen, LED und Programmierpads aussparen.
10. Kein Schutzgrad und keine Normprüfung: das ist ein Entwurf, kein geprüftes Installationsgehäuse.
