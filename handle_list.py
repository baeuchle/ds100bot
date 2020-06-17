import react
import log
log_ = log.getLogger(__name__)

def handle_list(tweet_list, apis, magic_tags):
    for tid, tweet in tweet_list.items():
        log_.info("Looking at tweet %d", tid)
        # exclude some tweets:
        if tweet.author().screen_name == apis.twitter.myself.screen_name:
            log_.debug("Not replying to my own tweets")
            continue
        if tweet.is_retweet():
            log_.debug("Not processing pure retweets")
            continue
        # handle #folgenbitte and #entfolgen and possibly other meta commands, but
        # only for explicit mentions.
        if tweet.is_explicit_mention(apis.twitter.myself):
            log_.info("Tweet explicitly mentions me")
            react.process_commands(tweet, apis.twitter)
        if tweet.has_hashtag(magic_tags):
            log_.info("Tweet has magic hashtag")
        # Process this tweet
        mode = None
        if tweet.is_explicit_mention(apis.twitter.myself) or tweet.has_hashtag(magic_tags):
            mode = 'all'
        react.process_tweet(tweet, apis, magic_tags, mode)
        # Process quoted or replied-to tweets, only for explicit mentions and magic tags
        if tweet.is_explicit_mention(apis.twitter.myself) or tweet.has_hashtag(magic_tags):
            for other_id in tweet.quoted_status_id(), tweet.in_reply_id():
                if other_id in tweet_list:
                    log_.debug("Other tweet %d already in tweet list", other_id)
                else:
                    log_.info("Obtaining other tweet %s", other_id)
                if (not other_id is None) and other_id not in tweet_list:
                    other_tweet = apis.twitter.get_tweet(other_id)
                    if other_tweet is None:
                        continue
                    # don't process the other tweet if we should have seen it before (this
                    # also prevents recursion via this branch):
                    if other_tweet.is_mention(apis.twitter.myself):
                        log_.info("Not processing other tweet because it already mentions me")
                    if other_tweet.has_hashtag(magic_tags):
                        log_.info("Not processing other tweet because it already has the magic hashtag")
                    else:
                        log_.info("Processing tweet %d mode 'all'", tweet.id)
                        dmt_list = [t[0] for t in tweet.hashtags(magic_tags)]
                        dmt = 'DS100'
                        if len(dmt_list) > 0:
                            dmt = dmt_list[0]
                        react.process_tweet(other_tweet, apis, magic_tags,
                            modus='all'
                                if tweet.is_explicit_mention(apis.twitter.myself)
                                else None,
                            default_magic_tag=dmt
                        )
    if len(tweet_list) > 0:
        return max(tweet_list.keys())
    else:
        return 0
