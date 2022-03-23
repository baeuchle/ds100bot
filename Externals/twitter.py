"""Twitter API including Command line argumentation"""

import configparser
import logging
import time
import tweepy

from Externals.Measure import Measure
from Externals.message import fromTweet
log_ = logging.getLogger('bot.api.twitter')
tweet_log_ = logging.getLogger('msg')

def set_arguments(ap):
    group = ap.add_argument_group('Twitter API', description='Configure Twitter API')
    group.add_argument('--config',
                        action='store',
                        help='path to configuration file',
                        required=True)
    group.add_argument('--application',
                        action='store',
                        help='Name of the twitter application',
                        required=True)
    group.add_argument('--user',
                        action='store',
                        help='Name of the user',
                        required=True
                        )
    group.add_argument('--readwrite',
                        action='store_true',
                        help="Don't post, only read status.",
                        required=False)

class Twitter:
    def __init__(self, api, readwrite, highest_ids):
        self.twit = api
        try:
            self.myself = self.twit.me()
        except tweepy.error.TweepError as te:
            raise RuntimeError(str(te)) from te
        self.measure = Measure()
        self.readonly = not readwrite
        self.high_message = highest_ids

    def post_single(self, text, **kwargs):
        """Actually posts text as a new tweet.

        kwargs are passed to tweepy directly.

        If api_code is 185 (status update limit), then the program pauses 1 minute and tries again
        (this will be repeated indefinitely) An error message will be logged each time.

        If api_code is neither 185 nor 187 (duplicate tweet), a critical log message will be logged.
        """
        if len(text) == 0:
            log_.error("Empty tweet?")
            return None
        if tweet_log_.isEnabledFor(logging.WARNING):
            lines = text.splitlines()
            length = max([len(l) for l in lines])
            tt = "▄{}┓\n".format('━'*(length+2))
            for l in lines:
                tt += ("█ {{:{}}} ┃\n".format(length)).format(l)
            tt += "▀{}┛".format('━'*(length+2))
            tweet_log_.warning(tt)
        if self.readonly:
            return None
        if 'reply_to_status' in kwargs:
            orig_tweet = kwargs.pop('reply_to_status')
            if orig_tweet:
                kwargs['in_reply_to_status_id'] = orig_tweet.id
        kwargs['auto_populate_reply_metadata'] = True
        while True: # catches rate limit
            try:
                new_tweet = self.twit.update_status(text, **kwargs)
                return new_tweet
            except tweepy.TweepError as twerror:
                if twerror.api_code is None:
                    log_.critical("Unknown error while tweeting: %s", twerror.reason)
                    return None
                if twerror.api_code == 185: # status update limit (tweeted too much)
                    log_.error("Tweeted too much, waiting 1 Minute before trying again")
                    time.sleep(60)
                    continue
                if twerror.api_code == 385:
                    log_.critical("Error 385: Tried to reply to deleted or invisible tweet %s",
                        kwargs.get('in_reply_to_status_id', 'N/A'))
                elif twerror.api_code != 187: # duplicate tweet
                    log_.critical("Error %s tweeting: %s", twerror.api_code, twerror.reason)
                return None

    def follow(self, user):
        log_.warning("Follow @%s", user.screen_name)
        if self.readonly:
            return
        try:
            self.twit.create_friendship(id=user.id)
        except tweepy.RateLimitError as rateerror:
            self.warn_rate_error(rateerror, "follow @{}".format(user.screen_name))

    def defollow(self, user):
        log_.warning("Defollow @%s", user.screen_name)
        if self.readonly:
            return
        try:
            self.twit.destroy_friendship(id=user.id)
        except tweepy.RateLimitError as rateerror:
            self.warn_rate_error(rateerror, "defollow @{}".format(user.screen_name))

    def warn_rate_error(self, rate_err, description):
        log_.critical("Rate limit violated at %s: %s", description, rate_err.reason)
        self.print_rate_limit()

    def print_rate_limit(self):
        rls = self.twit.rate_limit_status()
        res = rls['resources']
        for r in res:
            for l in res[r]:
                rrl = res[r][l]
                if rrl['limit'] == rrl['remaining']:
                    continue
                if rrl['remaining'] == 0:
                    log_.critical("Resource limit for %s used up: limit %s",
                        l,
                        rrl['limit']
                    )
                elif rrl['remaining'] < 5:
                    log_.warning("Resource limit for %s low: %s of %s remaining",
                        l,
                        rrl['remaining'],
                        rrl['limit']
                    )
                elif rrl['remaining'] < rrl['limit']:
                    log_.info("Resource limit for %s in use: %s of %s",
                        l,
                        rrl['remaining'],
                        rrl['limit']
                    )

    def post(self, text, **kwargs):
        """Post text, possibly split up into several separate messages."""
        reply_to = None
        if 'reply_to_status' in kwargs:
            reply_to = kwargs.pop('reply_to_status').orig
        for part in self.measure.split(text):
            reply_to = self.post_single(part, reply_to_status=reply_to, **kwargs)
            if not reply_to:
                return None
        return reply_to

    def all_relevant_tweets(self, mt_list):
        results = {}
        for tl in (self.mentions(),
                   self.timeline(),
                   self.hashtag(mt_list)):
            for t in tl:
                if t is None:
                    log_.error("Received None status")
                    continue
                if t.id in results:
                    log_.debug("Status %d already in results", t.id)
                    continue
                msg = fromTweet(t, self.myself)
                if msg.has_hashtag('NOBOT', case_sensitive=False):
                    log_.debug("Status %d has NOBOT", t.id)
                    continue
                results[msg.id] = msg
        if results:
            self.high_message = max(self.high_message, *results.keys())
        log_.info("found %d unique status worth looking into", len(results))
        return results

    def mentions(self):
        result = self.cursor(self.twit.mentions_timeline, since_id=self.high_message)
        log_.debug("found %d mentions", len(result))
        return result

    def timeline(self):
        result = self.cursor(self.twit.home_timeline, since_id=self.high_message)
        log_.debug("found %d status in timeline", len(result))
        return result

    def hashtag(self, mt_list):
        tagquery = "(" + " OR ".join(mt_list) + ")"
        result = []
        for ht in self.cursor(self.twit.search, q=tagquery, since_id=self.high_message):
            result.append(self.get_tweet(ht.id))
        log_.debug("found %d status in hashtags", len(result))
        return result

    def cursor(self, task, **kwargs):
        kwargs['tweet_mode'] = 'extended'
        kwargs['include_ext_alt_text'] = True
        try:
            result = []
            for t in tweepy.Cursor(task, **kwargs).items():
                result.append(t)
            log_.warning("%d tweets found", len(result))
            return result
        except tweepy.TweepError as twerror:
            try:
                if twerror.response.status_code == 429:
                    self.warn_rate_error(twerror, "cursoring")
                    return []
            finally:
                pass
            log_.critical("Error %s reading tweets: %s", twerror.api_code, twerror.reason)
        return []

    def get_tweet(self, tweet_id):
        try:
            return self.twit.get_status(
                tweet_id,
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
                log_.debug("%s's Author has blocked us from reading their tweets.", tweet_id)
                return None
            log_.critical("Error %s reading tweet %s: %s",
                          twerror.api_code,
                          tweet_id,
                          twerror.reason)
        return None

    def is_followed(self, user):
        try:
            return self.twit.show_friendship(
                self.myself.id,
                target_id=user.id
            )[0].following
        except tweepy.RateLimitError as rateerror:
            self.warn_rate_error(rateerror, "is_followed @{}".format(user.screen_name))
            return False

    def get_other_status(self, other_id, tlist):
        if not other_id:
            log_.debug("get_other_status with None")
            return None
        if other_id in tlist:
            log_.debug("get_other_status: other_id %d already in %s", other_id, str(tlist))
            return None
        log_.debug("Trying to get other tweet")
        msg = self.get_tweet(other_id)
        if not msg:
            return None
        return fromTweet(msg, self.myself)

def make_twapi(args, highest_ids):
    config = configparser.ConfigParser()
    config.read(args.config)
    auth = tweepy.OAuthHandler(
        config[args.application]['key'],
        config[args.application]['secret']
    )
    auth.set_access_token(
        config[args.user]['token'],
        config[args.user]['secret']
    )
    try:
        api = tweepy.API(auth)
    except tweepy.error.TweepError as te:
        raise RuntimeError(str(te)) from te
    log_.info("Created twitter API instance for @%s", api.me().screen_name)
    return Twitter(api, args.readwrite, highest_ids)
