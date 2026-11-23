# Bauteildaten fuer Stueckliste und Bestueckung: Referenz -> (Bezeichnung, Hersteller-Typ, LCSC-Nr., Hinweis)
# LCSC/JLCPCB-Nummern am 23.11.2026 ueber jlcpcb.com/lcsc.com nachgeschlagen; Lagerbestand vor der Bestellung pruefen.
R10K = ("10k 1% 0603", "0603WAF1002T5E", "C25804", "JLCPCB Basic")
TEILE = {
    "X1":  ("WAGO 2061-602/998-404 SMD-Klemme 2-polig (2 Stueck)", "2061-602/998-404", "C2765058", "JLCPCB Extended; 2 Stueck nebeneinander, in der Bestueckungsdatei als X1A und X1B"),
    "F1":  ("Sicherung T1A 250VAC SMD 10x3", "Littelfuse 0443001.DR", "C95352", "JLCPCB Extended; alternativ Schurter UMT 250 1A T (3403.0166.11)"),
    "RV1": ("Varistor 275VAC SMD", "TDK CU3225K275G2 (B72650M0271K072)", "C211106", "JLCPCB Extended; Bauform 8,0 x 6,3 mm"),
    "PS1": ("Netzteil 230V -> 3,3V 0,6A SMD", "Mean Well IRM-02-3.3S", "", "bei LCSC/JLCPCB nicht gelistet: beistellen oder von Hand loeten"),
    "U1":  ("ESP32-C3-MINI-1-H4X", "Espressif ESP32-C3-MINI-1-H4X", "C41349510", "JLCPCB Extended; N4 (C2838502) ist abgekuendigt (NRND)"),
    "U2":  ("LTV-814S AC-Optokoppler", "Lite-On LTV-814S-TA1", "C125118", "JLCPCB Extended"),
    "U3":  ("AQH3223A Photo-Triac 1,2A", "Panasonic AQH3223A", "C719698", "JLCPCB Extended; Bestand pruefen"),
    "U4":  ("SHT40 Feuchte/Temperatur", "Sensirion SHT40-AD1B-R2", "C2909890", "JLCPCB Extended"),
    "R1":  ("100k 1% 1206 200V", "1206W4F1003T5E", "C17900", "JLCPCB Basic"),
    "R2":  ("100k 1% 1206 200V", "1206W4F1003T5E", "C17900", "JLCPCB Basic"),
    "R3":  ("100R 1% 0603", "0603WAF1000T5E", "C22775", "JLCPCB Basic"),
    "R4":  ("220k 1% 0603", "0603WAF2203T5E", "C22961", "JLCPCB Basic"),
    "R5":  ("100R 1% 1206", "1206W4F1000T5E", "C17901", "JLCPCB Basic; impulsfest waere Panasonic ERJ-P08F1000V (C4195341)"),
    "R6": R10K, "R7": R10K, "R8": R10K, "R9": R10K, "R10": R10K, "R11": R10K,
    "R12": ("3k3 1% 0603", "0603WAF3301T5E", "C22978", "nur bei Bedarf bestuecken"),
    "C1":  ("100u 16V Elko SMD 6,3x5,4", "RVT1C101M0605", "C970684", "Bestand/Typ bei JLCPCB pruefen"),
    "C2":  ("10n X2 250VAC 2220", "Murata GA355QR7GB103KW01L", "C237426", "JLCPCB Extended; Sicherheitskondensator Klasse X2"),
    "C3":  ("470n 25V X7R 0603", "CL10B474KA8NNNC", "C1623", "JLCPCB Basic"),
    "C4":  ("10u 25V X5R 0805", "CL21A106KAYNNNE", "C15850", "JLCPCB Basic"),
    "C5":  ("100n 50V X7R 0603", "CC0603KRX7R9BB104", "C14663", "JLCPCB Basic"),
    "C6":  ("1u 50V X5R 0603", "CL10A105KB8NNNC", "C15849", "JLCPCB Basic"),
    "C7":  ("100n 50V X7R 0603", "CC0603KRX7R9BB104", "C14663", "JLCPCB Basic"),
    "J1":  ("Programmierpads 1,27 mm (3V3 GND TX RX IO9 EN)", "", "", "nicht bestueckt"),
}
