# pylint: disable=C0114
import logging
from .react import process_commands, process_message
logger = logging.getLogger('bot.' + __name__)

def handle_list(network, database, magic_tags, magic_emojis):
    message_dict = network.all_relevant_tweets(magic_tags)
    for mid, message in message_dict.items():
        # exclude some message:
        if message.is_not_eligible:
            logger.debug("Status %s is not eligible", mid)
            continue
        logger.info("Looking at status %d", mid)
        # handle #folgenbitte and #entfolgen and possibly other meta commands, but
        # only for explicit mentions.
        if message.is_explicit_mention:
            logger.info("Message explicitly mentions me")
            process_commands(message, network)
        if message.has_hashtag(magic_tags):
            logger.info("Message has magic hashtag")
        if message.has_hashtag(magic_emojis):
            logger.info("Message has magic emoji")
        # Process this message
        mode = message.get_mode(magic_tags, magic_emojis)
        process_message(message,
                network,
                database,
                magic_tags,
                magic_emojis,
                modus=mode)
        dmt = message.default_magic_hashtag([*magic_tags, *magic_emojis])
        for other in message.get_other_posts(
                    message_dict,
                    mode=mode,
                    network=network,
                    database=database,
                    magic_tags=magic_tags,
                    magic_emojis=magic_emojis
                ):
            logger.debug("Processing message %d mode %s def magic hash tag %s", other.id, mode, dmt)
            process_message(other,
                    network,
                    database,
                    magic_tags,
                    magic_emojis,
                    modus=mode,
                    default_magic_tag=dmt)
