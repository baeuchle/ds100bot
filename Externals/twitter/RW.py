# pylint: disable=C0114

import tweepy
import Persistence.log as log
from Externals.twitter.Api import TwitterBase as BaseApi
log_ = log.getLogger(__name__)

class ReadWrite(BaseApi):

    def tweet_single(self, text, **kwargs):
        super().tweet_single(text, **kwargs)
        try:
            new_tweet = self.twit.update_status(text, **kwargs)
            return new_tweet.id
        except tweepy.RateLimitError as rateerror:
            self.warn_rate_error(rateerror, "tweeting")
            return 0
        except tweepy.TweepError as twerror:
            if twerror.api_code is None:
                log_.critical("Unknown error while tweeting: %s", twerror.reason)
                return -1
            if twerror.api_code != 187: # duplicate tweet
                log_.critical("Error %s tweeting: %s", twerror.api_code, twerror.reason)
            return -int(twerror.api_code)

    def follow(self, user):
        super().follow(user)
        try:
            self.twit.create_friendship(id=user.id)
        except tweepy.RateLimitError as rateerror:
            self.warn_rate_error(rateerror, "follow @{}".format(user.screen_name))

    def defollow(self, user):
        super().defollow(user)
        try:
            self.twit.destroy_friendship(id=user.id)
        except tweepy.RateLimitError as rateerror:
            self.warn_rate_error(rateerror, "defollow @{}".format(user.screen_name))
