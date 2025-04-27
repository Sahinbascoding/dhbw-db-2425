DROP TRIGGER IF EXISTS trg_update_diagnose;

DELIMITER $$

CREATE TRIGGER trg_update_diagnose
AFTER UPDATE ON diagnose
FOR EACH ROW
BEGIN
    IF OLD.fahrtid IS NULL OR NEW.fahrtid IS NULL OR OLD.fahrtid != NEW.fahrtid THEN
        INSERT INTO changelog (table_name, operation_type, record_id, changed_column, old_value, new_value)
        VALUES (
            'diagnose', 
            'UPDATE', 
            OLD.diagnoseid, 
            'fahrtid', 
            COALESCE(CAST(OLD.fahrtid AS CHAR), 'NULL'), 
            COALESCE(CAST(NEW.fahrtid AS CHAR), 'NULL')
        );
    END IF;

    IF OLD.zeitstempel IS NULL OR NEW.zeitstempel IS NULL OR OLD.zeitstempel != NEW.zeitstempel THEN
        INSERT INTO changelog (table_name, operation_type, record_id, changed_column, old_value, new_value)
        VALUES (
            'diagnose', 
            'UPDATE', 
            OLD.diagnoseid, 
            'zeitstempel', 
            COALESCE(CAST(OLD.zeitstempel AS CHAR), 'NULL'), 
            COALESCE(CAST(NEW.zeitstempel AS CHAR), 'NULL')
        );
    END IF;

    IF OLD.fehlercode IS NULL OR NEW.fehlercode IS NULL OR OLD.fehlercode != NEW.fehlercode THEN
        INSERT INTO changelog (table_name, operation_type, record_id, changed_column, old_value, new_value)
        VALUES (
            'diagnose', 
            'UPDATE', 
            OLD.diagnoseid, 
            'fehlercode', 
            COALESCE(OLD.fehlercode, 'NULL'), 
            COALESCE(NEW.fehlercode, 'NULL')
        );
    END IF;

    IF OLD.beschreibung IS NULL OR NEW.beschreibung IS NULL OR OLD.beschreibung != NEW.beschreibung THEN
        INSERT INTO changelog (table_name, operation_type, record_id, changed_column, old_value, new_value)
        VALUES (
            'diagnose', 
            'UPDATE', 
            OLD.diagnoseid, 
            'beschreibung', 
            COALESCE(OLD.beschreibung, 'NULL'), 
            COALESCE(NEW.beschreibung, 'NULL')
        );
    END IF;
END $$

DELIMITER ;
