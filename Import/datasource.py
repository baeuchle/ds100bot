"""Abstracts a data source configuration"""

import csv
import Persistence.log as log
from .error import DataError, JsonError
from .row import Row
log_ = log.getLogger(__name__, fmt='{name}:{levelname} {message}')

class DataSource:
    _mandatory_fields = (
        "file",
        "long",
        "short"
    )

    def __init__(self, config_dict, complete_dict):
        self.config = config_dict
        self.id = self.config.get('id', complete_dict.get('id', None))
        for mf in DataSource._mandatory_fields:
            if mf not in config_dict:
                msg = "Key {} missing".format(mf)
                raise JsonError(msg)
        if self.id is None:
            raise JsonError("Key id neither in top level nor data::id")
        handle = open(self.config['file'])
        self.reader = csv.DictReader(handle, delimiter=self.config.get('delim', ';'))
        self.cols = {
            'short': self.config['short'],
            'long': self.config['long'],
            'add': self.config.get('add', None)
        }
        self.iter = None
        self.nolink = self.config.get('nolink', False)
        self.filters = self.config.get('filter', [])

    def __iter__(self):
        self.iter = self.reader.__iter__()
        return self

    def __next__(self):
        row = None
        while True:
            ni = self.iter.__next__()
            try:
                row = Row(ni, self.cols, self.nolink, self.filters)
                if row.valid:
                    break
            except DataError as de:
                de.args = ['{}: {}'.format(self.getPosition(), de.args[0])]
                raise
        return row

    def getLineNum(self):
        return self.reader.line_num

    def getPosition(self):
        return "{}::{}".format(self.config['file'], self.line_num)

    line_num = property(getLineNum)
    position = property(getPosition)
