DROP PROCEDURE IF EXISTS AddFahrt;

DELIMITER $$

CREATE PROCEDURE AddFahrt(
    IN p_fahrzeugid INT,
    IN p_geraetid INT,
    IN p_startzeitpunkt DATETIME,
    IN p_endzeitpunkt DATETIME,
    IN p_route VARCHAR(255)
)
BEGIN
    INSERT INTO fahrt (fahrzeugid, geraetid, startzeitpunkt, endzeitpunkt, route)
    VALUES (p_fahrzeugid, p_geraetid, p_startzeitpunkt, p_endzeitpunkt, p_route);
END$$

DELIMITER ;
