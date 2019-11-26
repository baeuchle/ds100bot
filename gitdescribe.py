import datetime
import tweepy
from GitVersion import Git

git_object = Git()
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
        return None
    return row[0]

def is_same_version(sql):
    return get_last_hash(sql) == git_object.hash()

def store_version(sql):
    if sql.readonly:
        return
    for subj, cont in (
        ('gitdescribe', git_object.describe()),
        ('githash', git_object.hash())
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

def get_changelog(sqlcursor):
    last_hash = get_last_hash(sqlcursor)
    return git_object.changelog(last_hash)

def notify_new_version(sql, twapi, verbose):
    if is_same_version(sql):
        return
    status = "Ich twittere nun von Version {}".format(git_object.describe())
    cl = get_changelog(sql)
    if not cl.strip() == "":
        status += ":\n" + cl
    if len(status) > 280:
        status = status[0:280]
    if twapi.tweet(
            status,
            auto_populate_reply_metadata=True
            ) > 0:
        store_version(sql)
