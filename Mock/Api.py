# pylint: disable=C0114

import logging
import tweepy # for exceptions
from Externals import Twitter
from Externals.Measure import Measure
from AnswerMachine.tweet import Tweet
from .Tweet import User, mocked_source, mocked_tweets
logger = logging.getLogger('bot.test.api')

class Count: # pylint: disable=too-few-public-methods
    def __init__(self):
        self.correct = 0
        self.missed = 0
        self.bad_content = 0

class Result: # pylint: disable=too-few-public-methods
    def __init__(self):
        self.tweet = Count()
        self.follow = Count()

class MockApi(Twitter): # pylint: disable=too-many-instance-attributes
    def __init__(self, **kwargs):
        self.running_id = 10001
        self.myself = User.theBot
        self.mode = kwargs.get('mode', 'testcases')
        mocked_t = mocked_tweets()
        if self.mode == 'external':
            self.mock = mocked_source()
        elif self.mode == 'testcases':
            self.mock = mocked_t
        elif self.mode == 'id':
            self.mock = [t for t in mocked_t if t.id in kwargs.get('id_list', [])]
        else:
            raise ValueError("Invalid mode in {}: {}".format(__name__, self.mode))
        self.replies = {}
        self.double_replies = []
        self.measure = Measure()
        self.readonly = True

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
                    logger.warning("Tweet %d was replied to twice!", reply_id)
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

    def statistics(self, output='descriptive'):
        stat_log = logging.getLogger('statistics')
        res_count = Result()
        stat_log.debug("    RESULTS")
        for t in self.mock:
            was_replied_to = t.id in self.replies
            if t.expected_answer is None:
                if was_replied_to:
                    stat_log.error("Tweet %d falsely answered", t.id)
                    res_count.tweet.missed += 1
                else:
                    res_count.tweet.correct += 1
                    stat_log.info("Tweet %d correctly unanswered", t.id)
                continue
            # expected answer is not None:
            if not was_replied_to:
                res_count.tweet.missed += 1
                stat_log.error("Tweet %d falsely unanswered", t.id)
                continue
            # correctly answered: is it the correct answer?
            if t.expected_answer == self.replies[t.id]:
                res_count.tweet.correct += 1
                stat_log.info("Tweet %d correctly answered with correct answer", t.id)
                continue
            res_count.tweet.bad_content += 1
            stat_log.error("Tweet %d correctly answered, but with wrong answer", t.id)
            stat_log.warning(t.expected_answer)
            stat_log.warning("↑↑↑↑EXPECTED↑↑↑↑  ↓↓↓↓GOT THIS↓↓↓↓")
            stat_log.warning(self.replies[t.id])
        for l in User.followers, User.nonfollowers:
            for u in l:
                if u.follows == u.follow_after:
                    stat_log.info("User @%s has correct following behaviour %s",
                                  u.screen_name, u.follows)
                    res_count.follow.correct += 1
                else:
                    stat_log.error("User @%s doesn't follow correctly (should %s, does %s)",
                                   u.screen_name, u.follow_after, u.follows)
                    res_count.follow.missed += 1
        self.report_statisctics(stat_log, output, res_count)
        return res_count.tweet.missed + res_count.tweet.bad_content + res_count.follow.missed

    def report_statisctics(self, stat_log, output, res_count): # pylint: disable=R0201
        denominator = (res_count.tweet.correct + res_count.tweet.missed +
                       res_count.tweet.bad_content + res_count.follow.correct +
                       res_count.follow.missed)
        if denominator == 0:
            stat_log.log(51, "No testcases found")
        elif output == 'descriptive':
            stat_log.log(51, "ALL GOOD:               %2d", res_count.tweet.correct)
            stat_log.log(51, "INCORRECT TEXT:         %2d", res_count.tweet.bad_content)
            stat_log.log(51, "WRONG ANSWER/NOT ANSWER:%2d", res_count.tweet.missed)
            stat_log.log(51, "CORRECT FOLLOWING:      %2d", res_count.follow.correct)
            stat_log.log(51, "WRONG FOLLOWING:        %2d", res_count.follow.missed)
        elif output == 'summary':
            ratio = (res_count.tweet.correct + res_count.follow.correct) / (0.0 + denominator)
            stat_log.log(51, "A %d/%d F %d/%d R %.1f%%",
                         res_count.tweet.correct,
                         res_count.tweet.bad_content + res_count.tweet.missed,
                         res_count.follow.correct, res_count.follow.missed,
                         100.0 * ratio)
