from api_twitter import TwitterApi
from tweet import Tweet
import tweepy # for exceptions
import re

from tweet_mock import *

class MockApi(TwitterApi):
    def __init__(self, verbose, **kwargs):
        self.verbose = verbose + 1
        self.running_id = 10001
        self.myself = User.theBot
        self.external = kwargs.get('external', False)
        if self.external:
            self.mock = mocked_source()
        else:
            self.mock = mocked_tweets(verbose)
        self.replies = {}
        if self.verbose > 0:
            print('Running from Mock API (faked tweets)')

    def get_tweet(self, tweet_id):
        for t in self.mock:
            if t.id == tweet_id:
                return t
        raise tweepy.TweepError("Kein solcher Tweet vorhanden")

    def tweet(self, text, **kwargs):
        super().tweet(text, **kwargs)
        if 'in_reply_to_status_id' in kwargs:
            reply_id = kwargs['in_reply_to_status_id']
            # don't track thread answers:
            if reply_id != self.running_id:
                if reply_id in self.replies:
                    print("Tweet {} was replied to twice!")
                    self.double_replies.append(reply_id)
                else:
                    self.replies[reply_id] = text
        self.running_id += 1
        return self.running_id

    def mentions(self, highest_id):
        mention_list = []
        for t in self.mock:
            for um in t.original.raw['entities']['user_mentions']:
                if um['screen_name'] == self.myself.screen_name:
                    mention_list.append(t)
                    break
        return mention_list

    def timeline(self, highest_id):
        return [t for t in self.mock if t.author().follows]

    def hashtag(self, q, highest_id):
        return [t for t in self.mock if t.has_hashtag(q)]

    def is_followed(self, user):
        return user.follows

    def follow(self, user):
        super().follow(user)
        user.follows = True

    def defollow(self, user):
        super().defollow(user)
        user.follows = False

    def statistics(self):
        if self.external:
            return
        all_ok = 0
        wrongs = 0
        badrpl = 0
        print("━"*120)
        print("    RESULTS")
        for t in self.mock:
            print("Tweet", t.id, end=' ')
            was_replied_to = t.id in self.replies
            if t.original.expected_answer is None:
                if was_replied_to:
                    print("falsely answered")
                    wrongs += 1
                else:
                    all_ok += 1
                    print("correcly unanswered")
                continue
            # expected answer is not None:
            if not was_replied_to:
                wrongs += 1
                print("falsely unanswered")
                continue
            # correctly answered: is it the correct answer?
            if t.original.expected_answer == self.replies[t.id]:
                all_ok += 1
                print("correctly answered with correct answer")
                continue
            badrpl += 1
            print("correctly answered, but with wrong answer")
            if self.verbose > 2:
                print(t.original.expected_answer)
                print(self.replies[t.id])
        print()
        print("ALL GOOD:               ", all_ok)
        print("INCORRECT TEXT:         ", badrpl)
        print("WRONG ANSWER/NOT ANSWER:", wrongs)
        for l in User.followers, User.nonfollowers:
            for u in l:
                print("User @{}".format(u.screen_name), end=' ')
                if u.follows == u.follow_after:
                    print("has correct following behaviour {}".format(u.follows))
                else:
                    print("doesn't follow correctly (should {}, does {})".format(u.follow_after, u.follows))
