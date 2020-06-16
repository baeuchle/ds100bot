import logging

# we wrap logging because I want more control in getLogger.

def getLogger(name, fmt=None):
    log_ = logging.getLogger(name)
    if fmt is not None:
        fm_ = logging.Formatter(fmt=fmt, style='{')
        lh_ = logging.StreamHandler()
        lh_.setFormatter(fm_)
        log_.addHandler(lh_)
        log_.propagate = False
    return log_

def basicConfig(*args, **kwargs):
    logging.basicConfig(*args, **kwargs)

from logging import DEBUG, INFO, WARNING, ERROR, CRITICAL
