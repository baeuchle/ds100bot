"""This module contains all functions that make the bot remember things"""

import logging

from .gitdescribe import notify_new_version, store_version
from .since import store_since_id, get_since_id

def init_logger(name='bot'):
    logger = logging.getLogger(name)
    botformat = logging.Formatter(
        fmt="%(levelname)-8s %(name)s %(message)s"
    )
    streamhdl = logging.StreamHandler()
    streamhdl.setFormatter(botformat)
    logger.addHandler(streamhdl)
    return logger

def set_logging_args(parser, default_lvl='CRITICAL'):
    levels = "DEBUG INFO WARNING ERROR CRITICAL".split()
    parser.add_argument('--log-level',
                        help='Set logging level',
                        required=False,
                        default=default_lvl,
                        choices=levels)
