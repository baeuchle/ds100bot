#!/usr/bin/python3

"""Tester for the bot"""

import argparse

from AnswerMachine import handle_list
from Externals import get_externals
import Mock
import Persistence.log as log

def arguments():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verbose', '-v',
                        dest='verbose',
                        help='Output lots of stuff',
                        required=False,
                        action='count')
    parser.add_argument('--external',
                        dest='external',
                        help='''Read mocked tweet objects not from the internal
                        list, but from tweet_details.py. That file may be created with
                        get_tweet.py.''',
                        required=False,
                        action='store_true',
                        default=False
                       )
    parser.add_argument('--parse_one',
                        dest='parse_one',
                        help='Parse only mocked tweet with this ID',
                        required=False,
                        action='store',
                        default=None
                       )
    args_ = parser.parse_args()
    if args_.verbose is None:
        args_.verbose = 0
    args_.verbose = 50 - args_.verbose * 10
    return args_

def setup_log(loglvl):
    if loglvl <= 0:
        loglvl = 1

    log.basicConfig(level=loglvl, style='{')
    return log.getLogger('test_ds100')

def setup_apis():
    api_ = get_externals(twmode='none', dbmode='readonly')
    api_.twitter = Mock.MockApi()
    return api_

if __name__ == "__main__":
    args = arguments()
    log_ = setup_log(args.verbose)
    api = setup_apis()

    tagsearch, magic_tags = api.database.magic_hashtags()
    max_id = handle_list(api.twitter.all_relevant_tweets(
                            0, tagsearch
                         ), apis=api, magic_tags=magic_tags)
    api.twitter.statistics()
