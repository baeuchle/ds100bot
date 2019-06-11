import datetime
import version

def get_last_version(cursor):
    cursor.execute("""
        SELECT
            content
        FROM
            last
        WHERE
            subject = 'gitdescribe'
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
        UPDATE
            last
        SET
            content = ?
        WHERE
            subject = 'gitdescribe'
        """,
        (
         get_version(),
        )
        )
