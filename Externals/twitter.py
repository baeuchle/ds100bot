"""Twitter API including Command line argumentation"""

import configparser
import logging
import time
import tweepy

from Externals.Measure import Measure
from Externals.tweet import fromTweet
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
                        help="Don't tweet, only read tweets.",
                        required=False)

class Twitter:
    def __init__(self, api, readwrite=False):
        self.twit = api
        try:
            self.myself = self.twit.me()
        except tweepy.error.TweepError as te:
            raise RuntimeError(str(te)) from te
        self.measure = Measure()
        self.readonly = not readwrite

    def tweet_single(self, text, **kwargs):
        """Actually posts text as a new tweet.

        kwargs are passed to tweepy directly.

        Returns:
            - the ID of the newly created tweet if there were no errors (positive)
            - -1 if there was an unknown error
            - -api_code if there was an error with API code api_code

        If api_code is 185 (status update limit), then the program pauses 1 minute and tries again
        (this will be repeated indefinitely) An error message will be logged each time.

        If api_code is neither 185 nor 187 (duplicate tweet), a critical log message will be logged.
        """
        if len(text) == 0:
            log_.error("Empty tweet?")
            return -1
        if tweet_log_.isEnabledFor(logging.WARNING):
            lines = text.splitlines()
            length = max([len(l) for l in lines])
            tt = "▄{}┓\n".format('━'*(length+2))
            for l in lines:
                tt += ("█ {{:{}}} ┃\n".format(length)).format(l)
            tt += "▀{}┛".format('━'*(length+2))
            tweet_log_.warning(tt)
        if self.readonly:
            return 1
        while True: # catches rate limit
            try:
                new_tweet = self.twit.update_status(text, **kwargs)
                return new_tweet.id
            except tweepy.TweepError as twerror:
                if twerror.api_code is None:
                    log_.critical("Unknown error while tweeting: %s", twerror.reason)
                    return -1
                if twerror.api_code == 185: # status update limit (tweeted too much)
                    log_.error("Tweeted too much, waiting 1 Minute before trying again")
                    time.sleep(60)
                    continue
                if twerror.api_code == 385:
                    log_.critical("Error 385: Tried to reply to deleted or invisible tweet %s",
                        kwargs.get('in_reply_to_status_id', 'N/A'))
                elif twerror.api_code != 187: # duplicate tweet
                    log_.critical("Error %s tweeting: %s", twerror.api_code, twerror.reason)
                return -int(twerror.api_code)

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

    def tweet(self, text, **kwargs):
        """Tweet text, possibly split up into several separate tweets.

        Returns:
            - ID of the last tweet that was sent, if all tweets were sent successfully
            - ID of the original tweet or last tweet that was sent if the last attempt ended in a
              duplicate tweet-error.
            - Negative API code if there was a different error.
        """
        reply_id = kwargs.get('in_reply_to_status_id', 0)
        kwargs['auto_populate_reply_metadata'] = True
        for part in self.measure.split(text):
            new_reply_id = self.tweet_single(part, **kwargs)
            if new_reply_id == -187: # duplicate tweet: Don't tweet the others
                return reply_id
            if new_reply_id < 0: # other error: return error code.
                return new_reply_id
            # all ok: go on with new id
            kwargs['in_reply_to_status_id'] = new_reply_id
            reply_id = new_reply_id
        return reply_id

    def all_relevant_tweets(self, highest_id, mt_list):
        results = {}
        for tl in (self.mentions(highest_id),
                   self.timeline(highest_id),
                   self.hashtag(mt_list, highest_id)):
            for t in tl:
                if t is None:
                    log_.error("Received None tweet")
                    continue
                if t.id in results:
                    continue
                msg = fromTweet(t, self.myself)
                if msg.has_hashtag(['NOBOT'], case_sensitive=False):
                    continue
                results[msg.id] = msg
        log_.info("found %d unique status worth looking into", len(results))
        return results

    def mentions(self, highest_id):
        return self.cursor(self.twit.mentions_timeline, since_id=highest_id)

    def timeline(self, highest_id):
        return self.cursor(self.twit.home_timeline, since_id=highest_id)

    def hashtag(self, mt_list, highest_id):
        tagquery = "(" + " OR ".join(mt_list) + ")"
        tweets = []
        for ht in self.cursor(self.twit.search, q=tagquery, since_id=highest_id):
            tweets.append(self.get_tweet(ht.id))
        return tweets

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

    def get_other_tweet(self, other_id, tlist):
        if not other_id:
            log_.debug("get_other_tweet with None")
            return None
        if other_id in tlist:
            log_.debug("get_other_tweet: other_id %d already in %s", other_id, str(tlist))
            return None
        log_.debug("Trying to get other tweet")
        msg = self.get_tweet(other_id)
        if not msg:
            return None
        return fromTweet(msg, self.myself)

def make_twapi(args):
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
    return Twitter(api, args.readwrite)
