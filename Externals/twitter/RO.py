# pylint: disable=C0114

import log
from Externals.twitter.Api import TwitterBase as BaseApi
log_ = log.getLogger(__name__)

class ReadOnly(BaseApi):
    # pylint: disable=R0903
    def __init__(self):
        super().__init__()
        log_.setLevel(log_.getEffectiveLevel() - 10)
        log_.info(
            'Running from readonly twitter API (read real tweets, do not actually post answers)')
