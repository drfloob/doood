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
    logger.debug("entering on_wrote_im_message")
    logger.debug("\taccount = %s", str(account))
    logger.debug("\tsender = %s", str(who_wrote))
    logger.debug("\tmessage = %s", str(message))
    logger.debug("\tconversation = %s", str(conversation))
    logger.debug("\tflags = %s", str(flags))





