"""Unit tests for AnswerMachine.react.process_commands"""

from Externals.message import Message
from AnswerMachine.react import process_commands

class MockApi:
    def __init__(self, willask, willdeask):
        self.will_ask = willask
        self.will_deask = willdeask

    def handle_followrequest(self, _):
        assert self.will_ask

    def handle_defollowrequest(self, _):
        assert self.will_deask

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
    process_commands(msg, MockApi(True, False))

def test_entfolgen_not_following():
    msg =  Message(id=0, text="blabla", author="followsnot", hashtag_texts=['entfolgen'])
    process_commands(msg, MockApi(False, True))

def test_entfolgen_following():
    msg =  Message(id=0, text="blabla", author="follows", hashtag_texts=['entfolgen'])
    process_commands(msg, MockApi(False, True))

def test_both_following():
    msg =  Message(id=0, text="blabla", author="follows",
            hashtag_texts=['folgenbitte', 'entfolgen'])
    process_commands(msg, MockApi(True, True))

def test_both_not_following():
    msg =  Message(id=0, text="blabla", author="followsnot",
            hashtag_texts=['entfolgen', 'folgenbitte'])
    process_commands(msg, MockApi(True, True))
