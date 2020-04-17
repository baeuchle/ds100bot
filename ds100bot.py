#!/usr/bin/python3

import api
from database import Database
import gitdescribe as git
import react
import since

import argparse
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

# setup twitter API
twapi = api.get_api_object(args.api, args.verbose)
# setup database
sql = Database(args.db, args.verbose)
git.notify_new_version(sql, twapi, args.verbose)

highest_id = since.get_since_id(sql)

tagsearch, magic_tags = sql.magic_hashtags()

tweet_list = twapi.all_relevant_tweets(highest_id, tagsearch)
for id, tweet in tweet_list.items():
    if args.verbose > 1:
        print(tweet)
    # exclude some tweets:
    if tweet.author().screen_name == twapi.myself.screen_name:
        if args.verbose > 2:
            print("Not replying to my own tweets")
            print("=================")
        continue
    if tweet.is_retweet():
        if args.verbose > 1:
            print("Not processing pure retweets")
            print("=================")
        continue
    # handle #folgenbitte and #entfolgen and possibly other meta commands, but
    # only for explicit mentions.
    if tweet.is_explicit_mention(twapi.myself):
        if args.verbose > 3:
            print("Tweet explicitly mentions me")
        react.process_commands(tweet, twapi, args.verbose)
    if tweet.has_hashtag(magic_tags):
        if args.verbose > 3:
            print("Tweet has magic hashtag")
    # Process this tweet
    mode = None
    if tweet.is_explicit_mention(twapi.myself) or tweet.has_hashtag(magic_tags):
        mode = 'all'
    react.process_tweet(tweet, twapi, sql, args.verbose, magic_tags, mode)
    # Process quoted or replied-to tweets, only for explicit mentions and magic tags
    if tweet.is_explicit_mention(twapi.myself) or tweet.has_hashtag(magic_tags):
        for other_id in tweet.quoted_status_id(), tweet.in_reply_id():
            if (args.verbose > 2 and not other_id is None) or args.verbose > 3:
                print("Looking for other tweet", other_id)
                if other_id in tweet_list:
                    print("...already in tweet_list")
            if (not other_id is None) and other_id not in tweet_list:
                other_tweet = twapi.get_tweet(other_id)
                if other_tweet is None:
                    continue
                # don't process the other tweet if we should have seen it before (this
                # also prevents recursion via this branch):
                if other_tweet.is_mention(twapi.myself):
                    if args.verbose > 1:
                        print("Not processing other tweet because it already mentions me")
                        print("=================")
                if other_tweet.has_hashtag(magic_tags):
                    if args.verbose > 1:
                        print("Not processing other tweet because it already has the magic hashtag")
                        print("=================")
                else:
                    if args.verbose > 2:
                        print("Processing tweet {} mode {}:".format(tweet.id, modus))
                        print(tweet)
                    react.process_tweet(other_tweet, twapi,
                        sql, args.verbose, magic_tags,
                        modus='all'
                            if tweet.is_explicit_mention(twapi.myself)
                            else None)
    print("█"*80 + '\n')

git.store_version(sql)
if tweet_list:
    since.store_since_id(sql, max(tweet_list.keys()))

sql.close_sucessfully()
