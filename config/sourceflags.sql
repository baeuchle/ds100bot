PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "sourceflags" (
	`sigil`	TEXT NOT NULL,
	`abbr`	TEXT NOT NULL,
	`sourcename`	TEXT NOT NULL,
	`magictag`	TEXT
);
DELETE FROM sourceflags;
-- national
INSERT INTO sourceflags VALUES('#','AT','db640','_AT');
INSERT INTO sourceflags VALUES('#','AT','db640','DB640');
INSERT INTO sourceflags VALUES('#','CH','ch','_CH');
INSERT INTO sourceflags VALUES('#','DS','ds100','_DE');
INSERT INTO sourceflags VALUES('$','DS','strecken','_DE');
INSERT INTO sourceflags VALUES('$','DS','benannte_strecken','_DE');
INSERT INTO sourceflags VALUES('%','DS','ds301','_DE');
INSERT INTO sourceflags VALUES('&','DS','brw','_DE');
INSERT INTO sourceflags VALUES('#','DS','ds100','DS100');
INSERT INTO sourceflags VALUES('$','DS','strecken','DS100');
INSERT INTO sourceflags VALUES('$','DS','benannte_strecken','DS100');
INSERT INTO sourceflags VALUES('%','DS','ds301','DS100');
INSERT INTO sourceflags VALUES('&','DS','brw','DS100');
INSERT INTO sourceflags VALUES('%','DS','ds301','DS301');
INSERT INTO sourceflags VALUES('&','DS','brw','DS408');
INSERT INTO sourceflags VALUES('#','FR','sncf','_FR');
INSERT INTO sourceflags VALUES('#','LP','leitpunkte','_LP');
INSERT INTO sourceflags VALUES('#','NL','nederlands','_NL');
INSERT INTO sourceflags VALUES('#','NO','banenor','_NO');
INSERT INTO sourceflags VALUES('#','UK','raildeliverygroup','_UK');
INSERT INTO sourceflags VALUES('#','UK','nationalrail','_UK');
INSERT INTO sourceflags VALUES('#','BOT','gimmick',NULL);
-- local
INSERT INTO sourceflags VALUES('#','FFM','vgfhst','_FFM');
INSERT INTO sourceflags VALUES('$','FFM','vgfstrecken','_FFM');
INSERT INTO sourceflags VALUES('/','FFM','vgflinien','_FFM');
INSERT INTO sourceflags VALUES('/','NI','niedersachsen','_NI');
INSERT INTO sourceflags VALUES('#','HH','hhe','_HH');
INSERT INTO sourceflags VALUES('#','W','wien_vor','_W');
-- legacy aliases
INSERT INTO sourceflags VALUES('#','DB','ds100',NULL);
INSERT INTO sourceflags VALUES('#','HHE','hhe',NULL);
INSERT INTO sourceflags VALUES('#','NOR','banenor',NULL);
INSERT INTO sourceflags VALUES('#','NO','banenor','_NSB');
INSERT INTO sourceflags VALUES('#','ÖBB','db640',NULL);
INSERT INTO sourceflags VALUES('#','VGF','vgfhst',NULL);
INSERT INTO sourceflags VALUES('$','VGF','vgfstrecken',NULL);
INSERT INTO sourceflags VALUES('#','VOR','wien_vor','_VOR');
COMMIT;
