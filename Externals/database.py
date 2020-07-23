# pylint: disable=C0114

import sqlite3
import datetime
import Persistence.log as log
from GitVersion import Git
log_ = log.getLogger(__name__)

class Database:
    def __init__(self, mode):
        git_ = Git()
        self.sql = sqlite3.connect(git_.topdir() + '/info.db')
        self.sql.row_factory = sqlite3.Row
        self.cursor = self.sql.cursor()
        self.readonly = (mode == 'readonly')
        if self.readonly:
            log_.info('Running with readonly database')

    def close_sucessfully(self):
        self.cursor.close()
        if not self.readonly:
            self.sql.commit()
        self.sql.close()

    def magic_hashtags(self):
        self.cursor.execute("""
            SELECT
                distinct(magic_hashtag)
            FROM
                sources
            WHERE
                magic_hashtag IS NOT NULL
        """)
        results = ["#" + row[0] for row in self.cursor.fetchall()]
        return "(" + (" OR ".join(results)) + ")", results

    def count_status(self, since):
        self.cursor.execute("""
            SELECT
                status AS status,
                count(status) AS count
            FROM
                requests
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
                    CASE
                        WHEN SUBSTR(ds100_id, 1, 1) = '#' THEN REPLACE(ds100_id, '#:', '#DS:')
                        WHEN SUBSTR(ds100_id, 1, 1) = '$' THEN REPLACE(ds100_id, '$:', '$DS:')
                        ELSE '#DS:' || ds100_id
                    END AS short
                FROM
                    requests
                WHERE
                    status = 'found'
                    AND
                    request_date >= ?
            )
            GROUP BY S
            ORDER BY C DESC
            LIMIT 0, 20
        """, (since, ))
        return self.cursor.fetchall()

    def popular_sources(self, since):
        self.cursor.execute("""
            SELECT
                source AS S,
                count(source) AS C
            FROM (
                SELECT
                    CASE
                        WHEN ds100_id LIKE '#:%' THEN 'DS'
                        WHEN ds100_id LIKE '$:%' THEN 'DS'
                        WHEN ds100_id LIKE '%:%' THEN substr(ds100_id, 2, instr(ds100_id, ':') - 2)
                        ELSE 'DS'
                    END AS source
                FROM
                    requests
                WHERE
                    status = 'found'
                    AND
                    request_date >= ?
            )
            GROUP BY S
            ORDER BY C DESC
            LIMIT 0, 20
        """, (since, ))
        return self.cursor.fetchall()

    def dumplist(self, source_id):
        self.cursor.execute("""
            SELECT
                Abk,
                Name
            FROM
                shortstore
            WHERE
                source = ?
            ORDER BY
                Abk
        """, (source_id, )
        )
        return self.cursor.fetchall()

    def purge_data(self):
        log_.info("Purging old data...")
        self.cursor.execute("DELETE FROM shortstore")
        self.cursor.execute("DELETE FROM sources")

    def insert_source(self, access, source_id, is_def):
        self.cursor.execute("""
            INSERT INTO sources(
                source_id,
                type,
                magic_hashtag,
                explicit_source,
                is_default
            ) VALUES (?, ?, ?, ?, ?)
        """,
            (source_id,
            access.type,
            access.magic_hashtag,
            access.explicit_source,
            is_def
            )
        )

    def insert_datalist(self, data_list, source_id):
        for row in data_list:
            try:
                self.insert_data(row, data_list.id, source_id)
            except sqlite3.Error as sqle:
                log_.critical("%s: Error inserting data: %s", data_list.position, sqle)
                return False
        return True

    def insert_data(self, datarow, data_id, source_id):
        if self.readonly:
            return
        primkey = '{}::{}'.format(data_id, datarow.abbr)
        self.cursor.execute("""
            INSERT OR REPLACE
            INTO shortstore(
                id,
                Abk,
                Name,
                Kurzname,
                source
            )
            VALUES
            (?,?,?,?,?)
        """,
             (primkey
            , datarow.abbr
            , datarow.long
            , datarow.add
            , source_id
            , )
        )

    def log_request(self, result):
        if self.readonly:
            return
        self.cursor.execute("""
            INSERT INTO
                requests(
                    ds100_id
                  , request_date
                  , status
                    )
                VALUES (?,?,?)
            """,
               (result.normalized()
              , datetime.datetime.today().strftime('%Y%m%d')
              , result.status
              , ))
