ALTER TABLE user
    CHANGE COLUMN `username` `username` VARCHAR(25) NULL DEFAULT NULL;

UPDATE schema_ver
    SET version = 3
    WHERE version = 2;
