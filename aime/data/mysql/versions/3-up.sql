ALTER TABLE achievement 
CHANGE achevement_id achievement_id int(11) NOT NULL;

UPDATE schema_ver
    SET version = 4
    WHERE version = 3;