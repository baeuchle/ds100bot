CREATE TABLE IF NOT EXISTS "last" (
  `subject` TEXT NOT NULL,
  `content` TEXT
);
CREATE TABLE IF NOT EXISTS "shortstore" (
  `id` TEXT NOT NULL,
  `Abk` TEXT NOT NULL,
  `Name` TEXT NOT NULL,
  `Kurzname` TEXT,
  `Datenliste` TEXT,
  `source` TEXT,
  PRIMARY KEY(`id`)
);
CREATE TABLE IF NOT EXISTS "sources" (
  "source_id" TEXT NOT NULL,
  "type" TEXT,
  "explicit_source" TEXT NOT NULL,
  "is_default" INTEGER NOT NULL DEFAULT 0 CHECK(is_default in (0,1))
);
CREATE TABLE IF NOT EXISTS "magic_hashtags" (
  "source_id" TEXT NOT NULL,
  "magic_hashtag" TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS "blacklist" (
  `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
  `source` TEXT NOT NULL,
  `Abk` TEXT NOT NULL
);
CREATE TABLE "requestlog" (
  "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
  "explicit_source" TEXT,
  "active_magic" TEXT NOT NULL,
  "type" TEXT,
  "abbreviation" TEXT NOT NULL,
  "request_date" TEXT NOT NULL,
  "derived_source" TEXT NOT NULL,
  "status" TEXT NOT NULL
);
