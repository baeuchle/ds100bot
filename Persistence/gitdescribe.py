# pylint: disable=C0114

import logging

from GitVersion import Git

logger = logging.getLogger('bot.persistence')

git_object = Git()
def get_last_hash(sql):
    sql.cursor.execute("""
        SELECT
            content
        FROM
            last
        WHERE
            subject = 'githash'
            AND
            network = ?
        """, (sql.network, ))
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
                AND
                network = ?
            """,
            (
             cont, subj, sql.network,
            )
            )
    sql.commit()

def get_changelog(sqlcursor):
    last_hash = get_last_hash(sqlcursor)
    return git_object.changelog(last_hash).replace('•', '\u200b•')

def notify_new_version(twitter, database):
    if is_same_version(database):
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug("Using same version as last time: %s", git_object.describe())
        return
    status = f"Ich schreibe nun von Version {git_object.describe()}"
    cl = get_changelog(database)
    if cl.strip() != "":
        status += ":\n" + cl
    if twitter.post(status):
        store_version(database)
