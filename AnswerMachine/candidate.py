"""Abstracts an abbreviation candidate"""

class Candidate:
    def __init__(self, parts, magic):
        if parts[0] is None or parts[0] == '':
            self.type_character = '#'
        else:
            self.type_character = parts[0]
        self.explicit_source = parts[1]
        self.abbr = parts[2]
        self.abbr = self.abbr[0] + self.abbr[1:].replace('_', ' ')
        self.abbr = ' '.join(self.abbr.split())
        self.magic_hashtag = magic

    def get_dict(self):
        return {
            'type_character': self.type_character,
            'explicit_source': self.explicit_source,
            'abbr': self.abbr,
            'magic_hashtag': self.magic_hashtag
        }

    def __str__(self):
        return str(self.get_dict())

    def __eq__(self, rhs):
        return self.__dict__ == rhs.__dict__
