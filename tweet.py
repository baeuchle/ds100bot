# pylint: disable=C0114

import react
import log
log_ = log.getLogger(__name__)

class Tweet:
    def __init__(self, tweepy_tweet):
        self.id = tweepy_tweet.id
        self.text = tweepy_tweet.full_text
        self.original = tweepy_tweet
        if 'extended_entities' in tweepy_tweet.__dict__:
            ee = tweepy_tweet.extended_entities
            if 'media' in ee:
                alt_text = '\u200b'.join([m['ext_alt_text']
                                          for m in ee['media']
                                          if 'ext_alt_text' in m])
                self.text = '\u200b'.join([self.text, alt_text])

    def __str__(self):
        if log_.getEffectiveLevel() < 30:
            return self.text
        text = "id = {}\n".format(self.id)
        if self.original is not None:
            text += str(self.original)
        else:
            text += "text = {}\n".format(self.text)
        return text

    def hashtag_texts(self):
        return [ht['text'] for ht in self.original.entities['hashtags']]

    def author(self):
        return self.original.author

    def quoted_status_id(self):
        if 'quoted_status_id' in vars(self.original):
            return self.original.quoted_status_id
        return None

    def in_reply_id(self):
        return self.original.in_reply_to_status_id

    def is_retweet(self):
        """
        Checks if this tweet is a pure retweet. It is not clear if this doesn't
        maybe find commented retweets.
        """
        return 'retweeted_status' in self.original.raw and self.original.raw['retweeted_status']

    def is_mention(self, bot):
        """
        Checks if the bot is included in the user mentions of this tweet.
        """
        for um in self.original.entities['user_mentions']:
            if um['screen_name'] == bot.screen_name:
                return True
        return False

    def is_explicit_mention(self, bot):
        """
        Checks if this tweet explicitly mentions the given bot.  This means
        that there hasn't only been a reply to something the bot tweeted or
        somthing that itself has mentioned the bot.

        We distinguish these by the display_text_range: If the bot's mention is
        within the displayed text, then we assume that the original author
        meant to explicitly include the bot.

        If the bot is explicitl mentioned in a reply, then there are two
        user_mentions in the tweet's entities, so we cannot only look at
        the first one.
        """
        for um in self.original.entities['user_mentions']:
            if um['screen_name'] == bot.screen_name:
                this_is_an_xm = um['indices'][0] >= self.original.display_text_range[0]
                this_is_an_xm &= um['indices'][1] <= self.original.display_text_range[1]
                if this_is_an_xm:
                    return True
        return False

    def has_hashtag(self, tag_list, **kwargs):
        """
        Checks if one of the given hashtags is in the tweet.
        """
        lowlist = [tag.lower() for tag in tag_list]
        alllower = ('case_sensitive' in kwargs and not kwargs['case_sensitive'])
        for ht in self.original.entities['hashtags']:
            lowht = ht['text'].lower()
            if alllower and lowht in lowlist or '#' + lowht in lowlist:
                return True
            if ht['text'] in tag_list or '#' + ht['text'] in tag_list:
                return True
        return False

    def hashtags(self, candidate_list):
        """
        Returns a list of all the entries in candidate_list that are
        present as hashtag in the tweet.
        """
        return [[ht['text'], ht['indices']]
                for ht in self.original.entities['hashtags']
                if '#' + ht['text'] in candidate_list]

    def is_eligible(self, myself):
        """
        Returns false if this is a tweet from the bot itself
        or is a pure retweet
        """
        if self.author().screen_name == myself.screen_name:
            log_.debug("Not replying to my own tweets")
            return False
        if self.is_retweet():
            log_.debug("Not processing pure retweets")
            return False
        return True


    def get_mode(self, myself, magic):
        if self.is_explicit_mention(myself) or self.has_hashtag(magic):
            return 'all'
        return None

    def process_other_tweets(self, tweet_list, myself, magic, apis):
        for other_id in self.quoted_status_id(), self.in_reply_id():
            other_tweet = apis.twitter.get_other_tweet(other_id, tweet_list)
            if other_tweet is None:
                continue
            other_tweet.process_as_other(myself, magic, apis, self)

    def default_magic_hashtag(self, magic):
        dmt_list = [t[0] for t in self.hashtags(magic)]
        dmt = 'DS100'
        if len(dmt_list) > 0:
            dmt = dmt_list[0]
        return dmt

    def process_as_other(self, myself, magic, apis, orig_tweet):
        if not self.is_eligible(myself):
            return
        if self.is_mention(myself):
            log_.info("Not processing other tweet because it already mentions me")
            return
        if self.has_hashtag(magic):
            log_.info(
            "Not processing other tweet because it already has the magic hashtag")
            return
        mode = orig_tweet.get_mode(myself, magic)
        dmt = orig_tweet.default_magic_hashtag(magic)
        log_.debug("Processing tweet %d mode '%s' default magic hash tag %s", self.id, mode, dmt)
        react.process_tweet(self, apis, magic, modus=mode, default_magic_tag=dmt)
