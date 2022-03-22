# pylint: disable=C0114

import logging
import re
from Externals.user import User
log_ = logging.getLogger('bot.' + __name__)

class Tweet:
    # pylint: disable=too-many-instance-attributes
    hashtagre = None

    def __init__(self, **kwargs):
        self.orig = kwargs.get('orig', {})
        self.id = kwargs['id']
        self.text = kwargs['text']
        self.hashtag_texts = kwargs.get('hashtag_texts', [])
        self.author = kwargs['author']
        self.quoted_status_id = kwargs.get('quoted_status_id', None)
        self.in_reply_to_status_id = kwargs.get('in_reply_to_status_id', None)
        self.is_retweet = kwargs.get('is_retweet', False)
        self.is_mention = kwargs.get('is_mention', False)
        self.is_explicit_mention = kwargs.get('is_explicit_mention', self.is_mention)

    def has_hashtag(self, tag_list, **kwargs):
        """
        Checks if one of the given hashtags is in the tweet.
        """
        lowlist = [tag.lower() for tag in tag_list]
        alllower = not kwargs.get('case_sensitive', True)
        for ht in self.hashtag_texts:
            lowht = ht.lower()
            if alllower and lowht in lowlist or '#' + lowht in lowlist:
                return True
            if ht in tag_list or '#' + ht in tag_list:
                return True
        return False

    def hashtags(self, candidate_list):
        """
        Returns a list of all the entries in candidate_list that are
        present in the tweet.
        """
        if Tweet.hashtagre is None:
            Tweet.hashtagre = re.compile('|'.join(map(re.escape, candidate_list)))
        return [
            [m.group(0).replace('#', '', 1), m.span()]
            for m in Tweet.hashtagre.finditer(self.text)
        ]

    def is_eligible(self, myself):
        """
        Returns false if this is a tweet from the bot itself
        or is a pure retweet
        """
        if self.author == myself:
            log_.debug("Not replying to my own tweets")
            return False
        if self.is_retweet:
            log_.debug("Not processing pure retweets")
            return False
        return True

    def get_mode(self, magic, emojis):
        if self.is_explicit_mention:
            log_.debug("Status %s is explicit mention", str(self.id))
            return 'all'
        if self.has_hashtag(magic):
            log_.debug("Status %s has magic hashtag", str(self.id))
            return 'all'
        if self.has_hashtag(emojis):
            log_.debug("Status %s has magic emojis", str(self.id))
            return 'all'
        log_.debug("Status %s has neither", str(self.id))
        return None

    def get_other_tweets(self, tweet_list, mode, network, **kwargs):
        result = []
        if mode != 'all':
            return result
        for other_id in self.in_reply_to_status_id, self.quoted_status_id:
            if not other_id:
                continue
            other_msg = network.get_other_tweet(other_id, tweet_list)
            if not other_msg:
                continue
            if other_msg.can_process_as_other(**kwargs):
                result.append(other_msg)
        return result

    def default_magic_hashtag(self, magic):
        dmt_list = [t[0] for t in self.hashtags(magic)]
        dmt = 'DS100'
        if len(dmt_list) > 0:
            dmt = dmt_list[0]
        return dmt

    def can_process_as_other(self, **kwargs):
        if not self.is_eligible(kwargs['myself']):
            return False
        if self.is_mention:
            log_.info("Not processing other tweet because it already mentions me")
            return False
        if self.has_hashtag(kwargs['magic_tags']):
            log_.info("Not processing other tweet because it already has the magic hashtag")
            return False
        if self.has_hashtag(kwargs['magic_emojis']):
            log_.info("Not processing other tweet because it already has the magic emojis")
            return False
        return True

def fromTweet(tweet, myself):
    """Construct a Message object from a tweet"""
    texts = [tweet.full_text]
    quoted_id = tweet.__dict__.get('quoted_status_id', None)
    for medium in tweet.__dict__.get('extended_entities', {}).get('media', ''):
        alt_text = medium.get('ext_alt_text', None)
        if not alt_text:
            continue
        texts.append(alt_text)
    textlist = list('\u200b'.join(texts))
    for key in ['media', 'urls']:
        for ent in tweet.entities.get(key, []):
            start = ent['indices'][0]
            end = ent['indices'][1]
            length = end - start
            textlist[start:end] = '_'*length
    text = "".join(textlist)
    m = Tweet(
        orig=tweet,
        id=tweet.id,
        text=text,
        hashtag_texts=[ht['text'] for ht in
                                tweet.entities['hashtags']],
        author=User(tweet.author.screen_name, tweet.author.id),
        quoted_status_id=quoted_id,
        in_reply_to_status_id=tweet.in_reply_to_status_id,
        is_retweet=tweet.__dict__.get('retweeted_status', False),
        is_mention=any(um['screen_name'] == myself for um in
                                tweet.entities['user_mentions']),
        is_explicit_mention=any(
            um['screen_name'] == str(myself)
            and
            um['indices'][0] >= tweet.display_text_range[0]
            and
            um['indices'][1] <= tweet.display_text_range[1]
            for um in tweet.entities['user_mentions']
        )
    )
    return m
