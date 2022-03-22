# pylint: disable=C0114

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
    if row is None:
        return None
    return row[0]

def is_same_version(sql):
    return get_last_hash(sql) == git_object.hash()

def store_version(sql):
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
    return git_object.changelog(last_hash).replace('•', '\u200b•')

def notify_new_version(twitter, database):
    if is_same_version(database):
        return
    status = f"Ich twittere nun von Version {git_object.describe()}"
    cl = get_changelog(database)
    if cl.strip() != "":
        status += ":\n" + cl
    if twitter.tweet(
            status,
            auto_populate_reply_metadata=True
            ) > 0:
        store_version(database)
