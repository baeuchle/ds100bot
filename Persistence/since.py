"""
    Functions for reading and storing highest ids
"""

import logging

logger = logging.getLogger('bot.persistence')

def get_since_id(sql):
    sql.cursor.execute("""
        SELECT
            content
        FROM
            last
        WHERE
            subject = 'since_id'
        """)
    row = sql.cursor.fetchone()
    if row is None:
        return 0
    try:
        return int(row[0])
    except ValueError:
        return 0

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
        """,
        (
         highest_id,
        )
        )
