"""Unit tests for AnswerMachine.react.process_commands"""

import logging

from Externals.message import Message
from Externals.network import Network
from AnswerMachine.react import process_commands

log = logging.getLogger('test')

class MockApi(Network): # pylint: disable=abstract-method
    def __init__(self, willfollow, willdefollow):
        self.willdefollow = willdefollow
        self.willfollow = willfollow

    def is_followed(self, author): # pylint: disable=no-self-use
        log.critical(author)
        return author == "follows"

    def follow(self, _):
        assert self.willfollow

    def defollow(self, _):
        assert self.willdefollow

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
