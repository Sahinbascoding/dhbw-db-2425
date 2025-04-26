SELECT 
    Fahrer.fahrerid,
    Fahrer.vorname,
    Fahrer.nachname,
    MAX(Fahrzeugparameter.geschwindigkeit) AS max_geschwindigkeit
FROM 
    Fahrer
JOIN 
    Fahrt_Fahrer ON Fahrer.fahrerid = Fahrt_Fahrer.fahrerid
JOIN 
    Fahrt ON Fahrt_Fahrer.fahrtid = Fahrt.fahrtid
JOIN 
    Fahrzeugparameter ON Fahrt.fahrtid = Fahrzeugparameter.fahrtid
GROUP BY 
    Fahrer.fahrerid, Fahrer.vorname, Fahrer.nachname;
