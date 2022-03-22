# pylint: disable=C0114

import logging
from .react import process_commands, process_tweet
logger = logging.getLogger('bot.' + __name__)

def handle_list(tweet_dict, twitter, database, magic_tags):
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
