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

def store_since_id(sql, network):
    logger.info("storing highest msg id: %d",
            network.high_message)
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
         network.high_message,
         sql.network,
        )
        )
