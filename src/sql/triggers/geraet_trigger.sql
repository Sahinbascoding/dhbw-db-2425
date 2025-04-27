DROP TRIGGER IF EXISTS trg_update_geraet;

DELIMITER $$

CREATE TRIGGER trg_update_geraet
AFTER UPDATE ON geraet
FOR EACH ROW
BEGIN
    IF OLD.fahrzeugid IS NULL OR NEW.fahrzeugid IS NULL OR OLD.fahrzeugid != NEW.fahrzeugid THEN
        INSERT INTO changelog (table_name, operation_type, record_id, changed_column, old_value, new_value)
        VALUES (
            'geraet',
            'UPDATE',
            OLD.geraetid,
            'fahrzeugid',
            COALESCE(CAST(OLD.fahrzeugid AS CHAR), 'NULL'),
            COALESCE(CAST(NEW.fahrzeugid AS CHAR), 'NULL')
        );
    END IF;

    IF OLD.geraet_typ IS NULL OR NEW.geraet_typ IS NULL OR OLD.geraet_typ != NEW.geraet_typ THEN
        INSERT INTO changelog (table_name, operation_type, record_id, changed_column, old_value, new_value)
        VALUES (
            'geraet',
            'UPDATE',
            OLD.geraetid,
            'geraet_typ',
            COALESCE(OLD.geraet_typ, 'NULL'),
            COALESCE(NEW.geraet_typ, 'NULL')
        );
    END IF;

    IF OLD.hersteller IS NULL OR NEW.hersteller IS NULL OR OLD.hersteller != NEW.hersteller THEN
        INSERT INTO changelog (table_name, operation_type, record_id, changed_column, old_value, new_value)
        VALUES (
            'geraet',
            'UPDATE',
            OLD.geraetid,
            'hersteller',
            COALESCE(OLD.hersteller, 'NULL'),
            COALESCE(NEW.hersteller, 'NULL')
        );
    END IF;

    IF OLD.modell IS NULL OR NEW.modell IS NULL OR OLD.modell != NEW.modell THEN
        INSERT INTO changelog (table_name, operation_type, record_id, changed_column, old_value, new_value)
        VALUES (
            'geraet',
            'UPDATE',
            OLD.geraetid,
            'modell',
            COALESCE(OLD.modell, 'NULL'),
            COALESCE(NEW.modell, 'NULL')
        );
    END IF;
END $$

DELIMITER ;
