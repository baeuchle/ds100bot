"""Network API"""

import logging
from sys import stderr
from urllib.parse import urlparse

logger = logging.getLogger('bot.api')
msg_logger = logging.getLogger('msg')
follog_ = logging.getLogger('followlog')

def set_arguments(parser):
    group = parser.add_argument_group('Network API', description='''
        Configure Twitter or Mastodon API. For twitter, use --application and --user; for mastodon,
        use --account only.

        All of these reference a section in the given config file containing the API keys.
    ''')
    group.add_argument('--config',
                        action='store',
                        help='path to configuration file',
                        required=True)
    group.add_argument('--readwrite',
                        action='store_true',
                        help="Don't send statuses, only read status.",
                        required=False)
    group.add_argument('--application',
                        action='store',
                        help='Name of the twitter application',
                        required=False)
    group.add_argument('--user',
                        action='store',
                        help='Name of the twitter user',
                        required=False)
    group.add_argument('--account',
                        action='store',
                        help='Mastodon account name',
                        required=False)

def get_hostname(base_url):
    url = urlparse(base_url)
    return url.hostname

def test_network_arguments(args):
    if args.account and (args.application or args.user):
        print("Error: Mixing mastodon and twitter arguments", file=stderr)
        raise SystemExit(1)
    if (args.application is None) != (args.user is None):
        print("Error: twitter arguments, but not both", file=stderr)
        raise SystemExit(1)
    if args.account:
        return args.config[args.account].pop('network',
                get_hostname(args.config[args.account]['api_base_url']))
    return 'twitter'

class Network:
    def __init__(self, readwrite, highest_ids, measure, from_function, myself):
        # pylint: disable=too-many-arguments
        self.readonly = not readwrite
        self.high_message = int(highest_ids.get('since_id', 0))
        self.from_function = from_function
        self.measure = measure
        self.myself = myself

    def handle_followrequest(self, message):
        author = message.author
        if self.is_followed(author):
            follog_.log(45, "folgenbitte from @%s: already following", str(author))
            return
        follog_.log(45, "folgenbitte from @%s: not yet following", str(author))
        self.follow(author)

    def handle_defollowrequest(self, message):
        author = message.author
        if not self.is_followed(author):
            follog_.log(45, "entfolgen from @%s: not even following yet", str(author))
            return
        follog_.log(45, "entfolgen from @%s: still following so far", str(author))
        self.defollow(author)

    def follow(self, _):
        raise NotImplementedError()

    def defollow(self, _):
        raise NotImplementedError()

    def is_followed(self, _):
        raise NotImplementedError()

    def report_user_magic_hashtag(self, message):
        msg = f"""Hallo!

Für dich benutze ich standardmäßig den Magic Hashtag {message.user_dmt}.

Mehr Informationen findest du unter https://ds100.frankfurtium.de/finde-listen.html."""
        self.post(msg, reply_to_status=message)
        follog_.log(45, "showdefault from @%s: %s", str(message.author), message.user_dmt)

    def post_single(self, text, **_): # pylint: disable=no-self-use
        """Actually posts text as a new status."""
        msg_logger.warning(text)
        return True

    def post(self, text, **kwargs):
        """Post text as status, possibly split up into several separate status items."""
        reply_to = None
        if 'reply_to_status' in kwargs:
            reply_to = kwargs.pop('reply_to_status').orig
        for part in self.measure.split(text, reply_to):
            reply_to = self.post_single(part, reply_to_status=reply_to, **kwargs)
            if not reply_to:
                return None
        return reply_to

    def all_relevant_status(self, mt_list):
        results = {}
        for tl in (self.mentions(),
                   self.timeline(),
                   self.hashtags(mt_list)):
            for t in tl:
                if t is None:
                    logger.error("Received None status")
                    continue
                if t.id in results:
                    logger.debug("Status %d already in results", t.id)
                    continue
                msg = self.from_function(t, self.myself)
                if msg.has_hashtag('NOBOT', case_sensitive=False):
                    logger.debug("Status %d has NOBOT", t.id)
                    continue
                results[msg.id] = msg
        if results:
            self.high_message = max(self.high_message, *results.keys())
        logger.info("found %d unique status worth looking into", len(results))
        return results

    def mentions(self):
        raise NotImplementedError()

    def timeline(self):
        raise NotImplementedError()

    def hashtags(self, mt_list):
        raise NotImplementedError()

    def get_status(self, status_id):
        raise NotImplementedError()

    def get_other_status(self, other_id, tlist):
        if not other_id:
            logger.debug("get_other_status with None")
            return None
        if other_id in tlist:
            logger.debug("get_other_status: other_id %d already in %s", other_id, str(tlist))
            return None
        logger.debug("Trying to get other status")
        msg = self.get_status(other_id)
        if not msg:
            return None
        return self.from_function(msg, self.myself)
