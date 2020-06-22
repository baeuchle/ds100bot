# pylint: disable=C0114

import sqlite3
import Persistence.log as log
log_ = log.getLogger(__name__)

class Database:
    def __init__(self, mode):
        self.sql = sqlite3.connect('info.db')
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
                distinct(magictag)
            FROM
                sourceflags
            WHERE
                magictag IS NOT NULL
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
