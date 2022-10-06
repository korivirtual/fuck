ALTER TABLE user
    CHANGE COLUMN `username` `username` VARCHAR(10) NULL DEFAULT NULL;

UPDATE schema_ver
    SET version = 2
    WHERE version = 3;
