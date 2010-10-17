#!/usr/bin/env python

import sys, time, random, os.path, json
import logging
import the_purple as purp


def get_reasonable_pause_before_reply():
    logging.debug("test debug output: %d", 5 )
    return random.randrange(1,3)


def on_wrote_im_message(account
                        , who_wrote
                        , message
                        , conversation
                        , flags ):
    logging.debug("account = %s", str(account))
    logging.debug("sender = %s", str(who_wrote))
    logging.debug("message = %s", str(message))
    logging.debug("conversation = %s", str(conversation))
    logging.debug("flags = %s", str(flags))





