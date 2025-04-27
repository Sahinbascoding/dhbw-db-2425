mysql -u root -p telematik

UPDATE Fahrzeug
SET modell = 'Supercar GT'
WHERE fahrzeugid = 1;

SELECT * FROM Changelog;


UPDATE Fahrzeug
SET hersteller = 'Test Hersteller'
WHERE fahrzeugid = 1;

SELECT * FROM Changelog;
