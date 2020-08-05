# pylint: disable=C0114

import time
import tweepy
import Persistence.log as log
from Externals.twitter.Api import TwitterBase as BaseApi
log_ = log.getLogger(__name__)

class ReadWrite(BaseApi):

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
        super().tweet_single(text, **kwargs)
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
