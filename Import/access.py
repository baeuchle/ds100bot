"""Abstracts the source access information (explicit source and magic hashtag)"""

import logging
from .error import JsonError
log_ = logging.getLogger('setup.' + __name__)

class Access:
    # pylint: disable=R0903
    _mandatory_fields = (
        'type',
        'x_source'
    )

    def __init__(self, config_dict):
        self.conf = config_dict
        for mf in Access._mandatory_fields:
            if mf not in config_dict:
                msg = "Key access::{} missing".format(mf)
                raise JsonError(msg)
        self.type = self.conf['type']
        self.explicit_source = self.conf['x_source']
