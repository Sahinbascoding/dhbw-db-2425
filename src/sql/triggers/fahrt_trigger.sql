DROP TRIGGER IF EXISTS trg_update_fahrt;

DELIMITER $$

CREATE TRIGGER trg_update_fahrt
AFTER UPDATE ON fahrt
FOR EACH ROW
BEGIN
    IF OLD.fahrzeugid IS NULL OR NEW.fahrzeugid IS NULL OR OLD.fahrzeugid != NEW.fahrzeugid THEN
        INSERT INTO changelog (table_name, operation_type, record_id, changed_column, old_value, new_value)
        VALUES (
            'fahrt', 
            'UPDATE', 
            OLD.fahrtid, 
            'fahrzeugid', 
            COALESCE(CAST(OLD.fahrzeugid AS CHAR), 'NULL'), 
            COALESCE(CAST(NEW.fahrzeugid AS CHAR), 'NULL')
        );
    END IF;

    IF OLD.geraetid IS NULL OR NEW.geraetid IS NULL OR OLD.geraetid != NEW.geraetid THEN
        INSERT INTO changelog (table_name, operation_type, record_id, changed_column, old_value, new_value)
        VALUES (
            'fahrt', 
            'UPDATE', 
            OLD.fahrtid, 
            'geraetid', 
            COALESCE(CAST(OLD.geraetid AS CHAR), 'NULL'), 
            COALESCE(CAST(NEW.geraetid AS CHAR), 'NULL')
        );
    END IF;

    IF OLD.startzeitpunkt IS NULL OR NEW.startzeitpunkt IS NULL OR OLD.startzeitpunkt != NEW.startzeitpunkt THEN
        INSERT INTO changelog (table_name, operation_type, record_id, changed_column, old_value, new_value)
        VALUES (
            'fahrt', 
            'UPDATE', 
            OLD.fahrtid, 
            'startzeitpunkt', 
            COALESCE(OLD.startzeitpunkt, 'NULL'), 
            COALESCE(NEW.startzeitpunkt, 'NULL')
        );
    END IF;

    IF OLD.endzeitpunkt IS NULL OR NEW.endzeitpunkt IS NULL OR OLD.endzeitpunkt != NEW.endzeitpunkt THEN
        INSERT INTO changelog (table_name, operation_type, record_id, changed_column, old_value, new_value)
        VALUES (
            'fahrt', 
            'UPDATE', 
            OLD.fahrtid, 
            'endzeitpunkt', 
            COALESCE(OLD.endzeitpunkt, 'NULL'), 
            COALESCE(NEW.endzeitpunkt, 'NULL')
        );
    END IF;

    IF OLD.route IS NULL OR NEW.route IS NULL OR OLD.route != NEW.route THEN
        INSERT INTO changelog (table_name, operation_type, record_id, changed_column, old_value, new_value)
        VALUES (
            'fahrt', 
            'UPDATE', 
            OLD.fahrtid, 
            'route', 
            COALESCE(OLD.route, 'NULL'), 
            COALESCE(NEW.route, 'NULL')
        );
    END IF;
END $$

DELIMITER ;
