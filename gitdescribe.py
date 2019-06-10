import datetime
import version

def get_last_version(cursor):
    cursor.execute("""
        SELECT
            gitdescribe
        FROM
            last
        ORDER BY time
        DESC LIMIT 1
        """)
    row = cursor.fetchone()
    if row == None:
        return '0000000000000000000000000000000000000000'
    return row[0]

def get_version():
    return version.git

def is_same_version(cursor):
    return get_last_version(cursor) == get_version()

def store_version(cursor):
    # store last answer time
    cursor.execute("""
        INSERT INTO
            last(
                time,
                gitdescribe
            )
        VALUES(?,?)
        """,
        (datetime.datetime.now().strftime('%Y%m%d%H%M%S'),
         get_version()
        )
        )
