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
            subject IN ('since_id', 'since_notification')
            AND
            network = ?
        """, (sql.network, ))
    result = dict(sql.cursor.fetchall())
    logger.debug("found highest ids for %s: %s", sql.network, result)
    return result

def store_since_id(sql, network):
    id_list = {'since_id': network.high_message}
    try:
        id_list['since_notification'] = network.high_notification
    except AttributeError:
        pass
    logger.info("storing highest msg id for %s: %s", sql.network, id_list)
    # store last answer time
    for name, high in id_list.items():
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
             high,
             name,
             sql.network,
            )
            )
