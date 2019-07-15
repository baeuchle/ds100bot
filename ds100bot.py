#!/usr/bin/python3

import answer
import api
import gitdescribe as git
import react
import since

import argparse
import sqlite3
import sys

def process_tweet(tweet, twapi, sqlcursor, readwrite, modus=None):
    if verbose > 2:
        print("Processing tweet {}:".format(tweet.id))
        print(tweet)
        print("+++++++++++++++++")
    reply_id = tweet.id
    twcounter = 1
    for reply in answer.compose_answer(tweet.text, sqlcursor, readwrite, verbose, modus):
        if verbose > 0:
            print("I tweet {} ({} chars):".format(twcounter, len(reply)))
            print(reply)
        twcounter += 1
        if not readwrite:
            continue
        new_reply_id = twapi.tweet(reply,
                in_reply_to_status_id=reply_id,
                auto_populate_reply_metadata=True
            )
        if new_reply_id > 0:
            reply_id = new_reply_id
    if verbose > 2:
        if twcounter == 1:
            print("No expandable content found")
        print("=================")

parser = argparse.ArgumentParser(description="""
        Bot zur DS100-Expansion auf Twitter
        """)
parser.add_argument('--readwrite',
                    dest='rw',
                    help='Do tweet or alter database',
                    required=False,
                    action='store_true',
                    default=False)
parser.add_argument('--api',
                    dest='api',
                    help='Use given API: readwrite, readonly, mock',
                    required=False,
                    action='store',
                    default='readwrite')
parser.add_argument('--verbose', '-v',
                    dest='verbose',
                    help='Output lots of stuff',
                    required=False,
                    action='count')
args = parser.parse_args()
readwrite = args.rw
verbose = args.verbose
if verbose == None:
    verbose = 0

if not readwrite:
    print("READONLY mode: Not tweeting or changing the database")
if args.api != 'readwrite':
    print("API mode", args.api)

# setup twitter API
twapi = api.get_api_object(args.api, verbose)

# setup database
sql = sqlite3.connect('info.db')
sqlcursor = sql.cursor()
git.notify_new_version(sqlcursor, twapi, readwrite, verbose)

highest_id = since.get_since_id(sqlcursor)

tweet_list = twapi.all_relevant_tweets(highest_id, '#DS100')
for id, tweet in tweet_list.items():
    if verbose > 1:
        print(tweet)
    # exclude some tweets:
    if tweet.author().screen_name == twapi.myself.screen_name:
        if verbose > 2:
            print("Not replying to my own tweets")
            print("=================")
        continue
    if tweet.is_retweet():
        if verbose > 0:
            print("Not processing pure retweets")
            print("=================")
        continue
    # handle #folgenbitte and #entfolgen and possibly other meta commands, but
    # only for explicit mentions.
    if tweet.is_explicit_mention(twapi.myself):
        react.process_commands(tweet, twapi, readwrite, verbose)
    # Process this tweet
    process_tweet(tweet, twapi, sqlcursor, readwrite)
    # Process quoted or replied-to tweets, only for explicit mentions and #DS100.
    if tweet.is_explicit_mention(twapi.myself) or tweet.has_hashtag('DS100'):
        for other_id in tweet.quoted_status_id(), tweet.in_reply_id():
            if other_id != None and other_id not in tweet_list:
                other_tweet = twapi.get_tweet(other_id)
                if other_tweet == None:
                    continue
                # don't process the other tweet if we should have seen it before (this
                # also prevents recursion via this branch):
                if other_tweet.is_mention(twapi.myself):
                    if verbose > 1:
                        print("Not processing other tweet because it already mentions me")
                        print("=================")
                if other_tweet.has_hashtag('DS100'):
                    if verbose > 1:
                        print("Not processing other tweet because it already has the magic hashtag")
                        print("=================")
                else:
                    process_tweet(other_tweet, twapi, sqlcursor, readwrite)

if readwrite:
    git.store_version(sqlcursor)
    since.store_since_id(sqlcursor, max(tweet_list.keys()))

sqlcursor.close()
sql.commit()
sql.close()
