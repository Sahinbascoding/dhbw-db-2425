-- 1. Prüfen ob Typ VARCHAR, dann konvertieren (manuell)

-- Wenn aktuell VARCHAR, dann umwandeln
UPDATE Fahrt
SET 
    startzeitpunkt = STR_TO_DATE(startzeitpunkt, '%d.%m.%Y %H:%i'),
    endzeitpunkt = STR_TO_DATE(endzeitpunkt, '%d.%m.%Y %H:%i')
WHERE startzeitpunkt LIKE '%.%' -- Nur wenn Datumsformat alt ist
  AND endzeitpunkt LIKE '%.%';

-- Danach Spalten auf echtes DATETIME setzen
ALTER TABLE Fahrt
MODIFY startzeitpunkt DATETIME,
MODIFY endzeitpunkt DATETIME;
