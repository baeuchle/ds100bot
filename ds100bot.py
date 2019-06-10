#!/usr/bin/python3

import answer
import credentials
import gitdescribe
import sqlite3
import sys
import datetime
import tweepy

# setup twitter API
auth = tweepy.OAuthHandler(credentials.consumer_key, credentials.consumer_secret)
auth.set_access_token(credentials.access_token, credentials.access_token_secret)
api = tweepy.API(auth)

# find tweets to answer
text = "Hallo hier ist ein ütf8-Test mit #_FF #_FFLF #_FKW #_FH #_FKOZ #_FKON #_HG #_FFLU #_FFS #_FW #_FFFFF #_AA #_RSI #_TS #_AA__G #_FF"

# setup database
sql = sqlite3.connect('info.db')
sqlcursor = sql.cursor()
if not gitdescribe.is_same_version(sqlcursor):
    print("version has changed:",
        gitdescribe.get_last_version(sqlcursor),
        gitdescribe.get_version())
    api.update_status("Ich twittere nun von Version {}".format(gitdescribe.get_version()))

for tweet in tweepy.Cursor(api.search,
                           q='#DS100',
                           tweet_mode='extended'
                          ).items(100):
    print (tweet.full_text)
    twcounter = 1
    for reply in answer.compose_answer(tweet.full_text, sqlcursor):
        try:
            api.update_status(reply,
                              in_reply_to_status_id=tweet.id,
                              auto_populate_reply_metadata=True
                             )
            print ("Tweet {}:".format(twcounter))
            print (reply)
            print ("-----------------")
            twcounter += 1
        except:
            pass

gitdescribe.store_version(sqlcursor)

sqlcursor.close()
sql.commit()
sql.close()
