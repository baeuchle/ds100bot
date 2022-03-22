# pylint: disable=C0114
import logging
from .react import process_commands, process_tweet
logger = logging.getLogger('bot.' + __name__)

def handle_list(tweet_dict, twitter, database, magic_tags, magic_emojis):
    for tid, tweet in tweet_dict.items():
        # exclude some tweets:
        if not tweet.is_eligible(twitter.myself):
            logger.debug("Status %s is not eligible", tid)
            continue
        logger.info("Looking at status %d", tid)
        # handle #folgenbitte and #entfolgen and possibly other meta commands, but
        # only for explicit mentions.
        if tweet.is_explicit_mention:
            logger.info("Tweet explicitly mentions me")
            process_commands(tweet, twitter)
        if tweet.has_hashtag(magic_tags):
            logger.info("Tweet has magic hashtag")
        if tweet.has_hashtag(magic_emojis):
            logger.info("Tweet has magic emoji")
        # Process this tweet
        mode = tweet.get_mode(magic_tags, magic_emojis)
        process_tweet(tweet,
                twitter,
                database,
                magic_tags,
                magic_emojis,
                modus=mode)
        dmt = tweet.default_magic_hashtag([*magic_tags, *magic_emojis])
        for other in tweet.get_other_tweets(
                    tweet_dict,
                    mode=mode,
                    network=twitter,
                    database=database,
                    myself=twitter.myself,
                    magic_tags=magic_tags,
                    magic_emojis=magic_emojis
                ):
            logger.debug("Processing tweet %d mode %s def magic hash tag %s", other.id, mode, dmt)
            process_tweet(other,
                    twitter,
                    database,
                    magic_tags,
                    magic_emojis,
                    modus=mode,
                    default_magic_tag=dmt)
    if len(tweet_dict) > 0:
        return max(tweet_dict.keys())
    return 0
