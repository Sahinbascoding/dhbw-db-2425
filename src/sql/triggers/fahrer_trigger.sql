DROP TRIGGER IF EXISTS trg_update_fahrer;

DELIMITER $$

CREATE TRIGGER trg_update_fahrer
AFTER UPDATE ON fahrer
FOR EACH ROW
BEGIN
    IF OLD.vorname IS NULL OR NEW.vorname IS NULL OR OLD.vorname != NEW.vorname THEN
        INSERT INTO changelog (table_name, operation_type, record_id, changed_column, old_value, new_value)
        VALUES (
            'fahrer', 
            'UPDATE', 
            OLD.fahrerid, 
            'vorname', 
            COALESCE(OLD.vorname, 'NULL'), 
            COALESCE(NEW.vorname, 'NULL')
        );
    END IF;

    IF OLD.nachname IS NULL OR NEW.nachname IS NULL OR OLD.nachname != NEW.nachname THEN
        INSERT INTO changelog (table_name, operation_type, record_id, changed_column, old_value, new_value)
        VALUES (
            'fahrer', 
            'UPDATE', 
            OLD.fahrerid, 
            'nachname', 
            COALESCE(OLD.nachname, 'NULL'), 
            COALESCE(NEW.nachname, 'NULL')
        );
    END IF;

    IF OLD.geburtsdatum IS NULL OR NEW.geburtsdatum IS NULL OR OLD.geburtsdatum != NEW.geburtsdatum THEN
        INSERT INTO changelog (table_name, operation_type, record_id, changed_column, old_value, new_value)
        VALUES (
            'fahrer', 
            'UPDATE', 
            OLD.fahrerid, 
            'geburtsdatum', 
            COALESCE(CAST(OLD.geburtsdatum AS CHAR), 'NULL'), 
            COALESCE(CAST(NEW.geburtsdatum AS CHAR), 'NULL')
        );
    END IF;

    IF OLD.kontakt_nr IS NULL OR NEW.kontakt_nr IS NULL OR OLD.kontakt_nr != NEW.kontakt_nr THEN
        INSERT INTO changelog (table_name, operation_type, record_id, changed_column, old_value, new_value)
        VALUES (
            'fahrer', 
            'UPDATE', 
            OLD.fahrerid, 
            'kontakt_nr', 
            COALESCE(CAST(OLD.kontakt_nr AS CHAR), 'NULL'), 
            COALESCE(CAST(NEW.kontakt_nr AS CHAR), 'NULL')
        );
    END IF;

    IF OLD.email IS NULL OR NEW.email IS NULL OR OLD.email != NEW.email THEN
        INSERT INTO changelog (table_name, operation_type, record_id, changed_column, old_value, new_value)
        VALUES (
            'fahrer', 
            'UPDATE', 
            OLD.fahrerid, 
            'email', 
            COALESCE(OLD.email, 'NULL'), 
            COALESCE(NEW.email, 'NULL')
        );
    END IF;
END $$

DELIMITER ;
