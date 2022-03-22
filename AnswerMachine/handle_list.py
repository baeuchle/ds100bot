# pylint: disable=C0114

import logging
from .tweet import Tweet
from .react import process_commands, process_tweet
logger = logging.getLogger('bot.' + __name__)

def filter_list(tweet_list):
    results = {}
    for api_tweet in tweet_list:
        if api_tweet is None:
            continue
        t = Tweet(api_tweet)
        if t.id in results:
            continue
        if t.has_hashtag(['NOBOT'], case_sensitive=False):
            continue
        results[t.id] = t
    return results

def handle_list(tweet_list, twitter, database, magic_tags):
    tweet_dict = filter_list(tweet_list)
    for tid, tweet in tweet_dict.items():
        # exclude some tweets:
        if not tweet.is_eligible(twitter.myself):
            logger.debug("Status %s is not eligible", tid)
            continue
        logger.info("Looking at status %d", tid)
        # handle #folgenbitte and #entfolgen and possibly other meta commands, but
        # only for explicit mentions.
        if tweet.is_explicit_mention(twitter.myself):
            logger.info("Tweet explicitly mentions me")
            process_commands(tweet, twitter)
        if tweet.has_hashtag(magic_tags):
            logger.info("Tweet has magic hashtag")
        # Process this tweet
        mode = tweet.get_mode(twitter.myself, magic_tags)
        process_tweet(tweet, twitter, database, magic_tags, modus=mode)
        # Process quoted or replied-to tweets, only for explicit mentions and magic tags
        if mode == 'all':
            tweet.process_other_tweets(tweet_dict, myself=twitter.myself, magic=magic_tags,
                                                   twitter=twitter, database=database)
    if len(tweet_dict) > 0:
        return max(tweet_dict.keys())
    return 0
