"""Represents a row of abbreviation data"""

from AnswerMachine.react import find_tokens
from .error import DataError

class Row:
    def normalize(self, contents, col):
        try:
            return ' '.join(contents[self.cols[col]].split())
        except AttributeError as ae:
            raise DataError(str(ae))

    # pylint: disable=R0903
    def __init__(self, iterator, cols, nolink, filters):
        self.cols = cols
        for c in ('short', 'long'):
            if self.cols[c] not in iterator['next']:
                msg = "Column {} ({}) not in contents".format(self.cols[c], c)
                raise DataError(msg)
        self.abbr = self.split(iterator)
        self.long = self.normalize(iterator['next'], 'long')
        self.add = None
        if self.cols['add'] is not None and self.cols['add'] in iterator['next']:
            self.add = iterator['next'][self.cols['add']]
        if nolink:
            self.long = self.long.replace('.', '\u2024')
        self.valid = False
        if self.abbr == "":
            return # invalid
        self.apply_filters(filters, iterator['next'])
        if self.valid:
            self.check_abbreviation()

    def apply_filters(self, filters, data):
        self.filters = filters
        if len(self.filters) == 0:
            # no filters: everything valid
            self.valid = True
        for f in self.filters:
            if f['col'] not in data:
                self.valid = False
                continue
            string = data[f['col']]
            if (string is None) == f['empty']:
                self.valid = True
                continue
            if (string == "") == f['empty']:
                self.valid = True
                continue
            if f['contains'] in string:
                self.valid = True
                continue

    def split(self, iterator):
        short = self.normalize(iterator['next'], 'short')
        if iterator['split'] is not None:
            abbrs = short.split(iterator['split'])
            short = abbrs[iterator['index']]
            self.abbr_index = iterator['index'] + 1
            if self.abbr_index == len(abbrs):
                self.abbr_index = 0
        else:
            self.abbr_index = 0
        return short

    def check_abbreviation(self):
        candidates = find_tokens('#' + self.abbr.replace(' ', '_'), '', '')
        if len(candidates) != 1:
            self.valid = False
            msg = "Abbreviation {} will not be matched".format(self.abbr)
            raise DataError(msg)
        if candidates[0].abbr != self.abbr:
            self.valid = False
            msg = "Abbreviation {} will be falsely matched as {}".format(self.abbr,
                candidates[0].abbr)
            raise DataError(msg)

    def next_index(self):
        return self.abbr_index

    def __str__(self):
        return str(self.__dict__)
