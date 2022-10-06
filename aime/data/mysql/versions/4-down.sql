ALTER TABLE achievement 
CHANGE achievement_id achevement_id int(11) NOT NULL;

UPDATE schema_ver
    SET version = 3
    WHERE version = 4;