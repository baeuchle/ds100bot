# pylint: disable=C0114

import json
import re
import unicodedata

weight_config = {}
with open('config/api_weights.json') as js:
    weight_config = json.load(js)
        
def measure_tweet_length(text):
    normalized = unicodedata.normalize('NFC', text)
    # this isn't the correct RE for twitter URLs, but
    # it should suffice for everything the bot generates.
    normalized = re.sub(r"(https?://)?\w+\.\w+[\w\.]*(/[\w\.%]*[\w]+)*/?",
        " "*weight_config['transformedURLLength'],
        normalized)
    total_weight = 0
    target = weight_config['maxWeightedTweetLength'] * weight_config['scale']
    for c in normalized:
        curr_weight = weight_config['defaultWeight']
        for r in weight_config['ranges']:
            if r['start'] <= ord(c) <= r['end']:
                curr_weight = r['weight']
        total_weight += curr_weight
    return total_weight - target

def is_short_enough(text):
    return measure_tweet_length(text) <= 0

next_separator = {
    '\u200b': '\n',
    '\n': '\t',
    '\t': ' ',
    ' ': ''
    }
replaced_separator = {
    '\u200b': '',
    }

def split_text(text, separator='\u200b'):
    # tweet candidates have zero-width space where they may be split sensibly:
    possible_parts = text.split(separator)
    status_list = []
    text_so_far = ""
    for part in possible_parts:
        if not is_short_enough(part):
            # next part is too big: put into its own tweet, separated with next
            # separator.
            if len(text_so_far) > 0:
                status_list.append(text_so_far)
                text_so_far = ""
            status_list.extend(split_text(part, next_separator[separator]))
            continue
        if not is_short_enough(text_so_far + part + replaced_separator.get(separator, separator)):
            # next part makes this too big: go on with what we have.
            if len(text_so_far) > 0:
                status_list.append(text_so_far)
                text_so_far = ""
        text_so_far += replaced_separator.get(separator, separator) + part
    if len(text_so_far) > 0:
        status_list.append(text_so_far)
    return status_list
