# pylint: disable=C0114

import react
import log
log_ = log.getLogger(__name__)

def handle_list(tweet_list, apis, magic_tags):
    for tid, tweet in tweet_list.items():
        log_.info("Looking at tweet %d", tid)
        # exclude some tweets:
        if not tweet.is_eligible(apis.twitter.myself):
            continue
        # handle #folgenbitte and #entfolgen and possibly other meta commands, but
        # only for explicit mentions.
        if tweet.is_explicit_mention(apis.twitter.myself):
            log_.info("Tweet explicitly mentions me")
            react.process_commands(tweet, apis.twitter)
        if tweet.has_hashtag(magic_tags):
            log_.info("Tweet has magic hashtag")
        # Process this tweet
        mode = tweet.get_mode(apis.twitter.myself, magic_tags)
        react.process_tweet(tweet, apis, magic_tags, mode)
        # Process quoted or replied-to tweets, only for explicit mentions and magic tags
        if mode == 'all':
            tweet.process_other_tweets(tweet_list, apis.twitter.myself, magic_tags, apis)
    if len(tweet_list) > 0:
        return max(tweet_list.keys())
    return 0
