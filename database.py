import sqlite3

class Database:
    def __init__(self, db, verbose):
        self.verbose = verbose
        self.sql = sqlite3.connect('info.db')
        self.sql.row_factory = sqlite3.Row
        self.cursor = self.sql.cursor()
        self.readonly = (db == 'readonly')
        if self.verbose >= 0 and self.readonly:
            print('Running with readonly database')

    def close_sucessfully(self):
        self.cursor.close()
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
