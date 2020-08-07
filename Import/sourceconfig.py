#!/usr/bin/python3

"""Read source configuation"""

import json
import Persistence.log as log
from .access import Access
from .datasource import DataSource
from .error import JsonError
log_ = log.getLogger(__name__, fmt='{name}:{levelname} {message}')

class SourceConfig:
    # pylint: disable=R0903
    # pylint: disable=R0902
    _mandatory_fields = (
        'access',
        'data',
        'id',
        'magic_hashtags'
    )

    def __init__(self, filepath):
        self.file = filepath
        with self.file.open() as jsonfile:
            try:
                self.json = json.load(jsonfile)
            except json.JSONDecodeError as jde:
                msg = "{}::{}::{}: JSON object could not be decoded: {}".format(
                    self.file, jde.lineno, jde.colno, jde.msg)
                raise JsonError(msg)
        for mf in SourceConfig._mandatory_fields:
            if mf not in self.json:
                msg = "Key {} missing".format(mf)
                raise JsonError(msg)
        self.access = [Access(a) for a in self.json['access']]
        self.magic_hashtags = self.json['magic_hashtags']
        self.data_list = [DataSource(d, self.json) for d in self.json['data']]
        self.id = self.json['id']
        self.head = self.json.get("headline", self.json.get("description", self.id))
        self.desc = self.json.get("description", "")
