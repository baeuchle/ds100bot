#!/usr/bin/python3

import answer
import credentials
import gitdescribe
import since

import argparse
import datetime
import sqlite3
import sys
import tweepy

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
if not gitdescribe.is_same_version(sqlcursor):
    print("version has changed:",
        gitdescribe.get_last_version(sqlcursor),
        gitdescribe.get_version())
    if readwrite:
        api.update_status("Ich twittere nun von Version {}".format(gitdescribe.get_version()))

highest_id = since.get_since_id(sqlcursor)
for tweet in tweepy.Cursor(api.search,
                           q='#DS100',
                           tweet_mode='extended',
                           since_id=highest_id
                          ).items(100):
    print (tweet.full_text)
    highest_id = max(highest_id, tweet.id)
    twcounter = 1
    for reply in answer.compose_answer(tweet.full_text, sqlcursor, readwrite):
        try:
            if readwrite:
                api.update_status(reply,
                                  in_reply_to_status_id=tweet.id,
                                  auto_populate_reply_metadata=True
                                 )
            else:
                print("NOT TWEETING:")
            print ("Tweet {}:".format(twcounter))
            print (reply)
            print ("-----------------")
            twcounter += 1
        except:
            print("Not tweeting reply")

if readwrite:
    gitdescribe.store_version(sqlcursor)
    since.store_since_id(sqlcursor, highest_id)

sqlcursor.close()
sql.commit()
sql.close()
