DROP TRIGGER IF EXISTS trg_update_geraet_installation;

DELIMITER $$

CREATE TRIGGER trg_update_geraet_installation
AFTER UPDATE ON geraet_installation
FOR EACH ROW
BEGIN
    IF OLD.geraetid IS NULL OR NEW.geraetid IS NULL OR OLD.geraetid != NEW.geraetid THEN
        INSERT INTO changelog (table_name, operation_type, record_id, changed_column, old_value, new_value)
        VALUES (
            'geraet_installation', 
            'UPDATE', 
            OLD.geraet_installationid, 
            'geraetid', 
            COALESCE(CAST(OLD.geraetid AS CHAR), 'NULL'), 
            COALESCE(CAST(NEW.geraetid AS CHAR), 'NULL')
        );
    END IF;

    IF OLD.fahrzeugid IS NULL OR NEW.fahrzeugid IS NULL OR OLD.fahrzeugid != NEW.fahrzeugid THEN
        INSERT INTO changelog (table_name, operation_type, record_id, changed_column, old_value, new_value)
        VALUES (
            'geraet_installation', 
            'UPDATE', 
            OLD.geraet_installationid, 
            'fahrzeugid', 
            COALESCE(CAST(OLD.fahrzeugid AS CHAR), 'NULL'), 
            COALESCE(CAST(NEW.fahrzeugid AS CHAR), 'NULL')
        );
    END IF;

    IF OLD.einbau_datum IS NULL OR NEW.einbau_datum IS NULL OR OLD.einbau_datum != NEW.einbau_datum THEN
        INSERT INTO changelog (table_name, operation_type, record_id, changed_column, old_value, new_value)
        VALUES (
            'geraet_installation', 
            'UPDATE', 
            OLD.geraet_installationid, 
            'einbau_datum', 
            COALESCE(CAST(OLD.einbau_datum AS CHAR), 'NULL'), 
            COALESCE(CAST(NEW.einbau_datum AS CHAR), 'NULL')
        );
    END IF;

    IF OLD.ausbau_datum IS NULL OR NEW.ausbau_datum IS NULL OR OLD.ausbau_datum != NEW.ausbau_datum THEN
        INSERT INTO changelog (table_name, operation_type, record_id, changed_column, old_value, new_value)
        VALUES (
            'geraet_installation', 
            'UPDATE', 
            OLD.geraet_installationid, 
            'ausbau_datum', 
            COALESCE(CAST(OLD.ausbau_datum AS CHAR), 'NULL'), 
            COALESCE(CAST(NEW.ausbau_datum AS CHAR), 'NULL')
        );
    END IF;
END $$

DELIMITER ;
