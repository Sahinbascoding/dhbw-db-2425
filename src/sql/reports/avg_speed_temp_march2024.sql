SELECT 
    AVG(fahrzeugparameter.geschwindigkeit) AS durchschnitt_geschwindigkeit,
    AVG(fahrzeugparameter.motortemperatur) AS durchschnitt_motortemperatur
FROM 
    fahrzeugparameter
JOIN 
    fahrt ON fahrzeugparameter.fahrtid = fahrt.fahrtid
WHERE 
    MONTH(fahrt.startzeitpunkt) = 3
    AND YEAR(fahrt.startzeitpunkt) = 2024;
