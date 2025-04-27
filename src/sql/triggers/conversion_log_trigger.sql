DROP TRIGGER IF EXISTS trg_update_conversion_log;

DELIMITER $$

CREATE TRIGGER trg_update_conversion_log
AFTER UPDATE ON conversion_log
FOR EACH ROW
BEGIN
    IF OLD.source_table IS NULL OR NEW.source_table IS NULL OR OLD.source_table != NEW.source_table THEN
        INSERT INTO changelog (table_name, operation_type, record_id, changed_column, old_value, new_value)
        VALUES (
            'conversion_log', 
            'UPDATE', 
            OLD.id, 
            'source_table', 
            COALESCE(OLD.source_table, 'NULL'), 
            COALESCE(NEW.source_table, 'NULL')
        );
    END IF;

    IF OLD.target_collection IS NULL OR NEW.target_collection IS NULL OR OLD.target_collection != NEW.target_collection THEN
        INSERT INTO changelog (table_name, operation_type, record_id, changed_column, old_value, new_value)
        VALUES (
            'conversion_log', 
            'UPDATE', 
            OLD.id, 
            'target_collection', 
            COALESCE(OLD.target_collection, 'NULL'), 
            COALESCE(NEW.target_collection, 'NULL')
        );
    END IF;

    IF OLD.status IS NULL OR NEW.status IS NULL OR OLD.status != NEW.status THEN
        INSERT INTO changelog (table_name, operation_type, record_id, changed_column, old_value, new_value)
        VALUES (
            'conversion_log', 
            'UPDATE', 
            OLD.id, 
            'status', 
            COALESCE(OLD.status, 'NULL'), 
            COALESCE(NEW.status, 'NULL')
        );
    END IF;

    IF OLD.duration_seconds IS NULL OR NEW.duration_seconds IS NULL OR OLD.duration_seconds != NEW.duration_seconds THEN
        INSERT INTO changelog (table_name, operation_type, record_id, changed_column, old_value, new_value)
        VALUES (
            'conversion_log', 
            'UPDATE', 
            OLD.id, 
            'duration_seconds', 
            COALESCE(CAST(OLD.duration_seconds AS CHAR), 'NULL'), 
            COALESCE(CAST(NEW.duration_seconds AS CHAR), 'NULL')
        );
    END IF;

    IF OLD.timestamp IS NULL OR NEW.timestamp IS NULL OR OLD.timestamp != NEW.timestamp THEN
        INSERT INTO changelog (table_name, operation_type, record_id, changed_column, old_value, new_value)
        VALUES (
            'conversion_log', 
            'UPDATE', 
            OLD.id, 
            'timestamp', 
            COALESCE(CAST(OLD.timestamp AS CHAR), 'NULL'), 
            COALESCE(CAST(NEW.timestamp AS CHAR), 'NULL')
        );
    END IF;
END $$

DELIMITER ;
