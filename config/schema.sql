CREATE TABLE IF NOT EXISTS "last" (
	`subject`	TEXT NOT NULL,
	`content`	TEXT
);
CREATE TABLE IF NOT EXISTS "requests" (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	`ds100_id`	TEXT NOT NULL,
	`request_date`	TEXT NOT NULL,
	`status`	INTEGER
);
CREATE TABLE IF NOT EXISTS "shortstore" (
	`id`	TEXT NOT NULL,
	`Abk`	TEXT NOT NULL,
	`Name`	TEXT NOT NULL,
	`Kurzname`	TEXT,
	`gueltigvon`	TEXT,
	`source`	TEXT,
	PRIMARY KEY(`id`)
);
CREATE TABLE IF NOT EXISTS "sourceflags" ( `sigil` TEXT NOT NULL, `abbr` TEXT NOT NULL, `sourcename` TEXT NOT NULL );
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
CREATE TABLE IF NOT EXISTS "blacklist" (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	`source`	TEXT NOT NULL,
	`Abk`	TEXT NOT NULL
);
/* No STAT tables available */
