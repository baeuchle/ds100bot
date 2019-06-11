def get_since_id(cursor):
    cursor.execute("""
        SELECT
            content
        FROM
            last
        WHERE
            subject = 'since_id'
        """)
    row = cursor.fetchone()
    if row == None:
        return 0
    try:
        return int(row[0])
    except:
        return 0

def store_since_id(cursor, highest_id):
    # store last answer time
    cursor.execute("""
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
