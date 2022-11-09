"""Mastodon API including Command line argumentation"""

import logging
import mastodon
from mastodon.Mastodon import MastodonAPIError, MastodonNotFoundError

from Externals.Measure import MeasureToot
from .message import fromToot
from .network import Network
from .user import fromMastodonUser

logger = logging.getLogger('bot.api.mastodon')
msg_logger = logging.getLogger('msg')
follog_ = logging.getLogger('followlog')

def set_arguments(ap):
    group = ap.add_argument_group('Mastodon', description='Configure Mastodon API')
    group.add_argument('--config',
                        action='store',
                        help='path to configuration file',
                        required=True)
    group.add_argument('--account',
                        action='store',
                        help='Mastodon account name',
                        required=True)
    group.add_argument('--readwrite',
                        action='store_true',
                        help="Don't tweet, only read tweets.",
                        required=False)

class Mastodon(Network):
    def __init__(self, api, readwrite, highest_ids):
        self.api = api
        me_ = self.api.me()
        user = fromMastodonUser(me_)
        self.mode = 'global'
        self.public = ''
        for f in me_.fields:
            if f['name'] == 'botmode':
                self.mode = f['value']
            if f['name'] == 'publicuse':
                self.public = f['value']
        super().__init__(readwrite, highest_ids, MeasureToot(), fromToot, user)

    def post_single(self, text, **kwargs):
        # pylint: disable=too-many-return-statements
        if len(text) == 0:
            logger.error("Empty toot?")
            return None
        msg_logger.warning(text)
        if self.readonly:
            return None
        if 'reply_to_status' in kwargs:
            orig_tweet = kwargs.pop('reply_to_status')
            if orig_tweet:
                try:
                    return self.api.status_reply(orig_tweet, text)
                except MastodonAPIError:
                    logger.exception("Error while tooting reply >%s<", text)
                    text = text[:len(text//2)] + " THIS TOOT WAS TOO LONG cc @baeuchle@chaos.social"
                    logger.critical("Now re-trying with >%s<", text)
                    try:
                        return self.api.status_reply(orig_tweet, text)
                    except MastodonAPIError:
                        logger.exception("Second-level error while tooting reply")
        # not replying to anything:
        try:
            return self.api.status_post(text,
                    sensitive=False,
                    visibility='public',
                    **kwargs
                    )
        except MastodonAPIError:
            logger.exception("Error while tooting >%s<", text)
            text = text[:len(text//2)] + " THIS TOOT WAS TOO LONG cc @baeuchle@chaos.social"
            logger.critical("Now re-trying with >%s<", text)
            try:
                return self.api.status_post(text,
                        sensitive=False,
                        visibility='public',
                        **kwargs
                        )
            except MastodonAPIError:
                logger.exception("Second-level error while tooting")
        return None

    def handle_followrequest(self, message):
        if self.mode == 'global':
            return super().handle_followrequest(message)
        # in 'local' mode, only follow in same network:
        if message.author.host == self.myself.host:
            return super().handle_followrequest(message)
        # for other networks, toot at them.
        msg = f"""Hallo!

Ich folge nur lokalen Accounts des Netzwerks {self.myself.host}. Für Accounts außerhalb dieses
Netzwerkes steht der Bot unter {self.public} zur Verfügung."""
        follog_.log(45, "folgenbitte from external network %s", message.author.host)
        return self.post(msg, reply_to_status=message)

    def follow(self, user):
        logger.warning("Follow @%s", str(user))
        if self.readonly:
            return
        self.api.account_follow(int(user))

    def defollow(self, user):
        logger.warning("Defollow @%s", str(user))
        if self.readonly:
            return
        self.api.account_unfollow(int(user))

    def mentions(self):
        result = []
        for noti in self.api.notifications(mentions_only=True):
            if noti.type == 'mention':
                result.append(noti.status)
                try:
                    if not self.readonly:
                        self.api.notifications_dismiss(noti)
                except MastodonNotFoundError:
                    logger.exception("Error while cleaning out notification %s", noti.id)
        logger.debug("found %d mentions", len(result))
        return result

    def timeline(self):
        if self.mode == 'global':
            result = self.api.timeline_home(since_id=self.high_message)
            logger.debug("found %d status in timeline", len(result))
        elif self.mode == 'local':
            result = self.api.timeline_local(since_id=self.high_message)
            logger.debug("found %d status in local timeline", len(result))
        else:
            raise NotImplementedError("Bad bot mode '%s' in account fields")
        return result

    def hashtags(self, mt_list):
        # NOTE: finding magic hashtags from other servers seems inconsistent.
        local = self.mode == 'local'
        result = []
        for tag in mt_list:
            for msg in self.api.timeline_hashtag(tag[1:], local=local, since_id=self.high_message):
                result.append(msg)
        logger.debug("found %d status in hashtags", len(result))
        return result

    def get_status(self, status_id):
        try:
            return self.api.status(id=status_id)
        except MastodonNotFoundError:
            return None

    def is_followed(self, user):
        return self.api.account_relationships(int(user))[0].following

def make_mastodon(args, highest_ids):
    mast = mastodon.Mastodon(
        **args.config[args.account]
    )
    logger.info("Created mastodon API instance for @%s@%s", mast.me().acct, mast.instance().uri)
    return Mastodon(mast, args.readwrite, highest_ids)
