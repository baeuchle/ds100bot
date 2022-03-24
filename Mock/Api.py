# pylint: disable=C0114

import logging
import tweepy # for exceptions
from Externals import Network
from Externals.Measure import Measure
from Externals.message import fromTweet
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

class MockApi(Network): # pylint: disable=too-many-instance-attributes
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
        self.high_message = 0
        self.from_function = fromTweet

    def get_status(self, status_id):
        for t in self.mock:
            if t.id == status_id:
                return t
        raise tweepy.TweepError("Kein solcher Tweet vorhanden")

    def post_single(self, text, **kwargs):
        super().post_single(text, **kwargs)
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

    def defollow(self, _):
        pass

    def follow(self, _):
        pass

    def is_followed(self, _):
        return True

    def mentions(self):
        mention_list = []
        for t in self.mock:
            for um in t.raw['entities']['user_mentions']:
                if um['screen_name'] == self.myself.screen_name:
                    mention_list.append(t)
        logger.debug("found %d mentions", len(mention_list))
        return mention_list

    def timeline(self):
        result = [t for t in self.mock if str(t.author) == "followee"]
        logger.debug("found %d status in timeline", len(result))
        return result

    def hashtags(self, mt_list):
        result = [t for t in self.mock if fromTweet(t, self.myself).has_hashtag(mt_list)]
        logger.debug("found %d status in hashtags", len(result))
        return result

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
        self.report_statisctics(stat_log, output, res_count)
        return res_count.tweet.missed + res_count.tweet.bad_content

    def report_statisctics(self, stat_log, output, res_count): # pylint: disable=R0201
        denominator = (res_count.tweet.correct + res_count.tweet.missed +
                       res_count.tweet.bad_content)
        if denominator == 0:
            stat_log.log(51, "No testcases found")
        elif output == 'descriptive':
            stat_log.log(51, "ALL GOOD:               %2d", res_count.tweet.correct)
            stat_log.log(51, "INCORRECT TEXT:         %2d", res_count.tweet.bad_content)
            stat_log.log(51, "WRONG ANSWER/NOT ANSWER:%2d", res_count.tweet.missed)
        elif output == 'summary':
            ratio = (res_count.tweet.correct) / (0.0 + denominator)
            stat_log.log(51, "A %d/%d R %.1f%%",
                         res_count.tweet.correct,
                         res_count.tweet.bad_content + res_count.tweet.missed,
                         100.0 * ratio)
