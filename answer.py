import datetime
import regex as re

max_tweet_length = 280

def compose_answer(tweet, cursor, readwrite, verbose, modus):
    all_answers = []
    short_list = []
    # generate answer
    charcount = 0
    generated_content = ""
    finder = re.compile(r"""
        (?p)                # find longest match
        (?:^|\W)            # either at the beginning of the text or after a non-alphanumeric character, but don't find this
        (?:                 # Select source
            (\$|\#)         # Special character to find something: # or $
            (?:(\p{Lu}+):)? # Optional prefix, e.g. "DS:" or "VGF:"
        )
        (                   # Payload
            [\p{Lu}\p{N}_]+ # All uppercase letters plus all kinds of numbers plus _
          | [\p{Ll}_]+\d*   # All lowercase letters plus trailing normal digits
          | \d+             # All numbers
        )
        (?:$|\W)            # either end of string or non-\w character
        """, re.X)
    tokens = finder.findall(tweet, overlapped=True)
    if len(tokens) == 0 and modus == 'all':
        finder2 = re.compile(r"""
            (?p)            # find longest match
            (?:^|\W)        # either at the beginning of the text or after a non-alphanumeric character, but don't find this
            ()
            ()
            (
                [\p{Lu}\p{N}_]+)
                            # All uppercase letters plus all kinds of numbers plus _
            (?:$|\W)        # either end of string or non-\w character
            """, re.X)
        tokens = finder2.findall(tweet, overlapped=True)
    for match in tokens:
        sigil = match[0] if not match[0] == "" else '#'
        source = match[1]
        payload = match[2]
        payload = payload.replace('_', ' ')
        payload = ' '.join(payload.split())
        payload = payload.upper()
        parameters = (payload, sigil, source if source != "" else 'DS', source if source != "" else 'BOT', )
        cursor.execute("""
            SELECT
                Abk,
                Name
            FROM
                shortstore
            JOIN
                sourceflags
            ON
                sourceflags.sourcename = shortstore.source
            WHERE
                Abk = ?
            AND
                gueltigvon < strftime('%Y%m%d', 'now')
            AND
                sourceflags.sigil = ?
            AND
                (sourceflags.abbr = ? OR sourceflags.abbr = ?)
            ORDER BY gueltigvon DESC
            LIMIT 1
            """,
            parameters
        )
        row = cursor.fetchone()
        normalized = '{}{}:{}'.format(sigil, source, payload)
        if verbose > 2:
            print ("{}: {}→{}".format(normalized, parameters, row))
        if normalized in short_list:
            continue
        short_list.append(normalized)
        if readwrite:
            # failures are always written if the source is not empty, and...
            if row == None and source == "":
                if len(payload) == 0:
                    continue
                if len(payload) > 5:
                    continue
                if payload == 'DS100':
                    continue
                if payload[0] == '_':
                    continue
                if sigil == '#' and payload[0].isdigit():
                    continue
            cursor.execute("""
                INSERT INTO
                    requests(
                        ds100_id
                      , request_date
                      , status
                        )
                    VALUES (?,?,?)
                """,
                   (normalized
                  , datetime.datetime.today().strftime('%Y%m%d')
                  , row != None
                  , ))
        if row == None:
            continue
        explain = "{}: {}\n".format(row[0], row[1]).replace('\\n', '\n')
        if charcount + len(explain) > max_tweet_length:
            all_answers.append(generated_content.strip())
            generated_content = ""
            charcount = 0
        charcount += len(explain)
        generated_content += explain
    if len(generated_content.strip()) > 0:
        all_answers.append(generated_content.strip())
    return all_answers
