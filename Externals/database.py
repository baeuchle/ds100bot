# pylint: disable=C0114

import datetime
import logging
import sqlite3

from GitVersion import Git

def setup_database(cli_args, network):
    return Database(cli_args.readwrite, network)

logger = logging.getLogger('bot.db')

class Database:
    def __init__(self, readwrite, network):
        git_ = Git()
        self.sql = sqlite3.connect(git_.topdir() + '/info.db')
        self.sql.row_factory = sqlite3.Row
        self.cursor = self.sql.cursor()
        self.readonly = not readwrite
        self.network = network
        if self.readonly:
            logger.info('Running with readonly database')
        logger.debug("Created database connection")

    def commit(self):
        if not self.readonly:
            self.sql.commit()
            logger.debug("Committing database content")

    def close_sucessfully(self):
        self.cursor.close()
        self.commit()
        self.sql.close()

    def magic_hashtags(self):
        self.cursor.execute("""
            SELECT
                distinct(magic_hashtag)
            FROM
                magic_hashtags
        """)
        tags = [row[0] for row in self.cursor.fetchall()]
        mht = ['#' + t for t in tags if ord(t[0]) < 2**16]
        emojis = [t for t in tags if ord(t[0]) >= 2**16]
        return mht, emojis

    def count_status(self, since):
        self.cursor.execute("""
            SELECT
                status AS status,
                count(status) AS count
            FROM
                requestlog
            WHERE
                request_date >= ?
            GROUP BY
                status
        """, (since, ))
        return {row[0]: row[1] for row in self.cursor.fetchall()}

    def popular_abbrs(self, since):
        self.cursor.execute("""
            SELECT
                short AS S,
                count(short) AS C
            FROM (
                SELECT
                    type || derived_source || ':' || abbreviation AS short
                FROM
                    requestlog
                WHERE
                    status = 'found'
                    AND
                    request_date >= ?
            )
            GROUP BY S
            ORDER BY C DESC
            LIMIT 0, 15
        """, (since, ))
        return self.cursor.fetchall()

    def popular_sources(self, since):
        self.cursor.execute("""
            SELECT
                derived_source AS S,
                count(derived_source) AS C
            FROM
                requestlog
            WHERE
                status = 'found'
                AND
                request_date >= ?
            GROUP BY S
            ORDER BY C DESC
            LIMIT 0, 5
        """, (since, ))
        return self.cursor.fetchall()

    def dumplist(self, source_id):
        self.cursor.execute("""
            SELECT
                Abk,
                Name,
                Kurzname,
                Datenliste
            FROM
                shortstore
            WHERE
                source = ?
            ORDER BY
                Abk
        """, (source_id, )
        )
        return self.cursor.fetchall()

    def dumpblack(self):
        self.cursor.execute("""
            SELECT
                blacklist.Abk,
                shortstore.Name,
                shortstore.Kurzname,
                shortstore.Datenliste
            FROM
                blacklist
            JOIN shortstore ON blacklist.Abk = shortstore.Abk
            JOIN sources ON sources.source_id = shortstore.source
            WHERE
                sources.type = '#'
            AND
                sources.is_default

            ORDER BY
                blacklist.Abk
        """, ()
        )
        return self.cursor.fetchall()

    def purge_data(self):
        logger.info("Purging old data...")
        self.cursor.execute("DELETE FROM shortstore")
        self.cursor.execute("DELETE FROM sources")
        self.cursor.execute("DELETE FROM magic_hashtags")

    def insert_source(self, access, source_id, is_def):
        self.cursor.execute("""
            INSERT INTO sources(
                source_id,
                type,
                explicit_source,
                is_default
            ) VALUES (?, ?, ?, ?)
        """,
            (source_id,
            access.type,
            access.explicit_source,
            is_def
            )
        )

    def insert_magic_hashtag(self, source_id, mht):
        self.cursor.execute("""
            INSERT INTO magic_hashtags(
                source_id,
                magic_hashtag
            ) VALUES (?, ?)
        """,
            (source_id,
             mht
            )
        )


    def insert_datalist(self, data_list, source_id):
        for row in data_list:
            try:
                self.insert_data(row, data_list.id, source_id)
            except sqlite3.Error as sqle:
                logger.critical("%s: Error inserting data: %s", data_list.position, sqle)
                return False
        return True

    def insert_data(self, datarow, data_id, source_id):
        primkey = '{}::{}'.format(data_id, datarow.abbr)
        self.cursor.execute("""
            INSERT OR REPLACE
            INTO shortstore(
                id,
                Abk,
                Name,
                Kurzname,
                Datenliste,
                source
            )
            VALUES
            (?,?,?,?,?,?)
        """,
             (primkey
            , datarow.abbr
            , datarow.long
            , datarow.add
            , data_id
            , source_id
            , )
        )

    def log_request(self, result):
        try:
            self.cursor.execute("""
                INSERT INTO
                    requestlog(
                        explicit_source,
                        active_magic,
                        type,
                        abbreviation,
                        derived_source,
                        request_date,
                        status,
                        network
                    )
                    VALUES (?,?,?,?,?,?,?,?)
            """,
             (result.candidate.explicit_source
            , result.candidate.magic_hashtag
            , result.candidate.type_character
            , result.abbr
            , result.default_source
            , datetime.datetime.today().strftime('%Y%m%d')
            , result.status
            , self.network
            ,
            ))
        except sqlite3.Error as sqle:
            logger.error("Cannot insert request: %s", sqle)
            logger.error("Missing data: %s %s %s",
                   result.normalized()
                  , datetime.datetime.today().strftime('%Y%m%d')
                  , result.status
                  )
