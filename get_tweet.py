#!/usr/bin/python3

import argparse
import pprint
from textwrap import dedent
from urllib.parse import urlparse
from pathlib import Path
import api

def print_tweet_details(tw, target):
    quoted_status_id = None
    ext = ''
    if 'quoted_status_id' in tw.__dict__:
        quoted_status_id = tw.quoted_status_id
    if 'extended_entities' in tw.__dict__:
        ext = 'extended_entities=\n{},'.format(pp.pformat(tw.extended_entities))
    print(dedent('''\
    list_of_tweets.append(Tweet(TweepyMock(
        full_text={},
        id={},
        display_text_range={},
        in_reply_to_user_id={},
        in_reply_to_status_id={},
        in_reply_to_screen_name={},
        quoted_status_id={},
        entities=
            {},
        {}
        user=User(
            screen_name={},
            name={},
            id={},
            follows={}
        )
        ), 8))
    ''').format(
        repr(tw.full_text),
        repr(tw.id),
        pp.pformat(tw.display_text_range),
        repr(tw.in_reply_to_user_id),
        repr(tw.in_reply_to_status_id),
        repr(tw.in_reply_to_screen_name),
        repr(quoted_status_id),
        pp.pformat(tw.entities),
        ext,
        repr(tw.user.screen_name),
        repr(tw.user.name),
        repr(tw.user.id),
        repr(twapi.is_followed(tw.user))
    ), file=target)

parser = argparse.ArgumentParser(description='Helper program for dumping tweet details')
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('--id',
                   dest='id',
                   help='ID of the tweet that will be downloaded',
                   type=int,
                   required=False,
                   action='store'
                   )
group.add_argument('--url',
                   dest='url',
                   help='URL of the tweet that will be downloaded',
                   type=str,
                   required=False,
                   action='store'
                   )
parser.add_argument('--mode',
                    dest='mode',
                    choices=['dump', 'mock'],
                    help=dedent('''\
                    dump: Just dump the tweet and be done with it.
                    mock: Prepare TweepyMock objects from this tweet and
                          referenced tweets that can be used in test cases.
                    '''),
                    required=False,
                    default='mock',
                    action='store'
                   )
args = parser.parse_args()

twapi = api.get_api_object('readonly')

tid = args.id
if tid is None:
    try:
        tid = int(Path(urlparse(args.url).path).name)
    except:
        parser.error("Cannot extract tweet id from URL {}".format(args.url))
tweet = twapi.get_tweet(tid)

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
        '''), file=target)
        print_tweet_details(tweet.original, target)
        if tweet.original.in_reply_to_status_id is not None:
            replied_to_tweet = twapi.get_tweet(tweet.original.in_reply_to_status_id)
            print_tweet_details(replied_to_tweet.original, target)
        if 'quoted_status_id' in tweet.original.__dict__:
            if tweet.original.quoted_status_id is not None:
                quoted_tweet = twapi.get_tweet(tweet.original.quoted_status_id)
                print_tweet_details(quoted_tweet.original, target)
