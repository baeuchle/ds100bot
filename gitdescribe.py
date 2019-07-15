import datetime
import tweepy
import version

def get_last_hash(sql):
    sql.cursor.execute("""
        SELECT
            content
        FROM
            last
        WHERE
            subject = 'githash'
        """)
    row = sql.cursor.fetchone()
    if row == None:
        return '0000000000000000000000000000000000000000'
    return row[0]

def get_hash():
    return version.githash

def is_same_version(sql):
    return get_last_hash(sql) == get_hash()

def store_version(sql):
    if sql.readonly:
        return
    for subj, cont in (
        ('gitdescribe', get_version()),
        ('githash', get_hash())
        ):
        # store last answer time
        sql.cursor.execute("""
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

def notify_new_version(sql, twapi, verbose):
    if is_same_version(sql):
        return
    status = "Ich twittere nun von Version {}".format(get_version())
    cl = get_changelog(sql)
    if not cl.strip() == "":
        status += ":" + cl
    if len(status) > 280:
        status = status[0:280]
    if twapi.tweet(
            status,
            auto_populate_reply_metadata=True
            ) > 0:
        store_version(sql)
