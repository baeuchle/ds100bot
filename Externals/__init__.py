"""External APIs"""

from collections import namedtuple
from .database import Database
from .twitter.Api import TwitterBase
from .twitter.RO import ReadOnly as TwitterReadOnly
from .twitter.RW import ReadWrite as TwitterReadWrite

def get_externals(**kwargs):
    api = namedtuple('Externals', ['twitter', 'database'])
    default_mode = kwargs.get('mode', 'readonly')
    api.twitter = get_twitter_object(kwargs.get('twmode', default_mode))
    api.database = get_database_object(kwargs.get('dbmode', default_mode))
    return api

def get_twitter_object(mode):
    if mode == "readonly":
        return TwitterReadOnly()
    if mode == "readwrite":
        return TwitterReadWrite()
    if mode == 'none':
        return None
    raise ValueError('Unsupported Twitter API {}'.format(mode))

def get_database_object(mode):
    return Database(mode)
