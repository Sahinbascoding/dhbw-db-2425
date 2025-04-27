DROP TRIGGER IF EXISTS trg_update_wartung;

DELIMITER $$

CREATE TRIGGER trg_update_wartung
AFTER UPDATE ON wartung
FOR EACH ROW
BEGIN
    IF OLD.fahrzeugid IS NULL OR NEW.fahrzeugid IS NULL OR OLD.fahrzeugid != NEW.fahrzeugid THEN
        INSERT INTO changelog (table_name, operation_type, record_id, changed_column, old_value, new_value)
        VALUES (
            'wartung', 
            'UPDATE', 
            OLD.wartungid, 
            'fahrzeugid', 
            COALESCE(CAST(OLD.fahrzeugid AS CHAR), 'NULL'), 
            COALESCE(CAST(NEW.fahrzeugid AS CHAR), 'NULL')
        );
    END IF;

    IF OLD.datum IS NULL OR NEW.datum IS NULL OR OLD.datum != NEW.datum THEN
        INSERT INTO changelog (table_name, operation_type, record_id, changed_column, old_value, new_value)
        VALUES (
            'wartung', 
            'UPDATE', 
            OLD.wartungid, 
            'datum', 
            COALESCE(CAST(OLD.datum AS CHAR), 'NULL'), 
            COALESCE(CAST(NEW.datum AS CHAR), 'NULL')
        );
    END IF;

    IF OLD.beschreibung IS NULL OR NEW.beschreibung IS NULL OR OLD.beschreibung != NEW.beschreibung THEN
        INSERT INTO changelog (table_name, operation_type, record_id, changed_column, old_value, new_value)
        VALUES (
            'wartung', 
            'UPDATE', 
            OLD.wartungid, 
            'beschreibung', 
            COALESCE(OLD.beschreibung, 'NULL'), 
            COALESCE(NEW.beschreibung, 'NULL')
        );
    END IF;
END $$

DELIMITER ;
