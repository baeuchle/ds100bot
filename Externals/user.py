"""Abstraction of social media users"""

from urllib.parse import urlparse

class User:
    def __init__(self, name, uid, host):
        self._name = name
        self._id = uid
        self._host = host

    @property
    def host(self):
        return self._host

    def __str__(self):
        return self._name

    def __int__(self):
        return self._id

    def __eq__(self, rhs):
        return str(self) == str(rhs)

def fromTwitterUser(twuser):
    return User(twuser.screen_name, twuser.id, 'twitter.com')

def fromMastodonUser(mastuser):
    authorurl = urlparse(mastuser.url)
    return User(mastuser.acct, mastuser.id, authorurl.hostname)
