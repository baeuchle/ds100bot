"""Unit tests for AnswerMachine.react.process_magic"""

from AnswerMachine.react import process_magic

def test_empty():
    assert process_magic([], 13, 'DEFAULT') == [['DEFAULT', [0, 0]], ['__', [13, 13]]]

def test_movetostart():
    inp = [
        ['ASDF', [3, 6]],
    ]
    out = [*inp, ['__', [15, 15]]]
    assert process_magic(inp, 15, 'D') == out

def test_keeporder():
    inp = [
        ['ASDF', [0, 6]],
        ['DDDD', [9, 6]],
        ['ASDF', [0, 5]],
        ['AAAA', [0, 8]],
        ['ERTF', [4, 2]],
    ]
    out = [*inp, ['__', [20, 20]]]
    assert process_magic(inp, 20, 'D') == out
