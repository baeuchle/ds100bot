"""Abstraction of social media users"""

class User:
    def __init__(self, name, uid):
        self._name = name
        self._id = uid

    def __str__(self):
        return self._name

    def __int__(self):
        return self._id

    def __eq__(self, rhs):
        return self._name == rhs._name

def fromTwitterUser(twuser):
    return User(twuser.screen_name, twuser.id)

def fromMastodonUser(mastuser):
    return User(mastuser.acct, mastuser.id)
