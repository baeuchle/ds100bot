"""Represents a row of abbreviation data"""

from .error import DataError

class Row:
    def normalize(self, contents, col):
        return ' '.join(contents[self.cols[col]].split())

    # pylint: disable=R0903
    def __init__(self, contents, cols, nolink, filters):
        self.cols = cols
        for c in ('short', 'long'):
            if self.cols[c] not in contents:
                msg = "Column {} ({}) not in contents".format(self.cols[c], c)
                raise DataError(msg)
        self.abbr = self.normalize(contents, 'short')
        self.long = self.normalize(contents, 'long')
        self.add = None
        if self.cols['add'] is not None and self.cols['add'] in contents:
            self.add = contents[self.cols['add']]
        if nolink:
            self.long = self.long.replace('.', '\u2024')
        self.valid = False
        if self.abbr == "":
            return # invalid
        self.filters = filters
        if len(self.filters) == 0:
            # no filters: everything valid
            self.valid = True
        for f in self.filters:
            if f['col'] not in contents:
                self.valid = False
                continue
            string = contents[f['col']]
            if (string is None) == f['empty']:
                self.valid = True
                continue
            if (string == "") == f['empty']:
                self.valid = True
                continue
            if f['contains'] in string:
                self.valid = True
                continue

    def __str__(self):
        return str(self.__dict__)
