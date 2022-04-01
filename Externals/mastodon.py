"""Mastodon API including Command line argumentation"""

import configparser
import logging
import mastodon
from mastodon.Mastodon import MastodonAPIError, MastodonNotFoundError

from Externals.Measure import MeasureToot
from .message import fromToot
from .network import Network
from .user import fromMastodonUser

logger = logging.getLogger('bot.api.mastodon')
msg_logger = logging.getLogger('msg')

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
        user = fromMastodonUser(self.api.me())
        super().__init__(readwrite, highest_ids, MeasureToot(), fromToot, user)

    def post_single(self, text, **kwargs):
        # pylint: disable=too-many-return-statements
        if len(text) == 0:
            logger.error("Empty tweet?")
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
                    self.api.notifications_dismiss(noti)
                except MastodonNotFoundError:
                    logger.exception("Error while cleaning out notification %s", noti.id)
        logger.debug("found %d mentions", len(result))
        return result

    def timeline(self):
        result = self.api.timeline_home(since_id=self.high_message)
        logger.debug("found %d status in timeline", len(result))
        return result

    def hashtags(self, mt_list):
        # NOTE: finding magic hashtags from other servers seems inconsistent.
        result = []
        for tag in mt_list:
            for msg in self.api.timeline_hashtag(tag[1:], local=False, since_id=self.high_message):
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
    config = configparser.ConfigParser()
    config.read(args.config)
    mast = mastodon.Mastodon(
        **config[args.account]
    )
    logger.info("Created mastodon API instance for @%s@%s", mast.me().acct, mast.instance().uri)
    return Mastodon(mast, args.readwrite, highest_ids)
