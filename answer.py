import datetime
import re

max_tweet_length = 280

def compose_answer(tweet, cursor, readwrite):
    all_answers = []
    # generate answer
    charcount = 0
    generated_content = ""
    marker = re.compile("#_([A-Z_]+)")
    short_list = []
    # get unique abbreviations, but keep them in order:
    for abbr in marker.findall(tweet):
        normalized = ' '.join(abbr.replace('_', ' ').split())
        if normalized not in short_list:
            short_list.append(normalized)
    for abbr in short_list:
        cursor.execute('SELECT Abk, Name FROM ds100 WHERE Abk = ?',
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
        explain = "{}: {}\n".format(row[0], row[1])
        if charcount + len(explain) > max_tweet_length:
            all_answers.append(generated_content.strip())
            generated_content = ""
            charcount = 0
        charcount += len(explain)
        generated_content += explain
    if len(generated_content.strip()) > 0:
        all_answers.append(generated_content.strip())
    return all_answers
