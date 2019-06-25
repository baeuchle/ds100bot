#!/usr/bin/python3

import answer
import credentials
import gitdescribe as git
import react
import since

import argparse
import datetime
import sqlite3
import sys
import tweepy

def print_rate_limit(api):
    rls = api.rate_limit_status()
    res = rls['resources']
    for r in res:
        rr = res[r]
        for l in res[r]:
            rrl = res[r][l]
            if rrl['limit'] != rrl['remaining'] and rrl['remaining'] < 5:
                print("Resource limit for {} low: {} of {} remaining".format(
                    l,
                    rrl['remaining'],
                    rrl['limit']
                ))

def print_tweet_object(tweet):
    global verbose
    if not verbose > 1:
        return
    for k in vars(tweet):
        if k[0] == '_':
            continue
        print(k, vars(tweet)[k])

def process_tweet(tweet, api, sqlcursor, readwrite, modus):
    if verbose > 0:
        print("Processing tweet {}:".format(tweet.id))
        print(tweet.full_text)
        print("+++++++++++++++++")
    if 'retweeted_status' in vars(tweet):
        print("Not replying to retweets")
        print_tweet_object(tweet)
        if verbose > 0:
            print("=================")
        return   
    if tweet.author.screen_name == '_ds_100':
        print("Not replying to my own tweets")
        print_tweet_object(tweet)
        if verbose > 0:
            print("=================")
        return
    print_tweet_object(tweet)
    reply_id = tweet.id
    twcounter = 1
    for reply in answer.compose_answer(tweet.full_text, sqlcursor, readwrite, modus):
        print("Tweet {} ({} chars):".format(twcounter, len(reply)))
        print(reply)
        twcounter += 1
        if not readwrite:
            continue
        try:
            new_tweet = api.update_status(reply,
                              in_reply_to_status_id=reply_id,
                              auto_populate_reply_metadata=True
                             )
            reply_id = new_tweet.id
        except tweepy.TweepError as twerror:
            print("Error {} tweeting {}: {}".format(twerror.api_code, tweet.in_reply_to_status_id, twerror.reason))
    if verbose > 0:
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

# setup twitter API
auth = tweepy.OAuthHandler(credentials.consumer_key, credentials.consumer_secret)
auth.set_access_token(credentials.access_token, credentials.access_token_secret)
api = tweepy.API(auth)

# setup database
sql = sqlite3.connect('info.db')
sqlcursor = sql.cursor()
git.notify_new_version(sqlcursor, api, readwrite)

highest_id = since.get_since_id(sqlcursor)
seen_ids = {}
seen_ids[highest_id] = 1

if verbose > 0:
    print("####### Processing mentions")
for tweet in tweepy.Cursor(api.mentions_timeline,
                           tweet_mode='extended',
                           since_id=highest_id
                          ).items():
    if tweet.id in seen_ids:
        if verbose > 0:
            print("Have seen tweet {} already:\n{}".format(tweet.id, tweet.full_text))
        continue
    seen_ids[tweet.id] = 1
    react.process_commands(tweet, api, readwrite)
    process_tweet(tweet, api, sqlcursor, readwrite, 'mention')
    if tweet.author.screen_name == '_ds_100':
        print("Not processing my own tweets")
        continue
    # if this tweet quotes another, not-yet-seen tweet, process that quoted tweet.
    if 'quoted_status_id' in vars(tweet) and tweet.quoted_status_id not in seen_ids:
        if verbose > 0:
            print("Processing quoted tweet {}:\n{}".format(tweet.quoted_status_id, "?"))
        seen_ids[tweet.quoted_status_id] = 1
        try:
            quoted_tweet = api.get_status(tweet.quoted_status_id,
                tweet_mode='extended')
            print("Quoted is >>>{}<<<".format(quoted_tweet.full_text))
            process_tweet(quoted_tweet, api, sqlcursor, readwrite, 'quoted')
        except tweepy.TweepError as twerror:
            print("Error {} receiving quoted tweet {}: {}".format(twerror.api_code, tweet.quoted_status_id, twerror.reason))
            print("Quotee was >>>{}<<<".format(tweet.full_text))
    if tweet.in_reply_to_status_id != None and tweet.in_reply_to_status_id not in seen_ids:
        print("Processing referenced Tweet")
        seen_ids[tweet.in_reply_to_status_id] = 1
        try:
            referenced_tweet = api.get_status(tweet.in_reply_to_status_id,
                tweet_mode='extended')
            print("Referenced is >>>{}<<<".format(referenced_tweet.full_text))
            process_tweet(referenced_tweet, api, sqlcursor, readwrite, 'referenced')
        except tweepy.TweepError as twerror:
            print("Error {} receiving referenced tweet {}: {}".format(twerror.api_code, tweet.in_reply_to_status_id, twerror.reason))
            print("Referee was >>>{}<<<".format(tweet.full_text))
if verbose > 0:
    print("####### Processing timeline")
for tweet in tweepy.Cursor(api.home_timeline,
                           tweet_mode='extended',
                           since_id=highest_id
                           ).items():
    if tweet.id in seen_ids:
        if verbose > 0:
            print("Have seen tweet {} already:\n{}".format(tweet.id, tweet.full_text))
        continue
    seen_ids[tweet.id] = 1
    if tweet.author.screen_name == '_ds_100':
        print("Not processing my own tweets")
        continue
    process_tweet(tweet, api, sqlcursor, readwrite, 'timeline')
    

if verbose > 0:
    print("####### Processing #DS100-tweets")
for tweet in tweepy.Cursor(api.search,
                           q='#DS100',
                           tweet_mode='extended',
                           since_id=highest_id
                          ).items():
    if tweet.id in seen_ids:
        continue
    seen_ids[tweet.id] = 1
    process_tweet(tweet, api, sqlcursor, readwrite, 'hashtag')

highest_id = max(seen_ids.keys())

if readwrite:
    git.store_version(sqlcursor)
    since.store_since_id(sqlcursor, highest_id)

sqlcursor.close()
sql.commit()
sql.close()
print_rate_limit(api)
