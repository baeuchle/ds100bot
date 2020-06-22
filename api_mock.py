# pylint: disable=C0114

import tweepy # for exceptions
from Externals import TwitterBase
from AnswerMachine.tweet import Tweet

from tweet_mock import User, mocked_source, mocked_tweets
import Persistence.log as log
log_ = log.getLogger(__name__)

class MockApi(TwitterBase):
    def __init__(self, **kwargs):
        log_.setLevel(log_.getEffectiveLevel() - 10)
        self.running_id = 10001
        self.myself = User.theBot
        self.external = kwargs.get('external', False)
        if self.external:
            self.mock = mocked_source()
        else:
            self.mock = mocked_tweets()
            p_id = kwargs.get('parse_one', None)
            if p_id is not None:
                self.mock = [self.get_tweet(int(p_id))]
        self.replies = {}
        self.double_replies = []

    def get_tweet(self, tweet_id):
        for t in self.mock:
            if t.id == tweet_id:
                return t
        raise tweepy.TweepError("Kein solcher Tweet vorhanden")

    def tweet_single(self, text, **kwargs):
        super().tweet_single(text, **kwargs)
        if 'in_reply_to_status_id' in kwargs:
            reply_id = kwargs['in_reply_to_status_id']
            # don't track thread answers:
            if reply_id != self.running_id:
                if reply_id in self.replies:
                    log_.warning("Tweet %d was replied to twice!", reply_id)
                    self.double_replies.append(reply_id)
                else:
                    self.replies[reply_id] = text.strip()
        self.running_id += 1
        return self.running_id

    def mentions(self, highest_id):
        mention_list = []
        for t in self.mock:
            for um in t.raw['entities']['user_mentions']:
                if um['screen_name'] == self.myself.screen_name:
                    mention_list.append(t)
                    break
        return mention_list

    def timeline(self, highest_id):
        return [t for t in self.mock if t.author.follows]

    def hashtag(self, tag, highest_id):
        return [t for t in self.mock if Tweet(t).has_hashtag(tag)]

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
        stat_log = log.getLogger('statistics', '{message}')
        all_ok = 0
        wrongs = 0
        badrpl = 0
        stat_log.debug("    RESULTS")
        for t in self.mock:
            was_replied_to = t.id in self.replies
            if t.expected_answer is None:
                if was_replied_to:
                    stat_log.error("Tweet %d falsely answered", t.id)
                    wrongs += 1
                else:
                    all_ok += 1
                    stat_log.info("Tweet %d correcly unanswered", t.id)
                continue
            # expected answer is not None:
            if not was_replied_to:
                wrongs += 1
                stat_log.error("Tweet %d falsely unanswered", t.id)
                continue
            # correctly answered: is it the correct answer?
            if t.expected_answer == self.replies[t.id]:
                all_ok += 1
                stat_log.info("Tweet %d correctly answered with correct answer", t.id)
                continue
            badrpl += 1
            stat_log.error("Tweet %d correctly answered, but with wrong answer", t.id)
            stat_log.warning(t.expected_answer)
            stat_log.warning(self.replies[t.id])
        bad_flw = 0
        goodflw = 0
        for l in User.followers, User.nonfollowers:
            for u in l:
                if u.follows == u.follow_after:
                    stat_log.info("User @%s has correct following behaviour %s",
                                  u.screen_name, u.follows)
                    goodflw += 1
                else:
                    stat_log.error("User @%s doesn't follow correctly (should %s, does %s)",
                                   u.screen_name, u.follow_after, u.follows)
                    bad_flw += 1
        stat_log.log(51, "ALL GOOD:               %2d", all_ok)
        stat_log.log(51, "INCORRECT TEXT:         %2d", badrpl)
        stat_log.log(51, "WRONG ANSWER/NOT ANSWER:%2d", wrongs)
        stat_log.log(51, "CORRECT FOLLOWING:      %2d", goodflw)
        stat_log.log(51, "WRONG FOLLOWING:        %2d", bad_flw)
