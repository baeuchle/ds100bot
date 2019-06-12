import datetime
import version

def get_last_hash(cursor):
    cursor.execute("""
        SELECT
            content
        FROM
            last
        WHERE
            subject = 'githash'
        """)
    row = cursor.fetchone()
    if row == None:
        return '0000000000000000000000000000000000000000'
    return row[0]

def get_hash():
    return version.githash

def is_same_version(cursor):
    return get_last_hash(cursor) == get_hash()

def store_version(cursor):
    for subj, cont in (
        ('gitdescribe', get_version()),
        ('githash', get_hash())
        ):
        # store last answer time
        cursor.execute("""
            UPDATE
                last
            SET
                content = ?
            WHERE
                subject = ?
            """,
            (
             cont, subj,
            )
            )

def get_version():
    return version.gitdescribe

def get_changelog(sqlcursor):
    last_hash = get_last_hash(sqlcursor)
    if last_hash in version.changelog:
        return version.changelog[last_hash]
    return ""

def notify_new_version(sqlcursor, api, readwrite):
    if is_same_version(sqlcursor):
        return
    status = "Ich twittere nun von Version {}".format(get_version())
    cl = get_changelog(sqlcursor)
    if not cl == "":
        status += ":" + cl
    if len(status) > 280:
        status = status[0:280]
    if readwrite:
        api.update_status(status)
    else:
        print("NOT TWEETING:")
    print("Tweet ({} chars):\n{}".format(len(status), status))
