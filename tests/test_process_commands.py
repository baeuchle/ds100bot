"""Unit tests for AnswerMachine.react.process_commands"""

from Externals.tweet import Tweet as Message
from AnswerMachine.react import process_commands

class MockApi:
    def __init__(self, willfollow, willdefollow):
        self.willdefollow = willdefollow
        self.willfollow = willfollow

    def is_followed(self, author): # pylint: disable=no-self-use
        return author == "follows"

    def follow(self, _):
        assert self.willfollow

    def defollow(self, _):
        assert self.willdefollow

def test_nocommand():
    msg = Message(id=0, text="blabla", author=None, hashtag_texts=[])
    try:
        process_commands(msg, None)
    except AttributeError:
        assert False, "unprocessable Message needs API"

def test_folgenbitte_not_following():
    msg =  Message(id=0, text="blabla", author="followsnot", hashtag_texts=['folgenbitte'])
    process_commands(msg, MockApi(True, False))

def test_folgenbitte_following():
    msg =  Message(id=0, text="blabla", author="follows", hashtag_texts=['folgenbitte'])
    process_commands(msg, MockApi(False, False))

def test_entfolgen_not_following():
    msg =  Message(id=0, text="blabla", author="followsnot", hashtag_texts=['entfolgen'])
    process_commands(msg, MockApi(False, False))

def test_entfolgen_following():
    msg =  Message(id=0, text="blabla", author="follows", hashtag_texts=['entfolgen'])
    process_commands(msg, MockApi(False, True))

def test_both_following():
    msg =  Message(id=0, text="blabla", author="follows",
            hashtag_texts=['folgenbitte', 'entfolgen'])
    process_commands(msg, MockApi(False, True))

def test_both_not_following():
    msg =  Message(id=0, text="blabla", author="followsnot",
            hashtag_texts=['entfolgen', 'folgenbitte'])
    process_commands(msg, MockApi(True, True))
