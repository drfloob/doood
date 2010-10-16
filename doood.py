#!/usr/bin/env python

################################################################################
# CONFIGURATION
################################################################################

## Your custom replies 
doodz = {
    'hair cut': 'did you know the human head has over 150,000 hairs on it?'
    }

## The users that this will work for
users = ["somechick", "somedood"]

################################################################################
# THE REST IS CODE
################################################################################

import time, random

def dood(account, sender, message, conversation, flags):
    if sender in users:
        print sender, "said: ", message
        for key in doodz.iterkeys():
            if string.find(string.lower(message), string.lower(key)) != -1:
                print("responding to: ", key)
                respond(sender, conversation, doodz[key])
                break

import dbus, gobject, string
from dbus.mainloop.glib import DBusGMainLoop
DBusGMainLoop(set_as_default=True)
bus = dbus.SessionBus()

def respond(who, conversation, saying):
    global bus
    obj = bus.get_object("im.pidgin.purple.PurpleService", "/im/pidgin/purple/PurpleObject")
    purple = dbus.Interface(obj, "im.pidgin.purple.PurpleInterface")
    
    #sets THEIR typing status in YOUR conversation window. WTF?
    #purple.PurpleConvImSetTypingState(purple.PurpleConvIm(conversation), 1)

    #print "gc: ", purple.PurpleConversationGetGc(conversation)
    #print "conv: ", purple.PurpleConvIm(conversation)
    gc = purple.PurpleConversationGetGc(conversation)

    # wait for a second before typing
    time.sleep(random.randrange(1,3))
    
    # tell user that I'm typing, and type for a while
    purple.ServSendTyping(gc, who, 1)
    time.sleep(random.randrange(2,5))
    
    # send message
    purple.PurpleConvImSend(purple.PurpleConvIm(conversation), saying)
    
    # just in case, set status to "not typing"
    purple.ServSendTyping(gc, who, 0)




bus.add_signal_receiver(dood,
                        dbus_interface="im.pidgin.purple.PurpleInterface",
                        signal_name="ReceivedImMsg")

loop = gobject.MainLoop()
loop.run()
