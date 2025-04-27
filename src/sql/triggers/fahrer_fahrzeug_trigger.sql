DROP TRIGGER IF EXISTS trg_update_fahrer_fahrzeug;

DELIMITER $$

CREATE TRIGGER trg_update_fahrer_fahrzeug
AFTER UPDATE ON fahrer_fahrzeug
FOR EACH ROW
BEGIN
    IF OLD.gueltig_ab IS NULL OR NEW.gueltig_ab IS NULL OR OLD.gueltig_ab != NEW.gueltig_ab THEN
        INSERT INTO changelog (table_name, operation_type, record_id, changed_column, old_value, new_value)
        VALUES (
            'fahrer_fahrzeug', 
            'UPDATE', 
            OLD.fahrerid, 
            'gueltig_ab', 
            COALESCE(CAST(OLD.gueltig_ab AS CHAR), 'NULL'), 
            COALESCE(CAST(NEW.gueltig_ab AS CHAR), 'NULL')
        );
    END IF;

    IF OLD.gueltig_bis IS NULL OR NEW.gueltig_bis IS NULL OR OLD.gueltig_bis != NEW.gueltig_bis THEN
        INSERT INTO changelog (table_name, operation_type, record_id, changed_column, old_value, new_value)
        VALUES (
            'fahrer_fahrzeug', 
            'UPDATE', 
            OLD.fahrerid, 
            'gueltig_bis', 
            COALESCE(CAST(OLD.gueltig_bis AS CHAR), 'NULL'), 
            COALESCE(CAST(NEW.gueltig_bis AS CHAR), 'NULL')
        );
    END IF;
END $$

DELIMITER ;
