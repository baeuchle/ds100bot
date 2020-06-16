#!/usr/bin/python3

import api
from database import Database
import gitdescribe as git
import react
import since

import argparse
import log
import sys

parser = argparse.ArgumentParser(description='Bot zur DS100-Expansion auf Twitter')
parser.add_argument('--readwrite',
                    dest='rw',
                    help='equivalent to --api readwrite --db readwrite',
                    required=False,
                    action='store_true',
                    default=False)
parser.add_argument('--api',
                    dest='api',
                    help='API to use: readwrite, readonly, mock',
                    required=False,
                    action='store',
                    default=None)
parser.add_argument('--db',
                    dest='db',
                    help='Database to use: readwrite, readonly',
                    required=False,
                    action='store',
                    default=None)
parser.add_argument('--verbose', '-v',
                    dest='verbose',
                    help='Output lots of stuff',
                    required=False,
                    action='count')
parser.add_argument('--external',
                    dest='external',
                    help='(Mock API only) Read mocked tweet objects not from the internal list, but from tweet_details.py. That file may be created with get_tweet.py.',
                    required=False,
                    action='store_true',
                    default=False
                   )
parser.add_argument('--parse_one',
                    dest='parse_one',
                    help='(Mock API only) Parse only mocked tweet with this ID',
                    required=False,
                    action='store',
                    default=None
                   )
args = parser.parse_args()

if args.db is None:
    if args.rw:
        args.db = 'readwrite'
    else:
        args.db = 'readonly'
if args.api is None:
    if args.rw:
        args.api = 'readwrite'
    else:
        args.api = 'readonly'
if args.verbose is None:
    args.verbose = 0
args.verbose = 50 - args.verbose * 10
loglvl = 50 - args.verbose * 10
if loglvl <= 0:
    loglvl = 1

log.basicConfig(level=loglvl, style='{')
log_ = log.getLogger('ds100')

# setup twitter API
twapi = api.get_api_object(args.api,
    external=args.external, parse_one=args.parse_one)
# setup database
sql = Database(args.db)
git.notify_new_version(sql, twapi)

highest_id = since.get_since_id(sql)

tagsearch, magic_tags = sql.magic_hashtags()
log_.info("Magic Tags: %s", magic_tags)

tweet_list = twapi.all_relevant_tweets(highest_id, tagsearch)
for id, tweet in tweet_list.items():
    log_.info("Looking at tweet %d", id)
    # exclude some tweets:
    if tweet.author().screen_name == twapi.myself.screen_name:
        log_.debug("Not replying to my own tweets")
        continue
    if tweet.is_retweet():
        log_.debug("Not processing pure retweets")
        continue
    # handle #folgenbitte and #entfolgen and possibly other meta commands, but
    # only for explicit mentions.
    if tweet.is_explicit_mention(twapi.myself):
        log_.info("Tweet explicitly mentions me")
        react.process_commands(tweet, twapi)
    if tweet.has_hashtag(magic_tags):
        log_.info("Tweet has magic hashtag")
    # Process this tweet
    mode = None
    if tweet.is_explicit_mention(twapi.myself) or tweet.has_hashtag(magic_tags):
        mode = 'all'
    react.process_tweet(tweet, twapi, sql, magic_tags, mode)
    # Process quoted or replied-to tweets, only for explicit mentions and magic tags
    if tweet.is_explicit_mention(twapi.myself) or tweet.has_hashtag(magic_tags):
        for other_id in tweet.quoted_status_id(), tweet.in_reply_id():
            if other_id in tweet_list:
                log_.debug("Other tweet %d already in tweet list", other_id)
            else:
                log_.info("Obtaining other tweet %s", other_id)
            if (not other_id is None) and other_id not in tweet_list:
                other_tweet = twapi.get_tweet(other_id)
                if other_tweet is None:
                    continue
                # don't process the other tweet if we should have seen it before (this
                # also prevents recursion via this branch):
                if other_tweet.is_mention(twapi.myself):
                    log_.info("Not processing other tweet because it already mentions me")
                if other_tweet.has_hashtag(magic_tags):
                    log_.info("Not processing other tweet because it already has the magic hashtag")
                else:
                    log_.info("Processing tweet %d mode 'all'", tweet.id)
                    dmt_list = [t[0] for t in tweet.hashtags(magic_tags)]
                    dmt = 'DS100'
                    if len(dmt_list) > 0:
                        dmt = dmt_list[0]
                    react.process_tweet(other_tweet, twapi,
                        sql, magic_tags,
                        modus='all'
                            if tweet.is_explicit_mention(twapi.myself)
                            else None,
                        default_magic_tag=dmt
                    )

git.store_version(sql)
if tweet_list:
    since.store_since_id(sql, max(tweet_list.keys()))
if args.api == 'mock':
    twapi.statistics()

sql.close_sucessfully()
