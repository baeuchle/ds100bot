# pylint: disable=C0114

import regex as re
import Persistence.log as log
from .candidate import Candidate
from .result import Result
log_ = log.getLogger(__name__)
follog_ = log.getLogger(__name__ + '.following', '{name} {message}')

def process_tweet(tweet, twitter, database, magic_tags, **kwargs):
    textlist = list(tweet.text)
    for key in ['media', 'urls']:
        if key in tweet.original.entities:
            for ent in tweet.original.entities[key]:
                start = ent['indices'][0]
                end = ent['indices'][1]
                length = end - start
                textlist[start:end] = '_'*length
    tweet.text = "".join(textlist)
    reply = compose_answer(tweet.text,
                           database,
                           tweet.hashtags(magic_tags),
                           kwargs.get('modus', None),
                           kwargs.get('default_magic_tag', 'DS100')
                          )
    if len(reply.strip()) == 0:
        log_.info("No expandable content found")
        return
    twitter.tweet(reply,
        in_reply_to_status_id=tweet.id,
        auto_populate_reply_metadata=True
    )

def process_commands(tweet, twapi):
    author = tweet.author()
    if tweet.has_hashtag(['folgenbitte'], case_sensitive=False):
        is_followed = twapi.is_followed(author)
        if is_followed:
            follog_.log(45, "folgenbitte from @%s: already following", author.screen_name)
        else:
            follog_.log(45, "folgenbitte from @%s: not yet following", author.screen_name)
        if not is_followed:
            twapi.follow(author)
    if tweet.has_hashtag(['entfolgen'], case_sensitive=False):
        is_followed = twapi.is_followed(author)
        if is_followed:
            follog_.log(45, "entfolgen from @%s: still following so far", author.screen_name)
        else:
            follog_.log(45, "entfolgen from @%s: not even following yet", author.screen_name)
        if is_followed:
            twapi.defollow(author)

def find_tokens(tweet, modus, magic_tag):
    finder = re.compile(r"""
        (?p)                # find longest match
        (?:^|\W)            # either at the beginning of the text or after a non-alphanumeric character, but don't find this
        (?:                 # Select source
            (\$|\#|\%|\&amp;|\/)# Special character to find something: #,$,%,&,/
            (?:(\p{Lu}+):)? # Optional prefix, e.g. "DS:" or "FFM:"
        )
        (                   # Payload
            [\p{L}\p{N}_]+  # All  letters plus all kinds of numbers plus _
        )
        (?:$|\W)            # either end of string or non-\w character
        """, re.X)
    tokens = finder.findall(tweet, overlapped=True)
    candidates = [Candidate(t, magic_tag) for t in tokens]
    # if modus isn't 'all', then that's all already.
    # if modus *is* 'all', and we have more than one result: great, too!
    if modus != 'all' or len(tokens) > 1:
        return candidates
    # if modus is 'all' and we have only one token and it's not the magic_tag, fine!
    if len(tokens) == 1 and str.join('', tokens[0][-1]) != magic_tag:
        return candidates
    # now: If modus is all and we have at found nothing but maybe the magic_tag,
    # we'll look for more. This can only be uppercase.
    finder2 = re.compile(r"""
        (?p)            # find longest match
        (?:^|\W)        # either at the beginning of the text or after a non-alphanumeric character, but don't find this
        ()
        ()
        (
            \p{Lu}[\p{Lu}\p{N}_]*)
                        # All uppercase letters plus all kinds of numbers plus _
        (?:$|\W)        # either end of string or non-\w character
        """, re.X)
    tokens = finder2.findall(tweet, overlapped=True)
    return [Candidate(t, magic_tag) for t in tokens]

def process_magic(magic_tags, length, default='DS100'):
    """
        Edits the list of magic hashtags so that
            - first mht or default mht starts at beginning
            - __ is appended at end.
        Returns the edited list.
    """
    if len(magic_tags) == 0:
        # no magic tag: Only magic is in DS100.
        magic_tags = [[default, [0, 0]]]
    else:
        # the first magic tag is valid from the beginning, no matter
        # where it is!
        magic_tags[0][1] = [0, 0]
    magic_tags.append(['__', [length, length]])
    return magic_tags

def compose_answer(tweet, sql, magic_tags, modus, default_magic_tag='DS100'):
    short_list = []
    # generate answer
    generated_content = ""
    magic_tags = process_magic(magic_tags, len(tweet), default_magic_tag)
    for mt, nextmt in zip(magic_tags[:-1], magic_tags[1:]):
        tweetpart = tweet[mt[1][1]:nextmt[1][0]]
        tag = mt[0]
        log_.debug("Part: '%s' mt '%s'", tweetpart, tag)
        for match in find_tokens(tweetpart, modus, tag):
            result = Result(match, sql)
            norm = result.normalized()
            if norm and norm in short_list:
                continue
            if norm:
                short_list.append(norm)
            if result.loggable(magic_tags):
                sql.log_request(result)
            if result.status != 'found':
                continue
            generated_content += result.answered()
    return generated_content
