-- 01: Fahrzeug
CREATE TABLE Fahrzeug (
    fahrzeugid INT PRIMARY KEY,
    hersteller VARCHAR(100),
    modell VARCHAR(100),
    baujahr YEAR
);

-- 02: Fahrer
CREATE TABLE Fahrer (
    fahrerid INT PRIMARY KEY,
    vorname CHAR(50),
    nachname CHAR(50),
    geburtsdatum DATE,
    kontakt_nr INT,
    email VARCHAR(100)
);

-- 03: Fahrer_Fahrzeug
CREATE TABLE Fahrer_Fahrzeug (
    fahrerid INT,
    fahrzeugid INT,
    gueltig_ab DATE,
    gueltig_bis DATE,
    PRIMARY KEY (fahrerid, fahrzeugid),
    FOREIGN KEY (fahrerid) REFERENCES Fahrer(fahrerid),
    FOREIGN KEY (fahrzeugid) REFERENCES Fahrzeug(fahrzeugid)
);

-- 04: Geraet
CREATE TABLE Geraet (
    geraetid INT PRIMARY KEY,
    fahrzeugid INT,
    geraet_typ VARCHAR(100),
    hersteller VARCHAR(100),
    modell VARCHAR(100),
    FOREIGN KEY (fahrzeugid) REFERENCES Fahrzeug(fahrzeugid)
);

-- 05: Fahrt
CREATE TABLE Fahrt (
    fahrtid INT PRIMARY KEY,
    fahrzeugid INT,
    geraetid INT,
    startzeitpunkt DATETIME,
    endzeitpunkt DATETIME,
    route TEXT,
    FOREIGN KEY (fahrzeugid) REFERENCES Fahrzeug(fahrzeugid),
    FOREIGN KEY (geraetid) REFERENCES Geraet(geraetid)
);

-- 06: Fahrt_Fahrer
CREATE TABLE Fahrt_Fahrer (
    fahrtid INT,
    fahrerid INT,
    PRIMARY KEY (fahrtid, fahrerid),
    FOREIGN KEY (fahrtid) REFERENCES Fahrt(fahrtid),
    FOREIGN KEY (fahrerid) REFERENCES Fahrer(fahrerid)
);

-- 07: Fahrzeugparameter
CREATE TABLE Fahrzeugparameter (
    fahrzeugparameterid INT AUTO_INCREMENT PRIMARY KEY,
    fahrtid INT,
    zeitstempel DATETIME,
    geschwindigkeit FLOAT,
    motortemperatur FLOAT,
    batterie FLOAT,
    FOREIGN KEY (fahrtid) REFERENCES Fahrt(fahrtid)
);

-- 08: Beschleunigung
CREATE TABLE Beschleunigung (
    beschleunigungid INT AUTO_INCREMENT PRIMARY KEY,
    fahrtid INT,
    zeitstempel DATETIME,
    x_achse FLOAT,
    y_achse FLOAT,
    z_achse FLOAT,
    FOREIGN KEY (fahrtid) REFERENCES Fahrt(fahrtid)
);

-- 09: Diagnose
CREATE TABLE Diagnose (
    diagnoseid INT AUTO_INCREMENT PRIMARY KEY,
    fahrtid INT,
    zeitstempel DATETIME,
    fehlercode TEXT,
    beschreibung TEXT,
    FOREIGN KEY (fahrtid) REFERENCES Fahrt(fahrtid)
);

-- 10: Wartung
CREATE TABLE Wartung (
    wartungid INT AUTO_INCREMENT PRIMARY KEY,
    fahrzeugid INT,
    datum DATETIME,
    beschreibung TEXT,
    FOREIGN KEY (fahrzeugid) REFERENCES Fahrzeug(fahrzeugid)
);

-- 11: Geraet_Installation
CREATE TABLE Geraet_Installation (
    geraet_installationid INT AUTO_INCREMENT PRIMARY KEY,
    geraetid INT,
    fahrzeugid INT,
    einbau_datum DATE,
    ausbau_datum DATE,
    FOREIGN KEY (geraetid) REFERENCES Geraet(geraetid),
    FOREIGN KEY (fahrzeugid) REFERENCES Fahrzeug(fahrzeugid)
);
