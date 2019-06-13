#!/usr/bin/python3

import answer
import credentials
import gitdescribe as git
import since

import argparse
import datetime
import sqlite3
import sys
import tweepy

def print_rate_limit(api):
    rls = api.rate_limit_status()
    print("Rate limit:")
    for r in rls['resources']:
        for l in rls['resources'][r]:
            if rls['resources'][r][l]['limit'] != rls['resources'][r][l]['remaining']:
                print(l, rls['resources'][r][l]['limit'], rls['resources'][r][l]['remaining'])

def print_tweet_object(tweet):
    for k in vars(tweet):
        print(k, vars(tweet)[k])

def process_tweet(tweet, api, sqlcursor, readwrite, modus):
    if tweet.author.screen_name == '_ds_100':
        print("Not replying to my own tweets")
    twcounter = 1
    for reply in answer.compose_answer(tweet.full_text, sqlcursor, readwrite, modus):
        try:
            if readwrite:
                api.update_status(reply,
                                  in_reply_to_status_id=tweet.id,
                                  auto_populate_reply_metadata=True
                                 )
            else:
                print("NOT TWEETING:")
            print ("Tweet {} ({} chars):".format(twcounter, len(reply)))
            print (reply)
            print ("-----------------")
            twcounter += 1
        except tweepy.TweepError as twerror:
            print("Error {} tweeting {}: {}".format(twerror.api_code, tweet.in_reply_to_status_id, twerror.reason))


parser = argparse.ArgumentParser(description="""
        Bot zur DS100-Expansion auf Twitter
        """)
parser.add_argument('--readwrite',
                    dest='rw',
                    help='Do tweet or alter database',
                    required=False,
                    action='store_true',
                    default=False)
args = parser.parse_args()
readwrite = args.rw

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
for tweet in tweepy.Cursor(api.search,
                           q='#DS100',
                           tweet_mode='extended',
                           since_id=highest_id
                          ).items():
    if tweet.id in seen_ids:
        continue
    seen_ids[tweet.id] = 1
    process_tweet(tweet, api, sqlcursor, readwrite, 'hashtag')
for tweet in tweepy.Cursor(api.mentions_timeline,
                           tweet_mode='extended',
                           since_id=highest_id
                          ).items():
    if tweet.id in seen_ids:
        continue
    seen_ids[tweet.id] = 1
    if tweet.author.screen_name == '_ds_100':
        print("Not processing my own tweets")
        continue
    process_tweet(tweet, api, sqlcursor, readwrite, 'mention')
    if 'quoted_status_id' in vars(tweet) and tweet.quoted_status_id not in seen_ids:
        print("Processing quoted Tweet")
        seen_ids[tweet.quoted_status_id] = 1
        try:
            quoted_tweet = api.get_status(tweet.quoted_status_id,
                tweet_mode='extended')
            process_tweet(quoted_tweet, api, sqlcursor, readwrite, 'quoted')
        except tweepy.TweepError as twerror:
            print("Error {} receiving quoted tweet {}: {}".format(twerror.api_code, tweet.quoted_status_id, twerror.reason))
    if tweet.in_reply_to_status_id != None and tweet.in_reply_to_status_id not in seen_ids:
        print("Processing referenced Tweet")
        seen_ids[tweet.in_reply_to_status_id] = 1
        try:
            referenced_tweet = api.get_status(tweet.in_reply_to_status_id,
                tweet_mode='extended')
            process_tweet(referenced_tweet, api, sqlcursor, readwrite, 'referenced')
        except tweepy.TweepError as twerror:
            print("Error {} receiving referenced tweet {}: {}".format(twerror.api_code, tweet.in_reply_to_status_id, twerror.reason))

highest_id = max(seen_ids.keys())

if readwrite:
    git.store_version(sqlcursor)
    since.store_since_id(sqlcursor, highest_id)

sqlcursor.close()
sql.commit()
sql.close()
print_rate_limit(api)
