"""Abstracts the source access information (explicit source and magic hashtag)"""

import Persistence.log as log
from .error import JsonError
log_ = log.getLogger(__name__, fmt='{name}:{levelname} {message}')

class Access:
    # pylint: disable=R0903
    _mandatory_fields = (
        'type',
        'm_hashtag',
        'x_source'
    )

    def __init__(self, config_dict):
        self.conf = config_dict
        for mf in Access._mandatory_fields:
            if mf not in config_dict:
                msg = "Key access::{} missing".format(mf)
                raise JsonError(msg)
        self.type = self.conf['type']
        self.magic_hashtag = self.conf['m_hashtag']
        self.explicit_source = self.conf['x_source']
