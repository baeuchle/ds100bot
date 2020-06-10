PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "sourceflags" (
	`sigil`	TEXT NOT NULL,
	`abbr`	TEXT NOT NULL,
	`sourcename`	TEXT NOT NULL,
	`magictag`	TEXT
);
DELETE FROM sourceflags;
INSERT INTO sourceflags VALUES('#','DS','ds100','DS100');
INSERT INTO sourceflags VALUES('$','DS','strecken','DS100');
INSERT INTO sourceflags VALUES('#','VGF','vgfhst',NULL);
INSERT INTO sourceflags VALUES('$','VGF','vgfstrecken',NULL);
INSERT INTO sourceflags VALUES('$','DS','benannte_strecken','DS100');
INSERT INTO sourceflags VALUES('#','DB','ds100',NULL);
INSERT INTO sourceflags VALUES('#','BOT','gimmick',NULL);
INSERT INTO sourceflags VALUES('#','FFM','vgfhst','_FFM');
INSERT INTO sourceflags VALUES('$','FFM','vgfstrecken','_FFM');
INSERT INTO sourceflags VALUES('#','ÖBB','db640','DB640');
INSERT INTO sourceflags VALUES('#','LP','leitpunkte','_LP');
INSERT INTO sourceflags VALUES('#','NOR','banenor','_NSB');
INSERT INTO sourceflags VALUES('#','VOR','wien_vor','_VOR');
INSERT INTO sourceflags VALUES('#','NL','nederlands','_NL');
INSERT INTO sourceflags VALUES('#','UK','raildeliverygroup','_UK');
INSERT INTO sourceflags VALUES('#','UK','nationalrail','_UK');
INSERT INTO sourceflags VALUES('#','HHE','hhe','_HHE');
COMMIT;
