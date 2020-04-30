PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "sources" (
	`source_name`	TEXT NOT NULL,
	`abk_col`	TEXT NOT NULL,
	`name_col`	TEXT NOT NULL,
	`kurz_col`	TEXT,
	`valid_from_col`	TEXT,
	`replace_links`	INTEGER NOT NULL,
	`delimiter`	TEXT NOT NULL,
	`valid_until_col`	TEXT,
	PRIMARY KEY(`source_name`,`source_name`)
);
DELETE FROM sources;
INSERT INTO sources VALUES('ds100','Abk','Name','Kurzname','gültig von',1,';',NULL);
INSERT INTO sources VALUES('gimmick','Abk','Name',NULL,NULL,0,';',NULL);
INSERT INTO sources VALUES('strecken','STRNR','STRKURZN','STRNAME',NULL,1,';',NULL);
INSERT INTO sources VALUES('vgfhst','Abk','Name',NULL,NULL,1,';',NULL);
INSERT INTO sources VALUES('vgfstrecken','Abk','Weg',NULL,NULL,1,';',NULL);
INSERT INTO sources VALUES('benannte_strecken','Abk','Beschreibung','Nummer',NULL,1,';',NULL);
INSERT INTO sources VALUES('db640','Abk','Name',NULL,NULL,1,';',NULL);
INSERT INTO sources VALUES('leitpunkte','Abk','Name',NULL,NULL,0,';',NULL);
INSERT INTO sources VALUES('banenor','Fork','Navn','Strekninger',NULL,1,';',NULL);
COMMIT;
