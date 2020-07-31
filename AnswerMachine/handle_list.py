# pylint: disable=C0114

import Persistence.log as log
from .tweet import Tweet
from .react import process_commands, process_tweet
log_ = log.getLogger(__name__)

def filter_list(tweet_list):
    results = {}
    for api_tweet in tweet_list:
        t = Tweet(api_tweet)
        if t.id in results:
            continue
        if t.has_hashtag(['NOBOT'], case_sensitive=False):
            continue
        results[t.id] = t
    return results

def handle_list(tweet_list, apis, magic_tags):
    tweet_dict = filter_list(tweet_list)
    for tid, tweet in tweet_dict.items():
        log_.info("Looking at tweet %d", tid)
        # exclude some tweets:
        if not tweet.is_eligible(apis.twitter.myself):
            continue
        # handle #folgenbitte and #entfolgen and possibly other meta commands, but
        # only for explicit mentions.
        if tweet.is_explicit_mention(apis.twitter.myself):
            log_.info("Tweet explicitly mentions me")
            process_commands(tweet, apis.twitter)
        if tweet.has_hashtag(magic_tags):
            log_.info("Tweet has magic hashtag")
        # Process this tweet
        mode = tweet.get_mode(apis.twitter.myself, magic_tags)
        process_tweet(tweet, apis, magic_tags, mode)
        # Process quoted or replied-to tweets, only for explicit mentions and magic tags
        if mode == 'all':
            tweet.process_other_tweets(tweet_dict, apis.twitter.myself, magic_tags, apis)
    if len(tweet_dict) > 0:
        return max(tweet_dict.keys())
    return 0
