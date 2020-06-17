#!/usr/bin/python3

import argparse
from collections import namedtuple
import log

import api as twitter_api
from database import Database
import gitdescribe as git
from handle_list import handle_list
import since

def arguments():
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
    return args

def setup_log(verbosity):
    loglvl = 50 - verbosity * 10
    if loglvl <= 0:
        loglvl = 1
    
    log.basicConfig(level=loglvl, style='{')
    return log.getLogger('ds100')

def setup_apis(args):
    api = namedtuple('Externals', ['twitter', 'database'])
    # setup twitter API
    api.twitter = twitter_api.get_api_object(args.api, external=args.external, parse_one=args.parse_one)
    # setup database
    api.database = Database(args.db)
    git.notify_new_version(api)
    return api

def teardown_apis(api, apiname, max_id=0):
    git.store_version(api.database)
    if max_id > 0:
        since.store_since_id(api.database, max_id)
    if apiname == 'mock':
        api.twitter.statistics()
    api.database.close_sucessfully()
    log_.info("Bot finished")

if __name__ == "__main__":
    args = arguments()
    log_ = setup_log(args.verbose)
    api = setup_apis(args)

    tagsearch, magic_tags = api.database.magic_hashtags()
    max_id = handle_list(api.twitter.all_relevant_tweets(
                            since.get_since_id(api.database), tagsearch
                         ), apis=api, magic_tags=magic_tags)
    teardown_apis(api, args.api, max_id)
