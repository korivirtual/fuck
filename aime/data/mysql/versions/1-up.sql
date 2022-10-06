ALTER TABLE profile
    ADD COLUMN name varchar(20) AFTER use_count;

UPDATE schema_ver
    SET version = 2
    WHERE version = 1;