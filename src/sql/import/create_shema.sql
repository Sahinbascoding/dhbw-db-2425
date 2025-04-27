-- 01: fahrzeug
CREATE TABLE IF NOT EXISTS fahrzeug (
    fahrzeugid INT PRIMARY KEY,
    hersteller VARCHAR(100),
    modell VARCHAR(100),
    baujahr YEAR
);

-- 02: fahrer
CREATE TABLE IF NOT EXISTS fahrer (
    fahrerid INT PRIMARY KEY,
    vorname CHAR(50),
    nachname CHAR(50),
    geburtsdatum DATE,
    kontakt_nr INT,
    email VARCHAR(100)
);

-- 03: fahrer_fahrzeug
CREATE TABLE IF NOT EXISTS fahrer_fahrzeug (
    fahrerid INT,
    fahrzeugid INT,
    gueltig_ab DATE,
    gueltig_bis DATE,
    PRIMARY KEY (fahrerid, fahrzeugid),
    FOREIGN KEY (fahrerid) REFERENCES fahrer(fahrerid),
    FOREIGN KEY (fahrzeugid) REFERENCES fahrzeug(fahrzeugid)
);

-- 04: geraet
CREATE TABLE IF NOT EXISTS geraet (
    geraetid INT PRIMARY KEY,
    fahrzeugid INT,
    geraet_typ VARCHAR(100),
    hersteller VARCHAR(100),
    modell VARCHAR(100),
    FOREIGN KEY (fahrzeugid) REFERENCES fahrzeug(fahrzeugid)
);

CREATE TABLE IF NOT EXISTS fahrt (
    fahrtid INT AUTO_INCREMENT PRIMARY KEY,
    fahrzeugid INT,
    geraetid INT,
    startzeitpunkt VARCHAR(255),
    endzeitpunkt VARCHAR(255),
    route VARCHAR(255),
    FOREIGN KEY (fahrzeugid) REFERENCES fahrzeug(fahrzeugid),
    FOREIGN KEY (geraetid) REFERENCES geraet(geraetid)
);

-- 06: fahrt_fahrer
CREATE TABLE IF NOT EXISTS fahrt_fahrer (
    fahrtid INT,
    fahrerid INT,
    PRIMARY KEY (fahrtid, fahrerid),
    FOREIGN KEY (fahrtid) REFERENCES fahrt(fahrtid),
    FOREIGN KEY (fahrerid) REFERENCES fahrer(fahrerid)
);

-- 07: fahrzeugparameter
CREATE TABLE IF NOT EXISTS fahrzeugparameter (
    fahrzeugparameterid INT AUTO_INCREMENT PRIMARY KEY,
    fahrtid INT,
    zeitstempel DATETIME,
    geschwindigkeit FLOAT,
    motortemperatur FLOAT,
    batterie FLOAT,
    FOREIGN KEY (fahrtid) REFERENCES fahrt(fahrtid)
);

-- 08: beschleunigung
CREATE TABLE IF NOT EXISTS beschleunigung (
    beschleunigungid INT AUTO_INCREMENT PRIMARY KEY,
    fahrtid INT,
    zeitstempel DATETIME,
    x_achse FLOAT,
    y_achse FLOAT,
    z_achse FLOAT,
    FOREIGN KEY (fahrtid) REFERENCES fahrt(fahrtid)
);

-- 09: diagnose
CREATE TABLE IF NOT EXISTS diagnose (
    diagnoseid INT AUTO_INCREMENT PRIMARY KEY,
    fahrtid INT,
    zeitstempel DATETIME,
    fehlercode TEXT,
    beschreibung TEXT,
    FOREIGN KEY (fahrtid) REFERENCES fahrt(fahrtid)
);

-- 10: wartung
CREATE TABLE IF NOT EXISTS wartung (
    wartungid INT AUTO_INCREMENT PRIMARY KEY,
    fahrzeugid INT,
    datum DATETIME,
    beschreibung TEXT,
    FOREIGN KEY (fahrzeugid) REFERENCES fahrzeug(fahrzeugid)
);

-- 11: geraet_installation
CREATE TABLE IF NOT EXISTS geraet_installation (
    geraet_installationid INT AUTO_INCREMENT PRIMARY KEY,
    geraetid INT,
    fahrzeugid INT,
    einbau_datum DATE,
    ausbau_datum DATE,
    FOREIGN KEY (geraetid) REFERENCES geraet(geraetid),
    FOREIGN KEY (fahrzeugid) REFERENCES fahrzeug(fahrzeugid)
);

-- 12: Conversion Log
CREATE TABLE IF NOT EXISTS conversion_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    source_table VARCHAR(255) NOT NULL,
    target_collection VARCHAR(255) NOT NULL,
    status VARCHAR(50),
    duration_seconds FLOAT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 13: changelog Tabelle
CREATE TABLE IF NOT EXISTS changelog (
    id INT AUTO_INCREMENT PRIMARY KEY,
    table_name VARCHAR(100),
    operation_type VARCHAR(20),
    record_id INT,
    changed_column VARCHAR(100),
    old_value TEXT,
    new_value TEXT,
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);