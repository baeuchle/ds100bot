import tweepy
from tweet import Tweet
from measure import split_text
import log
log_ = log.getLogger(__name__)
tweet_log_ = log.getLogger('tweet', '{message}')

class TwitterApi:
    def __init__(self):
        import credentials
        auth = tweepy.OAuthHandler(credentials.consumer_key, credentials.consumer_secret)
        auth.set_access_token(credentials.access_token, credentials.access_token_secret)
        self.twit = tweepy.API(auth)
        self.myself = self.twit.me()

    def warn_rate_error(self, rate_err, description):
        log_.critical("Rate limit violated at %s: %s", description, rate_err.reason)
        self.print_rate_limit()

    def print_rate_limit(self):
        if log_.getEffectiveLevel() > 49:
            return
        rls = self.twit.rate_limit_status()
        res = rls['resources']
        for r in res:
            for l in res[r]:
                rrl = res[r][l]
                if rrl['limit'] != rrl['remaining'] and rrl['remaining'] < 5:
                    log_.critical("Resource limit for %s low: %s of %s remaining",
                        l,
                        rrl['remaining'],
                        rrl['limit']
                    )

    # Return new tweet id, 0 if RateLimit (= try again), -1 if other
    # error (fix before trying again).
    def tweet(self, text, **kwargs):
        reply_id = kwargs.get('in_reply_to_status_id', 0)
        kwargs['auto_populate_reply_metadata'] = True
        for part in split_text(text):
            new_reply_id = self.tweet_single(part, **kwargs)
            kwargs['in_reply_to_status_id'] = new_reply_id
            if new_reply_id > 0:
                reply_id = new_reply_id
        return reply_id

    def tweet_single(self, text, **_):
        if len(text) == 0:
            log_.error("Empty tweet?")
            return -1
        if tweet_log_.isEnabledFor(log.WARNING):
            lines = text.splitlines()
            length = max([len(l) for l in lines])
            tt = "▄{}┓\n".format('━'*(length+2))
            for l in lines:
                tt += ("█ {{:{}}} ┃\n".format(length)).format(l)
            tt += "▀{}┛".format('━'*(length+2))
            tweet_log_.warning(tt)
        return 0

    def all_relevant_tweets(self, highest_id, tag):
        results = {}
        for tl in (self.mentions(highest_id),
                   self.timeline(highest_id),
                   self.hashtag(tag, highest_id)):
            for t in tl:
                if not t.has_hashtag(['NOBOT'], case_sensitive=False):
                    results[t.id] = t
        return results

    def mentions(self, highest_id):
        return self.cursor(self.twit.mentions_timeline, since_id=highest_id)

    def timeline(self, highest_id):
        return self.cursor(self.twit.home_timeline, since_id=highest_id)

    def hashtag(self, tag, highest_id):
        return self.cursor(self.twit.search, q=tag, since_id=highest_id)

    def cursor(self, task, **kwargs):
        kwargs['tweet_mode'] = 'extended'
        kwargs['include_ext_alt_text'] = True
        try:
            result = []
            for t in tweepy.Cursor(task, **kwargs).items():
                result.append(Tweet(t))
            log_.warning("%d tweets found", len(result))
            return result
        except tweepy.RateLimitError as rateerror:
            self.warn_rate_error(rateerror, "cursoring")
        except tweepy.TweepError as twerror:
            print("Error {} reading tweets: {}".format(twerror.api_code, twerror.reason))
        return []

    def get_tweet(self, tweet_id):
        try:
            return Tweet(self.twit.get_status(
                tweet_id,
                tweet_mode='extended',
                include_ext_alt_text=True
            ))
        except tweepy.RateLimitError as rateerror:
            self.warn_rate_error(rateerror, "getting tweet")
        except tweepy.TweepError as twerror:
            log_.critical("Error %s reading tweet %s: %s",
                          twerror.api_code,
                          tweet_id,
                          twerror.reason)
        return None

    def follow(self, user):
        log_.warning("Follow @%s", user.screen_name)

    def defollow(self, user):
        log_.warning("Defollow @%s", user.screen_name)

    def is_followed(self, user):
        try:
            return self.twit.show_friendship(
                self.myself.id,
                target_id=user.id
            )[0].following
        except tweepy.RateLimitError as rateerror:
            self.warn_rate_error(rateerror, "is_followed @{}".format(user.screen_name))
            return False
