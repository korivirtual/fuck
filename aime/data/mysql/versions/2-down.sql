ALTER TABLE profile
    DROP COLUMN name;

UPDATE schema_ver
    SET version = 1
    WHERE version = 2;