#!/usr/bin/env python

import sys, time, random, os.path, json
import logging
import the_purple as purp

logger = logging.getLogger("doood")

def get_reasonable_pause_before_reply():
    logger.debug("test debug output: %d", 5 )
    return random.randrange(1,3)

"""
From libpurple conversation.h

00105 typedef enum
00106 {
00107     PURPLE_MESSAGE_SEND        = 0x0001,
00108     PURPLE_MESSAGE_RECV        = 0x0002,
00109     PURPLE_MESSAGE_SYSTEM      = 0x0004,
00110     PURPLE_MESSAGE_AUTO_RESP   = 0x0008,
00111     PURPLE_MESSAGE_ACTIVE_ONLY = 0x0010,
00118     PURPLE_MESSAGE_NICK        = 0x0020,
00119     PURPLE_MESSAGE_NO_LOG      = 0x0040,
00120     PURPLE_MESSAGE_WHISPER     = 0x0080,
00121     PURPLE_MESSAGE_ERROR       = 0x0200,
00122     PURPLE_MESSAGE_DELAYED     = 0x0400,
00123     PURPLE_MESSAGE_RAW         = 0x0800,
00125     PURPLE_MESSAGE_IMAGES      = 0x1000,
00126     PURPLE_MESSAGE_NOTIFY      = 0x2000,
00127     PURPLE_MESSAGE_NO_LINKIFY  = 0x4000,
00129     PURPLE_MESSAGE_INVISIBLE   = 0x8000
00130 } PurpleMessageFlags;

"""
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

    if flags == 1:
        logger.debug("\t\tThis one COUNTS.")


def track_incoming_messages(account
                        , who_wrote
                        , message
                        , conversation
                        , flags ):
    logger.debug("entering ci.track_incoming_messages")
    logger.debug("\taccount = %s", str(account))
    logger.debug("\tsender = %s", str(who_wrote))
    logger.debug("\tmessage = %s", str(message))
    logger.debug("\tconversation = %s", str(conversation))
    logger.debug("\tflags = %s", str(flags))

    if flags == 2:
        logger.debug("\t\tThis one COUNTS.")



