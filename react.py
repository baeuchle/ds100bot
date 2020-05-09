import datetime
import regex as re
import sqlite3

max_tweet_length = 280

def process_tweet(tweet, twapi, sql, verbose, magic_tags, modus=None, default_magic_tag='DS100'):
    reply_id = tweet.id
    twcounter = 1
    for reply in compose_answer(tweet.text, sql, verbose, tweet.hashtags(magic_tags), modus, default_magic_tag):
        if verbose > 1:
            print("I tweet {} ({} chars):".format(twcounter, len(reply)))
            print(reply)
        twcounter += 1
        new_reply_id = twapi.tweet(reply,
                in_reply_to_status_id=reply_id,
                auto_populate_reply_metadata=True
            )
        if new_reply_id > 0:
            reply_id = new_reply_id
    if verbose > 2:
        if twcounter == 1:
            print("No expandable content found")
        print("▀"*60)

def process_commands(tweet, twapi, verbose):
    author = tweet.author()
    if tweet.has_hashtag(['folgenbitte'], case_sensitive=False):
        is_followed = twapi.is_followed(author)
        if verbose > 0:
            print ("folgenbitte from @{}:".format(author.screen_name), end='')
            if is_followed:
                print (" already following")
            else:
                print (" not yet following")
        if not is_followed:
            twapi.follow(author)
    if tweet.has_hashtag(['entfolgen'], case_sensitive=False):
        is_followed = twapi.is_followed(author)
        if verbose > 0:
            print ("entfolgen from @{}:".format(author.screen_name), end='')
            if is_followed:
                print(" still following so far")
            else:
                print(" not even following yet")
        if is_followed:
            twapi.defollow(author)

def find_tokens(tweet, modus, magic_tag):
    finder = re.compile(r"""
                            # this RE finds
                            # #AB:CD
                            # #AB
                            # #1234
                            # #AB_12_CD
                            # $AB:CD
                            # $AB
                            # $AB_12_CD
                            # $1234
        (?p)                # find longest match
        (?:^|\W)            # either at the beginning of the text or after a non-alphanumeric character, but don't find this
        (?:                 # Select source
            (\$|\#)         # Special character to find something: # or $
            (?:(\p{Lu}+):)? # Optional prefix, e.g. "DS:" or "VGF:"
        )
        (                   # Payload
            [\p{Lu}\p{N}_]+ # All uppercase letters plus all kinds of numbers plus _
        )
        (?:$|\W)            # either end of string or non-\w character
        """, re.X)
    tokens = finder.findall(tweet, overlapped=True)
    # if modus isn't 'all', then that's all already.
    # if modus *is* 'all', and we have more than one result: great, too!
    if modus != 'all' or len(tokens) > 1:
        return tokens
    # if modus is 'all' and we have only one token and it's not the magic_tag, fine!
    if len(tokens) == 1 and str.join('', tokens[0][0]) != magic_tag:
        return tokens
    # now: If modus is all and we have at found nothing but maybe the magic_tag,
    # we'll look for more.
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
    return finder2.findall(tweet, overlapped=True)

def find_entry(sql, parameters):
    sql.cursor.execute("""
        SELECT
            shortstore.Abk AS abk,
            shortstore.Name AS name,
            sourceflags.abbr AS source,
            sourceflags.sigil AS sigil,
            CASE
                WHEN (
                    blacklist.Abk IS NOT NULL
                    AND
                    sourceflags.magictag <> :abbr2
                ) THEN 'blacklist'
                ELSE 'found'
            END
            AS status
        FROM
            shortstore
        JOIN
            sourceflags
        ON
            sourceflags.sourcename = shortstore.source
        LEFT OUTER JOIN
            blacklist
        ON
            (blacklist.Abk = shortstore.Abk AND blacklist.source = shortstore.source)
        WHERE
            shortstore.Abk = :abk
        AND
            gueltigvon < strftime('%Y%m%d', 'now')
        AND
            sourceflags.sigil = :sigil
        AND
            (sourceflags.magictag = :magic_tag OR sourceflags.abbr = :abbr2)
        ORDER BY gueltigvon DESC
        LIMIT 1
        """,
        parameters
    )
    row = sql.cursor.fetchone()
    normalized = "{}{}:{}".format(parameters['sigil'], parameters['abbr1'], parameters['abk'])
    if row is None:
        row = sqlite3.Row(sql.cursor, (
            parameters['abk'],
            '',
            parameters['abbr1'],
            parameters['sigil'],
            'notfound'
        ))
    return row, normalized

def find_source(sql, tag):
    sql.cursor.execute("""
        SELECT
            abbr
        FROM
            sourceflags
        WHERE
            magictag = :magic
        LIMIT 1
        """,
        ({'magic': tag,})
    )
    row = sql.cursor.fetchone()
    if row is None:
        return tag
    return row['abbr']

def process_magic(magic_tags, length, default='DS100'):
    if len(magic_tags) == 0:
        # no magic tag: Only magic is in DS100.
        magic_tags = [[default, [0, 0]]]
    else:
        # the first magic tag is valid from the beginning, no matter
        # where it is!
        magic_tags[0][1] = [0, 0]
    magic_tags.append(['__', [length, length]])
    return magic_tags

def compose_answer(tweet, sql, verbose, magic_tags, modus, default_magic_tag='DS100'):
    all_answers = []
    short_list = []
    # generate answer
    charcount = 0
    generated_content = ""
    magic_tags = process_magic(magic_tags, len(tweet), default_magic_tag)
    for mt, nextmt in zip(magic_tags[:-1], magic_tags[1:]):
      tweetpart = tweet[mt[1][1]:nextmt[1][0]]
      tag = mt[0]
      tagsource = find_source(sql, tag)
      if verbose > 4:
        print("Part: '{}' mt '{}'".format(tweetpart, tag))
      for match in find_tokens(tweetpart, modus, tag):
        sigil = match[0] if not match[0] == "" else '#'
        source = match[1]
        payload = match[2]
        payload = payload.replace('_', ' ')
        payload = ' '.join(payload.split())
        payload = payload.upper()
        parameters = { 'abk': payload,
            'sigil': sigil,
            'magic_tag': source if source != "" else tag,
            'abbr1': source if source != "" else tagsource,
            'abbr2': source if source != "" else 'BOT',
        }
        row, normalized = find_entry(sql, parameters)
        if verbose > 2:
            print ("{}: {}→{}".format(normalized,
            list(parameters.values()), list(row)))
        if normalized in short_list:
            continue
        short_list.append(normalized)
        # failures are always written if the source is not empty, and...
        if row['status'] == 'notfound' and source == "":
            if len(payload) == 0:
                continue
            if len(payload) > 5:
                continue
            if '#' + payload in magic_tags:
                continue
            if payload[0] == '_':
                continue
            if sigil == '#' and payload[0].isdigit():
                continue
        if not sql.readonly:
            sql.cursor.execute("""
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
                  , row['status']
                  , ))
        if row['status'] != 'found':
            continue
        explain = "{}: {}\n".format(
            row['abk'],
            row['name']
        )
        if not (row['source'] == 'DS' or row['source'] == 'BOT'):
            explain = "{}{}{}".format(
                row['source'],
                row['sigil'],
                explain
            )
        explain = explain.replace('\\n', '\n')
        if charcount + len(explain) > max_tweet_length:
            all_answers.append(generated_content.strip())
            generated_content = ""
            charcount = 0
        charcount += len(explain)
        generated_content += explain
    if len(generated_content.strip()) > 0:
        all_answers.append(generated_content.strip())
    return all_answers
