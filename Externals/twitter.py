"""Twitter API including Command line argumentation"""

import logging
import time
from urllib.parse import quote_plus
import tweepy

from Externals.Measure import MeasureTweet
from .message import fromTweet
from .network import Network
from .user import fromTwitterUser

logger = logging.getLogger('bot.api.twitter')
msg_log = logging.getLogger('msg')

class Twitter(Network):
    def __init__(self, api, readwrite, highest_ids):
        self.api = api
        try:
            me = self.api.me()
        except tweepy.error.TweepError as te:
            raise RuntimeError(str(te)) from te
        myself = fromTwitterUser(me)
        super().__init__(readwrite, highest_ids, MeasureTweet(), fromTweet, myself)

    def post_single(self, text, **kwargs):
        """Actually posts text as a new tweet.

        kwargs are passed to tweepy directly.

        If api_code is 185 (status update limit), then the program pauses 1 minute and tries again
        (this will be repeated indefinitely) An error message will be logged each time.

        If api_code is neither 185 nor 187 (duplicate tweet), a critical log message will be logged.
        """
        if len(text) == 0:
            logger.error("Empty tweet?")
            return None
        msg_log.warning(text)
        if self.readonly:
            return None
        if 'reply_to_status' in kwargs:
            orig_tweet = kwargs.pop('reply_to_status')
            if orig_tweet:
                kwargs['in_reply_to_status_id'] = orig_tweet.id
        kwargs['auto_populate_reply_metadata'] = True
        while True: # catches rate limit
            try:
                new_tweet = self.api.update_status(text, **kwargs)
                return new_tweet
            except tweepy.TweepError as twerror:
                if twerror.api_code is None:
                    logger.critical("Unknown error while tweeting: %s", twerror.reason)
                    return None
                if twerror.api_code == 185: # status update limit (tweeted too much)
                    logger.error("Tweeted too much, waiting 1 Minute before trying again")
                    time.sleep(60)
                    continue
                if twerror.api_code == 385:
                    logger.critical("Error 385: Tried to reply to deleted or invisible tweet %s",
                        kwargs.get('in_reply_to_status_id', 'N/A'))
                elif twerror.api_code != 187: # duplicate tweet
                    logger.critical("Error %s tweeting: %s", twerror.api_code, twerror.reason)
                return None

    def follow(self, user):
        logger.warning("Follow @%s", str(user))
        if self.readonly:
            return
        try:
            self.api.create_friendship(id=int(user))
        except tweepy.RateLimitError as rateerror:
            self.warn_rate_error(rateerror, "follow @{:s}".format(user))

    def defollow(self, user):
        logger.warning("Defollow @%s", str(user))
        if self.readonly:
            return
        try:
            self.api.destroy_friendship(id=user.id)
        except tweepy.RateLimitError as rateerror:
            self.warn_rate_error(rateerror, "defollow @{:s}".format(user))

    def warn_rate_error(self, rate_err, description):
        logger.critical("Rate limit violated at %s: %s", description, rate_err.reason)
        self.print_rate_limit()

    def print_rate_limit(self):
        rls = self.api.rate_limit_status()
        res = rls['resources']
        for r in res:
            for l in res[r]:
                rrl = res[r][l]
                if rrl['limit'] == rrl['remaining']:
                    continue
                if rrl['remaining'] == 0:
                    logger.critical("Resource limit for %s used up: limit %s",
                        l,
                        rrl['limit']
                    )
                elif rrl['remaining'] < 5:
                    logger.warning("Resource limit for %s low: %s of %s remaining",
                        l,
                        rrl['remaining'],
                        rrl['limit']
                    )
                elif rrl['remaining'] < rrl['limit']:
                    logger.info("Resource limit for %s in use: %s of %s",
                        l,
                        rrl['remaining'],
                        rrl['limit']
                    )

    def mentions(self):
        result = self.cursor(self.api.mentions_timeline, since_id=self.high_message)
        logger.debug("found %d mentions", len(result))
        return result

    def timeline(self):
        result = self.cursor(self.api.home_timeline, since_id=self.high_message)
        logger.debug("found %d status in timeline", len(result))
        return result

    def _get_tag_query(self, mt_list):
        tagquery = "(" + " OR ".join(mt_list) + ")"
        if len(quote_plus(tagquery)) > 500 and len(mt_list) > 1:
            logger.debug("tagquery %s too long, partioning...", tagquery)
            return [*self._get_tag_query(mt_list[::2]), *self._get_tag_query(mt_list[1::2])]
        logger.debug("tagquery %s short enough; we can use it.", tagquery)
        return [tagquery]

    def hashtags(self, mt_list):
        result = []
        for tagquery in self._get_tag_query(mt_list):
            for ht in self.cursor(self.api.search, q=tagquery, since_id=self.high_message):
                result.append(self.get_status(ht.id))
            logger.debug("found %d status in hashtags", len(result))
        return result

    def cursor(self, task, **kwargs):
        kwargs['tweet_mode'] = 'extended'
        kwargs['include_ext_alt_text'] = True
        try:
            result = []
            for t in tweepy.Cursor(task, **kwargs).items():
                result.append(t)
            return result
        except tweepy.TweepError as twerror:
            try:
                if twerror.response.status_code == 429:
                    self.warn_rate_error(twerror, "cursoring")
                    return []
            finally:
                pass
            logger.critical("Error %s reading tweets: %s", twerror.api_code, twerror.reason)
        return []

    def get_status(self, status_id):
        try:
            return self.api.get_status(
                status_id,
                tweet_mode='extended',
                include_ext_alt_text=True
            )
        except tweepy.TweepError as twerror:
            try:
                if twerror.response.status_code == 429:
                    self.warn_rate_error(twerror, "cursoring")
                    return None
            finally:
                pass
            if twerror.api_code == 136: # user has blocked the bot: chill out.
                logger.debug("%s's Author has blocked us from reading their tweets.", status_id)
                return None
            logger.critical("Error %s reading tweet %s: %s",
                          twerror.api_code,
                          status_id,
                          twerror.reason)
        return None

    def is_followed(self, user):
        try:
            return self.api.show_friendship(
                int(self.myself),
                target_id=int(user)
            )[0].following
        except tweepy.RateLimitError as rateerror:
            self.warn_rate_error(rateerror, "is_followed @{}".format(user.screen_name))
            return False

def make_twapi(args, highest_ids):
    auth = tweepy.OAuthHandler(
        args.config[args.application]['key'],
        args.config[args.application]['secret']
    )
    auth.set_access_token(
        args.config[args.user]['token'],
        args.config[args.user]['secret']
    )
    try:
        api = tweepy.API(auth)
    except tweepy.error.TweepError as te:
        raise RuntimeError(str(te)) from te
    logger.info("Created twitter API instance for @%s", api.me().screen_name)
    return Twitter(api, args.readwrite, highest_ids)
