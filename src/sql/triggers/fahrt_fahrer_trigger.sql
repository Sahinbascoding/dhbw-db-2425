DROP TRIGGER IF EXISTS trg_update_fahrt_fahrer;

DELIMITER $$

CREATE TRIGGER trg_update_fahrt_fahrer
AFTER UPDATE ON fahrt_fahrer
FOR EACH ROW
BEGIN
    IF OLD.fahrtid IS NULL OR NEW.fahrtid IS NULL OR OLD.fahrtid != NEW.fahrtid THEN
        INSERT INTO changelog (table_name, operation_type, record_id, changed_column, old_value, new_value)
        VALUES (
            'fahrt_fahrer', 
            'UPDATE', 
            OLD.fahrtid, 
            'fahrtid', 
            COALESCE(CAST(OLD.fahrtid AS CHAR), 'NULL'), 
            COALESCE(CAST(NEW.fahrtid AS CHAR), 'NULL')
        );
    END IF;

    IF OLD.fahrerid IS NULL OR NEW.fahrerid IS NULL OR OLD.fahrerid != NEW.fahrerid THEN
        INSERT INTO changelog (table_name, operation_type, record_id, changed_column, old_value, new_value)
        VALUES (
            'fahrt_fahrer', 
            'UPDATE', 
            OLD.fahrtid, 
            'fahrerid', 
            COALESCE(CAST(OLD.fahrerid AS CHAR), 'NULL'), 
            COALESCE(CAST(NEW.fahrerid AS CHAR), 'NULL')
        );
    END IF;
END $$

DELIMITER ;
