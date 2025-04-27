-- Zusätzlich Daten in Tabelle beschleunigung, damit 1:n klar wird: eine fahrt kann mehrere beschleunigungswerte haben
INSERT INTO beschleunigung (fahrtid, zeitstempel, x_achse, y_achse, z_achse)
VALUES 
(95435, '2024-01-02 08:53:05', 2.18, -1.1, 2.97),
(95435, '2024-01-02 08:53:06', 3.15, 1.83, 4.69),
(95435, '2024-01-02 08:53:07', 2.98, -4.19, -4.87);

-- Löschen falscher Daten aus fahrt_fahrer
DELETE FROM fahrt_fahrer WHERE fahrtid IN (100001, 100003);

-- Zusätzlich Daten in Tabelle fahrt_fahrer, damit Beziehung klar wird: Ein fahrer kann mehrere fahrten haben, eine fahrt kann mehrere fahrer haben (n:m)
INSERT IGNORE INTO fahrt_fahrer (fahrtid, fahrerid) VALUES 
(30, 5),  -- fahrt 30 hat jetzt zwei fahrer (4 & 5)
(16, 11); -- fahrt 16 hat jetzt zwei fahrer (10 & 11)

-- Zusätzlich Daten in Tabelle diagnose, damit 1:n klar wird: Eine fahrt kann mehrere diagnosen haben
INSERT INTO diagnose (fahrtid, zeitstempel, fehlercode, beschreibung)
VALUES
    (FLOOR(RAND() * 100000) + 1, TIMESTAMPADD(MINUTE, FLOOR(RAND() * 120), '2024-01-01 08:00:00'), 'E0148', 'Information: 14'),
    (FLOOR(RAND() * 100000) + 1, TIMESTAMPADD(MINUTE, FLOOR(RAND() * 120), '2024-01-01 08:00:00'), 'E0779', 'Warnung: 43'),
    (FLOOR(RAND() * 100000) + 1, TIMESTAMPADD(MINUTE, FLOOR(RAND() * 120), '2024-01-01 08:00:00'), 'E0656', 'Kritischer Fehler: 6'),
    (FLOOR(RAND() * 100000) + 1, TIMESTAMPADD(MINUTE, FLOOR(RAND() * 120), '2024-01-01 08:00:00'), 'E0097', 'Warnung: 34'),
    (FLOOR(RAND() * 100000) + 1, TIMESTAMPADD(MINUTE, FLOOR(RAND() * 120), '2024-01-01 08:00:00'), 'E0069', 'Kritischer Fehler: 1');
