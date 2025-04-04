DROP DATABASE IF EXISTS telematik;
CREATE DATABASE telematik;
USE telematik;


-- Tabelle: Fahrzeug
CREATE TABLE Fahrzeug (
    fahrzeugid INT PRIMARY KEY,
    hersteller VARCHAR(100),
    modell VARCHAR(100),
    baujahr DATE
);

-- Tabelle: Fahrer
CREATE TABLE Fahrer (
    fahrerid INT PRIMARY KEY,
    vorname CHAR(50),
    nachname CHAR(50),
    geburtsdatum DATE,
    kontakt_nr INT,
    email VARCHAR(100)
);

-- Tabelle: Geraet
CREATE TABLE Geraet (
    geraetid INT PRIMARY KEY,
    fahrzeugid INT,
    geraet_typ VARCHAR(100),
    hersteller VARCHAR(100),
    modell VARCHAR(100),
    FOREIGN KEY (fahrzeugid) REFERENCES Fahrzeug(fahrzeugid)
);

-- Tabelle: Geraet_Installation
CREATE TABLE Geraet_Installation (
    geraet_installationid INT PRIMARY KEY,
    geraetid INT,
    fahrzeugid INT,
    einbau_datum DATE,
    ausbau_datum DATE,
    FOREIGN KEY (geraetid) REFERENCES Geraet(geraetid),
    FOREIGN KEY (fahrzeugid) REFERENCES Fahrzeug(fahrzeugid)
);

-- Tabelle: Fahrer_Fahrzeug
CREATE TABLE Fahrer_Fahrzeug (
    fahrerid INT,
    fahrzeugid INT,
    gueltig_ab DATE,
    gueltig_bis DATE,
    PRIMARY KEY (fahrerid, fahrzeugid),
    FOREIGN KEY (fahrerid) REFERENCES Fahrer(fahrerid),
    FOREIGN KEY (fahrzeugid) REFERENCES Fahrzeug(fahrzeugid)
);

-- Tabelle: Fahrt
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

-- Tabelle: Fahrt_Fahrer
CREATE TABLE Fahrt_Fahrer (
    fahrtid INT,
    fahrerid INT,
    PRIMARY KEY (fahrtid, fahrerid),
    FOREIGN KEY (fahrtid) REFERENCES Fahrt(fahrtid),
    FOREIGN KEY (fahrerid) REFERENCES Fahrer(fahrerid)
);

-- Tabelle: Fahrzeugparameter
CREATE TABLE Fahrzeugparameter (
    fahrzeugparameterid INT PRIMARY KEY,
    fahrtid INT,
    zeitstempel DATETIME,
    geschwindigkeit FLOAT,
    motortemperatur FLOAT,
    batterie FLOAT,
    FOREIGN KEY (fahrtid) REFERENCES Fahrt(fahrtid)
);

-- Tabelle: Beschleunigung
CREATE TABLE Beschleunigung (
    beschleunigungid INT PRIMARY KEY,
    fahrtid INT,
    zeitstempel DATETIME,
    x_achse FLOAT,
    y_achse FLOAT,
    z_achse FLOAT,
    FOREIGN KEY (fahrtid) REFERENCES Fahrt(fahrtid)
);

-- Tabelle: Diagnose
CREATE TABLE Diagnose (
    diagnoseid INT PRIMARY KEY,
    fahrtid INT,
    zeitstempel DATETIME,
    fehlercode TEXT,
    beschreibung TEXT,
    FOREIGN KEY (fahrtid) REFERENCES Fahrt(fahrtid)
);

-- Tabelle: Unfall
CREATE TABLE Unfall (
    unfallid INT PRIMARY KEY,
    fahrtid INT,
    unfall_zeit DATETIME,
    unfall_ort TEXT,
    schaden INT,
    unfall_ursache TEXT,
    FOREIGN KEY (fahrtid) REFERENCES Fahrt(fahrtid)
);

-- Tabelle: Wartung
CREATE TABLE Wartung (
    wartungid INT PRIMARY KEY,
    fahrzeugid INT,
    datum DATETIME,
    beschreibung TEXT,
    FOREIGN KEY (fahrzeugid) REFERENCES Fahrzeug(fahrzeugid)
);
