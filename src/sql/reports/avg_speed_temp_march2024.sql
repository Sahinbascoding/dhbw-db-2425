SELECT 
    AVG(fahrzeugparameter.geschwindigkeit) AS durchschnitt_geschwindigkeit,
    AVG(fahrzeugparameter.motortemperatur) AS durchschnitt_motortemperatur
FROM 
    Fahrzeugparameter
JOIN 
    Fahrt ON Fahrzeugparameter.fahrtid = Fahrt.fahrtid
WHERE 
    MONTH(Fahrt.startzeitpunkt) = 3
    AND YEAR(Fahrt.startzeitpunkt) = 2024;
