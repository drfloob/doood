#!/usr/bin/env python

import sys, logging, time, random


def do_delayed_reply( who
                      , conversation_id
                      , message_text
                      , sleep_time_for_fake_thought
                      , sleep_time_for_fake_typing
                      , the_purple_object 
                      , logger ):
    print "entering do_delayed_reply"
    logger.debug("entering do_delayed_reply")
    logger.debug("\twho = %s", who )
    logger.debug("\tconversation = %d", conversation_id)

    time.sleep( sleep_time_for_fake_thought )
    gc = the_purple_object.PurpleConversationGetGc(conversation_id)

    # tell user that I'm typing, and type for a while
    the_purple_object.ServSendTyping(gc, who, 1)
    time.sleep(sleep_time_for_fake_typing)
    
    # send message
    the_purple_object.PurpleConvImSend(the_purple_object.PurpleConvIm(conversation_id), message_text)
    
    # just in case, set status to "not typing"
    #purple.ServSendTyping(gc, who, 0)
    
