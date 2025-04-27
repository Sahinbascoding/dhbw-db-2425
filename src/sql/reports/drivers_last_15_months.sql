SELECT DISTINCT 
    fahrer.fahrerid,
    fahrer.vorname,
    fahrer.nachname,
    MAX(fahrt.startzeitpunkt) AS letzte_fahrt
FROM 
    fahrer
JOIN 
    fahrer_fahrzeug ON fahrer.fahrerid = fahrer_fahrzeug.fahrerid
JOIN 
    fahrt ON fahrer_fahrzeug.fahrzeugid = fahrt.fahrzeugid
WHERE 
    fahrt.startzeitpunkt >= DATE_SUB(CURDATE(), INTERVAL 15 MONTH)
GROUP BY 
    fahrer.fahrerid, fahrer.vorname, fahrer.nachname;
