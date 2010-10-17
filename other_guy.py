#!/usr/bin/env python
import the_purple as purp
import sys, gobject, logging, time, random

logger = logging.getLogger("other_guy")

if __name__ == "__main__":
    print sys.argv[1]
    print sys.argv[2]

    who = sys.argv[1]
    conversation = int( sys.argv[2])
    saying = sys.argv[3]

    bus = purp.get_bus()

    # wait for a second before typing
    #time.sleep( ci.get_reasonable_pause_before_reply() )
    time.sleep(10)

    purple = purp.get_purple(purp.get_bus())

    #sets THEIR typing status in YOUR conversation window. WTF?
    #purple.PurpleConvImSetTypingState(purple.PurpleConvIm(conversation), 1)

    logger.debug("gc: %s", purple.PurpleConversationGetGc(conversation))
    logger.debug("conv: %s", purple.PurpleConvIm(conversation))
    gc = purple.PurpleConversationGetGc(conversation)


    # tell user that I'm typing, and type for a while
    purple.ServSendTyping(gc, who, 1)
    time.sleep(15)
    
    # send message
    purple.PurpleConvImSend(purple.PurpleConvIm(conversation), saying)
    
    # just in case, set status to "not typing"
    #purple.ServSendTyping(gc, who, 0)
