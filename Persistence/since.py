"""
    Functions for reading and storing highest ids
"""

import logging

logger = logging.getLogger('bot.persistence')

def get_since_id(sql):
    sql.cursor.execute("""
        SELECT
            subject,
            content
        FROM
            last
        WHERE
            subject = 'since_id'
            AND
            network = ?
        """, (sql.network, ))
    result = dict(sql.cursor.fetchall())
    logger.debug("found highest ids for %s: %s", sql.network, result)
    return result.get('since_id', 0)

def store_since_id(sql, highest_id):
    logger.info("storing highest id: %d",
            highest_id)
    # store last answer time
    sql.cursor.execute("""
        UPDATE
            last
        SET
            content = ?
        WHERE
            subject = 'since_id'
            AND
            network = ?
        """,
        (
         highest_id,
         sql.network,
        )
        )
