DROP TRIGGER IF EXISTS trg_update_fahrzeug;

DELIMITER $$

CREATE TRIGGER trg_update_fahrzeug
AFTER UPDATE ON fahrzeug
FOR EACH ROW
BEGIN
    IF OLD.hersteller IS NULL OR NEW.hersteller IS NULL OR OLD.hersteller != NEW.hersteller THEN
        INSERT INTO changelog (table_name, operation_type, record_id, changed_column, old_value, new_value)
        VALUES (
            'fahrzeug', 
            'UPDATE', 
            OLD.fahrzeugid, 
            'hersteller', 
            COALESCE(OLD.hersteller, 'NULL'), 
            COALESCE(NEW.hersteller, 'NULL')
        );
    END IF;

    IF OLD.modell IS NULL OR NEW.modell IS NULL OR OLD.modell != NEW.modell THEN
        INSERT INTO changelog (table_name, operation_type, record_id, changed_column, old_value, new_value)
        VALUES (
            'fahrzeug', 
            'UPDATE', 
            OLD.fahrzeugid, 
            'modell', 
            COALESCE(OLD.modell, 'NULL'), 
            COALESCE(NEW.modell, 'NULL')
        );
    END IF;

    IF OLD.baujahr IS NULL OR NEW.baujahr IS NULL OR OLD.baujahr != NEW.baujahr THEN
        INSERT INTO changelog (table_name, operation_type, record_id, changed_column, old_value, new_value)
        VALUES (
            'fahrzeug', 
            'UPDATE', 
            OLD.fahrzeugid, 
            'baujahr', 
            COALESCE(CAST(OLD.baujahr AS CHAR), 'NULL'), 
            COALESCE(CAST(NEW.baujahr AS CHAR), 'NULL')
        );
    END IF;
END $$

DELIMITER ;
