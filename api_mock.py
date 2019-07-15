from tweet import Tweet
import tweepy # for exceptions
import re

from tweet_mock import *

class MockApi:
    def __init__(self, verbose):
        self.verbose = verbose + 1
        self.running_id = 108
        self.myself = User(id='@_ds_100', screen_name='_ds_100')
        self.mock = mocked_tweets(verbose)

    def get_tweet(self, tweet_id):
        for t in self.mock:
            if t.id == tweet_id:
                return t
        raise tweepy.TweepError("Kein solcher Tweet vorhanden")

    def tweet(self, text, *args, **kwargs):
        if self.verbose > 1:
            lines = text.splitlines()
            length = max([len(l) for l in lines])
            print("+{}+".format('-'*(length+2)))
            for l in lines:
                print(("| {{:{}}} |".format(length)).format(l))
            print("+{}+".format('-'*(length+2)))
        self.running_id += 1
        return self.running_id

    def all_relevant_tweets(self, highest_id, tag):
        results = {}
        for tl in self.mentions(highest_id), self.timeline(highest_id), self.hashtag(tag, highest_id):
            for t in tl:
                results[t.id] = t
        return results

    def mentions(self, highest_id):
        mention_list = []
        for t in self.mock:
            for um in t.original.raw['entities']['user_mentions']:
                if um['screen_name'] == self.myself.screen_name:
                    mention_list.append(t)
                    break
        return mention_list

    def timeline(self, highest_id):
        timeline_list = []
        for t in self.mock:
            if 'in_timeline' in t.original.raw and t.original.raw['in_timeline']:
                timeline_list.append(t)
        return timeline_list

    def hashtag(self, q, highest_id):
        hashtag_list = []
        for t in self.mock:
            for ht in t.original.raw['entities']['hashtags']:
                if ht['text'] == 'DS100':
                    hashtag_list.append(t)
                    break
        return hashtag_list
