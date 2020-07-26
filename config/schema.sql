CREATE TABLE IF NOT EXISTS "last" (
  `subject` TEXT NOT NULL,
  `content` TEXT
);
CREATE TABLE IF NOT EXISTS "requests" (
  `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
  `ds100_id` TEXT NOT NULL,
  `request_date` TEXT NOT NULL,
  `status` INTEGER
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
  "magic_hashtag" TEXT,
  "explicit_source" TEXT NOT NULL,
  "is_default" INTEGER NOT NULL DEFAULT 0 CHECK(is_default in (0,1))
);
CREATE TABLE IF NOT EXISTS "blacklist" (
  `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
  `source` TEXT NOT NULL,
  `Abk` TEXT NOT NULL
);
