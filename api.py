from api_twitter import TwitterApi
from api_mock import MockApi
from tweet import Tweet
import tweepy
import log
log_ = log.getLogger(__name__)

def get_api_object(mode, **kwargs):
    if mode == "mock":
        return MockApi(**kwargs)
    if mode == "readonly":
        return ReadOnlyApi()
    return ReadWriteApi()

class ReadOnlyApi(TwitterApi):
    def __init__(self):
        super().__init__()
        log_.setLevel(log_.getEffectiveLevel() - 10)
        log_.warning('Running from readonly twitter API (read real tweets, do not actually post answers)')

class ReadWriteApi(TwitterApi):
    def __init__(self):
        super().__init__()

    def tweet_single(self, text, **kwargs):
        super().tweet_single(text, **kwargs)
        try:
            new_tweet = self.twit.update_status(text, **kwargs)
            return new_tweet.id
        except tweepy.RateLimitError as rateerror:
            self.warn_rate_error(rateerror, "tweeting")
            return 0
        except tweepy.TweepError as twerror:
            if twerror.api_code == 187: # duplicate tweet
                return 0
            log_.critical("Error {} tweeting: {}".format(twerror.api_code, twerror.reason))
            return -1

    def follow(self, user):
        super().follow(user)
        try:
            self.twit.create_friendship(id=user.id)
        except tweepy.RateLimitError as rateerror:
            self.warn_rate_error("follow @{}".format(user.screen_name))

    def defollow(self, user):
        super().defollow(user)
        try:
            self.twit.destroy_friendship(id=user.id)
        except tweepy.RateLimitError as rateerror:
            self.warn_rate_error("defollow @{}".format(user.screen_name))
