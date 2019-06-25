import datetime
import re

max_tweet_length = 280

def compose_answer(tweet, cursor, readwrite, modus):
    all_answers = []
    # generate answer
    charcount = 0
    generated_content = ""
    markers = [
        re.compile(r'#_?([A-Z_]+\d*)\b'),
        re.compile(r'#_?([a-z_]+\d*)\b'),
        re.compile(r'\b([A-Z_]+\d*)\b')
    ]
    marker_indices = []
    if modus == 'hashtag':
        marker_indices = [0, 1]
    elif modus == 'mention' or modus == 'quoted' or modus == 'referenced':
        marker_indices = [0, 1, 2]
    elif modus == 'timeline':
        marker_indices = [0]
    else:
        print("UNKNOWN MODUS", modus)
    short_list = []
    # get unique abbreviations, but keep them in order:
    for mi in marker_indices:
        for abbr in markers[mi].findall(tweet):
            abbr = abbr.replace('_', ' ')
            normalized = ' '.join(abbr.split())
            normalized = normalized.upper()
            if len(normalized) == 0:
                continue
            if len(normalized) > 5:
                continue
            if normalized == 'DS100':
                continue
            if normalized[0] == '_':
                continue
            if normalized[0].isdigit():
                continue
            if normalized in short_list:
                continue
            short_list.append(normalized)
    for abbr in short_list:
        cursor.execute("""
            SELECT
                Abk,
                Name,
                gueltigvon
            FROM
                shortstore
            WHERE
                Abk = ?
            ORDER BY gueltigvon DESC
            LIMIT 1
            """,
            (abbr, )
        )
        row = cursor.fetchone()
        if readwrite:
            cursor.execute("""
                INSERT INTO
                    requests(
                        ds100_id
                      , request_date
                      , status
                        )
                    VALUES (?,?,?)
                """,
                   (abbr
                  , datetime.datetime.today().strftime('%Y%m%d')
                  , row != None
                  , ))
        if row == None:
            continue
        explain = "{}: {}\n".format(row[0], row[1]).replace('.','\u2024').replace('\\n', '\n')
        if charcount + len(explain) > max_tweet_length:
            all_answers.append(generated_content.strip())
            generated_content = ""
            charcount = 0
        charcount += len(explain)
        generated_content += explain
    if len(generated_content.strip()) > 0:
        all_answers.append(generated_content.strip())
    return all_answers
