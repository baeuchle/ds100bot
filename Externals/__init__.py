"""External APIs"""

from .database import setup_database
from .network import set_arguments
from .network import test_network_arguments
from .network import Network
from .mastodon import make_mastodon

def setup_network(_, args, highest_ids):
    return make_mastodon(args, highest_ids)
