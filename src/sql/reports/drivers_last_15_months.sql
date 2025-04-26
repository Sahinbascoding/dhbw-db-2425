SELECT DISTINCT 
    Fahrer.fahrerid,
    Fahrer.vorname,
    Fahrer.nachname,
    MAX(Fahrt.startzeitpunkt) AS letzte_fahrt
FROM 
    Fahrer
JOIN 
    Fahrer_Fahrzeug ON Fahrer.fahrerid = Fahrer_Fahrzeug.fahrerid
JOIN 
    Fahrt ON Fahrer_Fahrzeug.fahrzeugid = Fahrt.fahrzeugid
WHERE 
    Fahrt.startzeitpunkt >= DATE_SUB(CURDATE(), INTERVAL 15 MONTH)
GROUP BY 
    Fahrer.fahrerid, Fahrer.vorname, Fahrer.nachname;
