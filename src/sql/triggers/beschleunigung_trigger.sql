DROP TRIGGER IF EXISTS trg_update_beschleunigung;

DELIMITER $$

CREATE TRIGGER trg_update_beschleunigung
AFTER UPDATE ON beschleunigung
FOR EACH ROW
BEGIN
    IF OLD.fahrtid IS NULL OR NEW.fahrtid IS NULL OR OLD.fahrtid != NEW.fahrtid THEN
        INSERT INTO changelog (table_name, operation_type, record_id, changed_column, old_value, new_value)
        VALUES (
            'beschleunigung', 
            'UPDATE', 
            OLD.beschleunigungid, 
            'fahrtid', 
            COALESCE(CAST(OLD.fahrtid AS CHAR), 'NULL'), 
            COALESCE(CAST(NEW.fahrtid AS CHAR), 'NULL')
        );
    END IF;

    IF OLD.zeitstempel IS NULL OR NEW.zeitstempel IS NULL OR OLD.zeitstempel != NEW.zeitstempel THEN
        INSERT INTO changelog (table_name, operation_type, record_id, changed_column, old_value, new_value)
        VALUES (
            'beschleunigung', 
            'UPDATE', 
            OLD.beschleunigungid, 
            'zeitstempel', 
            COALESCE(CAST(OLD.zeitstempel AS CHAR), 'NULL'), 
            COALESCE(CAST(NEW.zeitstempel AS CHAR), 'NULL')
        );
    END IF;

    IF OLD.x_achse IS NULL OR NEW.x_achse IS NULL OR OLD.x_achse != NEW.x_achse THEN
        INSERT INTO changelog (table_name, operation_type, record_id, changed_column, old_value, new_value)
        VALUES (
            'beschleunigung', 
            'UPDATE', 
            OLD.beschleunigungid, 
            'x_achse', 
            COALESCE(CAST(OLD.x_achse AS CHAR), 'NULL'), 
            COALESCE(CAST(NEW.x_achse AS CHAR), 'NULL')
        );
    END IF;

    IF OLD.y_achse IS NULL OR NEW.y_achse IS NULL OR OLD.y_achse != NEW.y_achse THEN
        INSERT INTO changelog (table_name, operation_type, record_id, changed_column, old_value, new_value)
        VALUES (
            'beschleunigung', 
            'UPDATE', 
            OLD.beschleunigungid, 
            'y_achse', 
            COALESCE(CAST(OLD.y_achse AS CHAR), 'NULL'), 
            COALESCE(CAST(NEW.y_achse AS CHAR), 'NULL')
        );
    END IF;

    IF OLD.z_achse IS NULL OR NEW.z_achse IS NULL OR OLD.z_achse != NEW.z_achse THEN
        INSERT INTO changelog (table_name, operation_type, record_id, changed_column, old_value, new_value)
        VALUES (
            'beschleunigung', 
            'UPDATE', 
            OLD.beschleunigungid, 
            'z_achse', 
            COALESCE(CAST(OLD.z_achse AS CHAR), 'NULL'), 
            COALESCE(CAST(NEW.z_achse AS CHAR), 'NULL')
        );
    END IF;
END $$

DELIMITER ;
