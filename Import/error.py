"""Exception classes for imports"""

class SourceError(Exception):
    pass

class JsonError(SourceError):
    pass

class DataError(SourceError):
    pass
