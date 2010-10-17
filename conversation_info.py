#!/usr/bin/env python

import sys, time, random, os.path, json
import logging
import the_purple as purp

logger = logging.getLogger("doood")

def get_reasonable_pause_before_reply():
    logger.debug("test debug output: %d", 5 )
    return random.randrange(1,3)


def on_wrote_im_message(account
                        , who_wrote
                        , message
                        , conversation
                        , flags ):
    logger.debug("account = %s", str(account))
    logger.debug("sender = %s", str(who_wrote))
    logger.debug("message = %s", str(message))
    logger.debug("conversation = %s", str(conversation))
    logger.debug("flags = %s", str(flags))





