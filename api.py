from api_twitter import TwitterApi
from api_mock import MockApi
from tweet import Tweet
import tweepy

def get_api_object(mode, verbose):
    if mode == "mock":
        return MockApi(verbose)
    if mode == "readonly":
        return ReadOnlyApi(verbose)
    return ReadWriteApi(verbose)

class ReadOnlyApi(TwitterApi):
    def __init__(self, verbose):
        super().__init__(verbose + 1)
        if self.verbose > 0:
            print('Running from readonly twitter API (read real tweets, do not actually post answers)')

class ReadWriteApi(TwitterApi):
    def __init__(self, verbose):
        super().__init__(verbose)

    def warn_rate_error(self, rate_err, description):
        print ("Rate limit violated at {}: {}".format(description, rate_err.reason))
        super().print_rate_limit()

    # Return new tweet id, 0 if RateLimit (= try again), -1 if other
    # error (fix before trying again).
    def tweet(self, text, **kwargs):
        super().tweet(text, **kwargs)
        try:
            new_tweet = self.twit.update_status(text, **kwargs)
            return new_tweet.id
        except tweepy.RateLimitError as rateerror:
            warn_rate_error(rateerror, "tweeting")
            return 0
        except tweepy.TweepError as twerror:
            if twerror.api_code == 187: # duplicate tweet
                return 0
            print("Error {} tweeting: {}".format(twerror.api_code, twerror.reason))
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
