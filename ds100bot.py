#!/usr/bin/python3

"""Twitter-Bot für die Expansion von DS100-Abkürzungen und ähnlichen Abkürzungslisten"""

import argparse

from AnswerMachine import handle_list
from Externals import get_externals
import Persistence
import Persistence.log as log

def arguments():
    parser = argparse.ArgumentParser(description=__doc__)
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
    args_ = parser.parse_args()
    if args_.db is None:
        if args_.rw:
            args_.db = 'readwrite'
        else:
            args_.db = 'readonly'
    if args_.api is None:
        if args_.rw:
            args_.api = 'readwrite'
        else:
            args_.api = 'readonly'
    if args_.verbose is None:
        args_.verbose = 0
    args_.verbose = 50 - args_.verbose * 10
    return args_

def setup_log(loglvl):
    if loglvl <= 0:
        loglvl = 1

    log.basicConfig(level=loglvl, style='{')
    return log.getLogger('ds100')

def setup_apis(args_):
    api_ = get_externals(twmode=args_.api, dbmode=args_.db)
    Persistence.notify_new_version(api_)
    return api_

def teardown_apis(api_, apiname, max_id_=0):
    Persistence.store_version(api_.database)
    if max_id > 0:
        Persistence.store_since_id(api_.database, max_id_)
    if apiname == 'mock':
        api_.twitter.statistics()
    api_.database.close_sucessfully()
    log_.info("Bot finished")

if __name__ == "__main__":
    args = arguments()
    log_ = setup_log(args.verbose)
    api = setup_apis(args)

    tagsearch, magic_tags = api.database.magic_hashtags()
    max_id = handle_list(api.twitter.all_relevant_tweets(
                            Persistence.get_since_id(api.database), tagsearch
                         ), apis=api, magic_tags=magic_tags)
    teardown_apis(api, args.api, max_id)
