#!/usr/bin/python3

from Externals import get_database_object

db = get_database_object('readwrite')
db.cursor.execute("DELETE FROM requestlog")
db.cursor.execute("UPDATE sqlite_sequence SET seq = 0 WHERE name = 'requestlog'")
db.cursor.execute("""
    SELECT
        ds100_id,
        request_date,
        status
    FROM
        requests
    """)
rows = []

# not sure if this changes anything, but let's collect all data from the
# cursor befor starting new queries inside the loop body.
for row in db.cursor.fetchall():
    rows.append(row)

for row in rows:
    payload = row[0]
    date = row[1]
    status = row[2]
    if payload == '':
        continue
    # newer data look like 'DS::FF':
    parts = payload.split('::')
    if len(parts) == 1:
        # older data may look like '#DS:FF' or even 'FF':
        parts = payload.split(':')
    tc = '_'
    if len(parts[0]) > 0 and parts[0][0] in ('#', '%', '/', '&', '$'):
        tc = parts[0][0]
        parts[0] = ''.join(list(parts[0])[1:])
    if len(parts) == 1:
        parts = ['', parts[0]]
    translate = {
        'VGF': 'FFM',
        'NOR': 'NO',
        'DS100': 'DS',
        'HHA': 'HH',
        'AT': 'ÖBB',
        'DE': 'DS'
    }
    xsource = translate.get(parts[0], parts[0])
    abbr = parts[1]
    derived_source = xsource
    active_magic = 'DS100'
    # two lines here that I don't know where they come from.
    if xsource == 'None':
        continue
    # Now look for matches and possibly correct tc and set
    # derived_source
    if status != 'notfound':
        db.cursor.execute('''
            SELECT
                type
              , explicit_source
              , magic_hashtag
            FROM
                shortstore
            JOIN
                sources ON source = sources.source_id
            JOIN
                magic_hashtags ON magic_hashtags.source_id = sources.source_id
            WHERE
                Abk = :abk
            AND
                (:type = '_' OR type = :type)
            AND
                is_default
            ORDER BY magic_hashtag ASC
        ''', {
          'abk': abbr,
          'type': tc,
          'xs': xsource
        })
        sources = db.cursor.fetchone()
        if sources is None:
            derived_source = xsource
        else:
            tc = sources['type']
            derived_source = sources['explicit_source']
            # if the source is different from the one we thought it would be,
            # this must be because of the magic hashtag.
            if derived_source != xsource:
                active_magic = sources['magic_hashtag']
    db.cursor.execute('''
        INSERT INTO requestlog (
            explicit_source
          , active_magic
          , type
          , abbreviation
          , request_date
          , derived_source
          , status
        ) VALUES (
            :xs
          , :active
          , :type
          , :abbr
          , :date
          , :ds
          , :status
        )
    ''', {
        'xs': xsource
      , 'type': tc
      , 'active': active_magic
      , 'abbr': abbr
      , 'date': row[1]
      , 'ds': derived_source
      , 'status': row[2]
    })

db.close_sucessfully()
