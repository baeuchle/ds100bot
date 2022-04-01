# pylint: disable=C0114

import json
import re
import unicodedata

class Measure:
    def __init__(self):
        self.next_separator = {
            '\u200b': '\n',
            '\n': '\t',
            '\t': ' ',
            ' ': ''
        }
        self.replaced_separator = {
            '\u200b': '',
        }

    def split(self, text, orig_status, separator='\u200b'):
        # msg candidates have zero-width space where they may be split sensibly:
        possible_parts = text.split(separator)
        status_list = []
        text_so_far = ""
        for part in possible_parts:
            if not self.is_short_enough(part):
                # next part is too big: put into its own tweet, separated with next
                # separator.
                if len(text_so_far.strip()) > 0:
                    status_list.append(text_so_far.strip())
                    text_so_far = ""
                status_list.extend(self.split(part, orig_status, self.next_separator[separator]))
                continue
            if not self.is_short_enough(text_so_far, part,
                                        self.replaced_separator.get(separator, separator)):
                # next part makes this too big: go on with what we have.
                if len(text_so_far.strip()) > 0:
                    status_list.append(text_so_far.strip())
                    text_so_far = ""
            text_so_far += self.replaced_separator.get(separator, separator) + part
        if len(text_so_far.strip()) > 0:
            status_list.append(text_so_far.strip())
        return status_list

    def is_short_enough(self, *args):
        return self.measure_message_length(''.join(args)) <= 0

    def measure_message_length(self, text):
        raise NotImplementedError()

class MeasureToot(Measure):
    def __init__(self):
        super().__init__()
        # Mastodon allows 500 characters, but counts mentions. Since in replies, these are set
        # automatically, and extracting and measurig their lengths doesn't seem to be easily doable
        # here, we'll simply add a margin of error of 100 characters. This is still 120 characters
        # more than we'll have for Twitter :)
        self.length = 400
        self.link_length = 23

    def measure_message_length(self, text):
        normalized = unicodedata.normalize('NFC', text)
        normalized = re.sub(r"(https?://)?\w+\.\w+[\w\.]*(/[\w\.%]*[\w]+)*/?",
            " "*self.link_length,
            normalized)
        return len(normalized) - self.length

class MeasureTweet(Measure):
    def __init__(self):
        super().__init__()
        self.weight_config = {}
        with open('config/api_weights.json') as js:
            self.weight_config = json.load(js)
        if self.weight_config['emojiParsingEnabled']:
            self.emoji_flag_re = re.compile('[\U0001F1E6-\U0001F1FF]{2}')

    def measure_message_length(self, text):
        normalized = unicodedata.normalize('NFC', text)
        # this isn't the correct RE for twitter URLs, but
        # it should suffice for everything the bot generates.
        normalized = re.sub(r"(https?://)?\w+\.\w+[\w\.]*(/[\w\.%]*[\w]+)*/?",
            " "*self.weight_config['transformedURLLength'],
            normalized)
        total_weight = 0
        target = self.weight_config['maxWeightedTweetLength'] * self.weight_config['scale']
        if self.weight_config['emojiParsingEnabled']:
            # replace double-flag-letter-emoji by one flag-letter-emoji
            # (A, in this case)
            normalized = self.emoji_flag_re.sub('\U0001F1E6', normalized)
        for c in normalized:
            curr_weight = self.weight_config['defaultWeight']
            for r in self.weight_config['ranges']:
                if r['start'] <= ord(c) <= r['end']:
                    curr_weight = r['weight']
            total_weight += curr_weight
        return total_weight - target
