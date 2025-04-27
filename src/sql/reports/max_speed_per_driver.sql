SELECT 
    fahrer.fahrerid,
    fahrer.vorname,
    fahrer.nachname,
    MAX(fahrzeugparameter.geschwindigkeit) AS max_geschwindigkeit
FROM 
    fahrer
JOIN 
    fahrt_fahrer ON fahrer.fahrerid = fahrt_fahrer.fahrerid
JOIN 
    fahrt ON fahrt_fahrer.fahrtid = fahrt.fahrtid
JOIN 
    fahrzeugparameter ON fahrt.fahrtid = fahrzeugparameter.fahrtid
GROUP BY 
    fahrer.fahrerid, fahrer.vorname, fahrer.nachname;
