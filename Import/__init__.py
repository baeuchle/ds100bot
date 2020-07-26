"""Importing data from JSON/CSV into Database"""

import Persistence.log as log
from .sourceconfig import SourceConfig
from .error import SourceError, JsonError, DataError
log_ = log.getLogger(__name__)

def find_all_configs(directory):
    configurations = {}
    data_lists = {}
    for f in directory.glob('*.json'):
        config = None
        try:
            config = SourceConfig(f)
        except SourceError as se:
            log_.critical("Error reading configuation file %s: %s", f, str(se))
            return None
        if config.id in configurations:
            log_.critical("Source %s specified twice: in %s and in %s",
                config.id, configurations[config.id].file, f)
            return None
        for dl in config.data_list:
            if dl.id in data_lists:
                log_.critical("Data list %s specified twice: in %s and in %s",
                    dl.id, data_lists[dl.id], f)
                return None
            data_lists[dl.id] = config.file
        configurations[config.id] = config
    return configurations
