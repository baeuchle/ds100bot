"""External APIs"""

from .database import setup_database
from .network import set_arguments
from .network import test_network_arguments
from .network import Network
from .twitter import make_twapi as setup_twitter
from .mastodon import make_mastodon

def setup_network(name, args, highest_ids):
    if name == 'twitter':
        return setup_twitter(args, highest_ids)
    return make_mastodon(args, highest_ids)
