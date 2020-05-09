#!/usr/bin/python3

import api
import argparse
import pprint
from textwrap import dedent

parser = argparse.ArgumentParser(description='Helper program for dumping tweet details')
parser.add_argument('--id',
                    dest='id',
                    help='ID of the tweet that will be downloaded',
                    type=int,
                    required=True,
                    action='store'
                   )
parser.add_argument('--mode',
                    dest='mode',
                    choices=['dump', 'mock', 'recursive'],
                    required=False,
                    default='mock',
                    action='store'
                   )
args = parser.parse_args()

twapi = api.get_api_object('readonly', 1000)
tweet = twapi.get_tweet(args.id)

pp = pprint.PrettyPrinter(indent=2, width=80)
if args.mode == 'dump':
    # promote inner objects so that pretty print also prints them
    for key in ['user', 'author']:
        tweet.original.__dict__[key] = tweet.original.__dict__[key].__dict__['_json']
    del tweet.original.__dict__['_api']
    del tweet.original.__dict__['_json']
    print("tweetdict = ", end='')
    pp.pprint(tweet.original.__dict__)
else:
    with open('tweet_details.py', 'w') as target:
        print(dedent('''\
        import datetime
        from tweet import Tweet
        from tweet_mock import TweepyMock
        from tweet_mock import User
        list_of_tweets = []
        list_of_tweets.append(Tweet(TweepyMock(
            full_text={},
            id={},
            display_text_range={},
            in_reply_to_user_id={},
            in_reply_to_status_id={},
            in_reply_to_screen_name={},
            entities=
                {},
            user=User(
                screen_name={},
                name={},
                id={},
                follows={}
            )
            ), 8))
        ''').format(
            repr(tweet.original.full_text),
            repr(tweet.original.id),
            pp.pformat(tweet.original.display_text_range),
            repr(tweet.original.in_reply_to_status_id),
            repr(tweet.original.in_reply_to_user_id),
            repr(tweet.original.in_reply_to_screen_name),
            pp.pformat(tweet.original.entities),
            repr(tweet.original.user.screen_name),
            repr(tweet.original.user.name),
            repr(tweet.original.user.id),
            repr(twapi.is_followed(tweet.original.user))
        ), file=target)
