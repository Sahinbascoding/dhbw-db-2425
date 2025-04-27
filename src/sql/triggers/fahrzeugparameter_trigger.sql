DROP TRIGGER IF EXISTS trg_update_fahrzeugparameter;

DELIMITER $$

CREATE TRIGGER trg_update_fahrzeugparameter
AFTER UPDATE ON fahrzeugparameter
FOR EACH ROW
BEGIN
    IF OLD.fahrtid IS NULL OR NEW.fahrtid IS NULL OR OLD.fahrtid != NEW.fahrtid THEN
        INSERT INTO changelog (table_name, operation_type, record_id, changed_column, old_value, new_value)
        VALUES (
            'fahrzeugparameter', 
            'UPDATE', 
            OLD.fahrzeugparameterid, 
            'fahrtid', 
            COALESCE(CAST(OLD.fahrtid AS CHAR), 'NULL'), 
            COALESCE(CAST(NEW.fahrtid AS CHAR), 'NULL')
        );
    END IF;

    IF OLD.zeitstempel IS NULL OR NEW.zeitstempel IS NULL OR OLD.zeitstempel != NEW.zeitstempel THEN
        INSERT INTO changelog (table_name, operation_type, record_id, changed_column, old_value, new_value)
        VALUES (
            'fahrzeugparameter', 
            'UPDATE', 
            OLD.fahrzeugparameterid, 
            'zeitstempel', 
            COALESCE(CAST(OLD.zeitstempel AS CHAR), 'NULL'), 
            COALESCE(CAST(NEW.zeitstempel AS CHAR), 'NULL')
        );
    END IF;

    IF OLD.geschwindigkeit IS NULL OR NEW.geschwindigkeit IS NULL OR OLD.geschwindigkeit != NEW.geschwindigkeit THEN
        INSERT INTO changelog (table_name, operation_type, record_id, changed_column, old_value, new_value)
        VALUES (
            'fahrzeugparameter', 
            'UPDATE', 
            OLD.fahrzeugparameterid, 
            'geschwindigkeit', 
            COALESCE(CAST(OLD.geschwindigkeit AS CHAR), 'NULL'), 
            COALESCE(CAST(NEW.geschwindigkeit AS CHAR), 'NULL')
        );
    END IF;

    IF OLD.motortemperatur IS NULL OR NEW.motortemperatur IS NULL OR OLD.motortemperatur != NEW.motortemperatur THEN
        INSERT INTO changelog (table_name, operation_type, record_id, changed_column, old_value, new_value)
        VALUES (
            'fahrzeugparameter', 
            'UPDATE', 
            OLD.fahrzeugparameterid, 
            'motortemperatur', 
            COALESCE(CAST(OLD.motortemperatur AS CHAR), 'NULL'), 
            COALESCE(CAST(NEW.motortemperatur AS CHAR), 'NULL')
        );
    END IF;

    IF OLD.batterie IS NULL OR NEW.batterie IS NULL OR OLD.batterie != NEW.batterie THEN
        INSERT INTO changelog (table_name, operation_type, record_id, changed_column, old_value, new_value)
        VALUES (
            'fahrzeugparameter', 
            'UPDATE', 
            OLD.fahrzeugparameterid, 
            'batterie', 
            COALESCE(CAST(OLD.batterie AS CHAR), 'NULL'), 
            COALESCE(CAST(NEW.batterie AS CHAR), 'NULL')
        );
    END IF;
END $$

DELIMITER ;
