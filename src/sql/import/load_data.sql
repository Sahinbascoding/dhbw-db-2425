-- #TODO 1: Fahrzeug
START TRANSACTION;
LOAD DATA LOCAL INFILE 'data/01_fahrzeug.csv'
IGNORE INTO TABLE fahrzeug
FIELDS TERMINATED BY ',' ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 LINES (fahrzeugid, hersteller, modell, baujahr);
COMMIT;

-- #TODO 2: Fahrer
START TRANSACTION;
LOAD DATA LOCAL INFILE 'data/02_fahrer.csv'
IGNORE INTO TABLE fahrer
FIELDS TERMINATED BY ',' ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 LINES (fahrerid, vorname, nachname, geburtsdatum, kontakt_nr, email);
COMMIT;

-- #TODO 3: Fahrer_Fahrzeug
START TRANSACTION;
LOAD DATA LOCAL INFILE 'data/03_fahrer_fahrzeug.csv'
IGNORE INTO TABLE fahrer_fahrzeug
FIELDS TERMINATED BY ',' ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 LINES (fahrerid, fahrzeugid, gueltig_ab, gueltig_bis);
COMMIT;

-- #TODO 4: Gerät
START TRANSACTION;
LOAD DATA LOCAL INFILE 'data/04_geraet.csv'
IGNORE INTO TABLE geraet
FIELDS TERMINATED BY ',' ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 LINES (geraetid, fahrzeugid, geraet_typ, hersteller, modell);
COMMIT;

-- #TODO 5: Fahrt
START TRANSACTION;
LOAD DATA LOCAL INFILE 'data/05_fahrt.csv'
IGNORE INTO TABLE fahrt
FIELDS TERMINATED BY ',' ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 LINES (fahrtid, fahrzeugid, geraetid, startzeitpunkt, endzeitpunkt, route);
COMMIT;

-- #TODO 6: Fahrt_Fahrer
START TRANSACTION;
LOAD DATA LOCAL INFILE 'data/06_fahrt_fahrer.csv'
IGNORE INTO TABLE fahrt_fahrer
FIELDS TERMINATED BY ',' ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 LINES (fahrtid, fahrerid);
COMMIT;

-- #TODO 7: Fahrzeugparameter
START TRANSACTION;
LOAD DATA LOCAL INFILE 'data/07_fahrzeugparameter.csv'
IGNORE INTO TABLE fahrzeugparameter
FIELDS TERMINATED BY ',' ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 LINES (fahrzeugparameterid, fahrtid, zeitstempel, geschwindigkeit, motortemperatur, batterie);
COMMIT;

-- #TODO 8: Beschleunigung
START TRANSACTION;
LOAD DATA LOCAL INFILE 'data/08_beschleunigung.csv'
IGNORE INTO TABLE beschleunigung
FIELDS TERMINATED BY ',' ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 LINES (beschleunigungid, fahrtid, zeitstempel, x_achse, y_achse, z_achse);
COMMIT;

-- #TODO 9: Diagnose
START TRANSACTION;
LOAD DATA LOCAL INFILE 'data/09_diagnose.csv'
IGNORE INTO TABLE diagnose
FIELDS TERMINATED BY ',' ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 LINES (diagnoseid, fahrtid, zeitstempel, fehlercode, beschreibung);
COMMIT;

-- #TODO 10: Wartung
START TRANSACTION;
LOAD DATA LOCAL INFILE 'data/10_wartung.csv'
IGNORE INTO TABLE wartung
FIELDS TERMINATED BY ',' ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 LINES (wartungid, fahrzeugid, datum, beschreibung);
COMMIT;

-- #TODO 11: Gerät_Installation
START TRANSACTION;
LOAD DATA LOCAL INFILE 'data/11_geraet_installation.csv'
IGNORE INTO TABLE geraet_installation
FIELDS TERMINATED BY ',' ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 LINES (geraet_installationid, geraetid, fahrzeugid, einbau_datum, ausbau_datum);
COMMIT;
