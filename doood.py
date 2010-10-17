#!/usr/bin/env python

CONFIG_FILENAME= ".doood_config.json"

import sys, time, random, os.path, json
import logging # in the __main__ function the log level is set.
import conversation_info as ci
ConfigData= None

import dbus, gobject, string
from dbus.mainloop.glib import DBusGMainLoop
DBusGMainLoop(set_as_default=True)
bus = dbus.SessionBus()

def get_purple():
    global bus
    obj = bus.get_object("im.pidgin.purple.PurpleService", "/im/pidgin/purple/PurpleObject")
    purple = dbus.Interface(obj, "im.pidgin.purple.PurpleInterface")
    return purple


def config_file_path():
    """Returns the absolute path to the working config file. If no config file exists, the program quits"""
    Home= os.getenv("HOME")
    DirLoc = os.path.dirname(__file__)

    if os.path.isfile(os.path.join(DirLoc, CONFIG_FILENAME)):
        return os.path.join(DirLoc, CONFIG_FILENAME)
    if os.path.isfile(os.path.join(Home, ".config", CONFIG_FILENAME)):
        return os.path.join(Home, ".config", CONFIG_FILENAME)
    if os.path.isfile(os.path.join(Home, CONFIG_FILENAME)):
        return os.path.join(Home, CONFIG_FILENAME)

    print "No config file was found"
    sys.exit(42)
    

def load_settings():
    global ConfigData
    FilePath= config_file_path()
    with open(FilePath) as f:
        ConfigData= json.load(f)

    #debug info
    print "Loaded Config Data from file", FilePath, ":"
    print json.dumps(ConfigData, sort_keys=True, indent=4)
    print "Raw Config Data"
    print ConfigData


def dood(account, sender, message, conversation, flags):
    logging.debug("account = %s", str(account))
    logging.debug("sender = %s", str(sender))
    logging.debug("message = %s", str(message))
    logging.debug("conversation = %s", str(conversation))
    logging.debug("flags = %s", str(flags))
    logging.debug("type of conversation = %s", str(type(conversation)))
    
    purple = get_purple()
    cd = purple.PurpleConversationGetChatData( conversation )
    the_im = purple.PurpleConvIm( conversation )
    logging.debug("data = %s", str(the_im))

    # intentionally disabled test code
    if 1 == 0:
        for i in range(0,65500):
            msgtxt = ''
            try:
                msgtxt = purple.PurpleConversationMessageGetMessage(i)
            except:
                pass
            else:
                if len(msgtxt) != 0:
                    logging.debug("i = %d; msg = %s", i, msgtxt)

    if sender in ConfigData[u"users"]:
        #print sender, "said: ", message
        for key in ConfigData[u"replies"].iterkeys():
            if string.find(string.lower(message), string.lower(key)) != -1:
                #debug info
                print("responding to: ", key)

                respond(sender, conversation, ConfigData[u"replies"][key])
                break


def respond(who, conversation, saying):
    purple = get_purple()

    #sets THEIR typing status in YOUR conversation window. WTF?
    #purple.PurpleConvImSetTypingState(purple.PurpleConvIm(conversation), 1)

    #print "gc: ", purple.PurpleConversationGetGc(conversation)
    #print "conv: ", purple.PurpleConvIm(conversation)
    gc = purple.PurpleConversationGetGc(conversation)

    # wait for a second before typing
    time.sleep( ci.get_reasonable_pause_before_reply() )
    
    # tell user that I'm typing, and type for a while
    purple.ServSendTyping(gc, who, 1)
    time.sleep(random.randrange(2,5))
    
    # send message
    purple.PurpleConvImSend(purple.PurpleConvIm(conversation), saying)
    
    # just in case, set status to "not typing"
    purple.ServSendTyping(gc, who, 0)



if __name__ == "__main__":
    load_settings()
    logging.basicConfig(level=logging.DEBUG) # this should probably be configurable
    bus.add_signal_receiver(dood,
                            dbus_interface="im.pidgin.purple.PurpleInterface",
                            signal_name="ReceivedImMsg")
    bus.add_signal_receiver(ci.on_wrote_im_message,
                            dbus_interface="im.pidgin.purple.PurpleInterface",
                            signal_name="WroteImMsg")

    loop = gobject.MainLoop()
    loop.run()
