#!/usr/bin/env python

CONFIG_FILENAME= ".doood_config.json"

import sys, time, random, os.path, json
import logging
import conversation_info as ci

ConfigData= None
logger = logging.getLogger("doood")

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

    logger.critical("No config file was found")
    sys.exit(42)
    

def load_settings():
    """Loads config file and parses JSON data"""
    global ConfigData
    FilePath= config_file_path()
    with open(FilePath) as f:
        ConfigData= json.load(f)

    #debug info
    logger.debug("Loaded Config Data from file '%s'", FilePath)
    logger.debug(json.dumps(ConfigData, sort_keys=True, indent=4))


def dood(account, sender, message, conversation, flags):
    logger.debug("account = %s", str(account))
    logger.debug("sender = %s", str(sender))
    logger.debug("message = %s", str(message))
    logger.debug("conversation = %s", str(conversation))
    logger.debug("flags = %s", str(flags))

    if sender in ConfigData[u"users"]:
        logger.debug("%s said: '%s'", sender, message)
        for key in ConfigData[u"replies"].iterkeys():
            if string.find(string.lower(message), string.lower(key)) != -1:
                #debug info
                logger.debug("responding to: '%s'", key)

                respond(sender, conversation, ConfigData[u"replies"][key])
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

    logger.debug("gc: %s", purple.PurpleConversationGetGc(conversation))
    logger.debug("conv: %s", purple.PurpleConvIm(conversation))
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


def handle_cmdargs():
    import getopt
    args = sys.argv[1:]
    logger.debug(args)
    try:
        oplist, args = getopt.getopt(args, "vd")
    except getopt.GetoptError, e:
        print "Error: %s" % e
        usage()
        sys.exit(2)
    for opt, arg in oplist:
        if opt == "-d":
            logging.basicConfig(level=logging.DEBUG)
            logger.debug("debug logging level set")
        elif opt == "-v":
            logging.basicConfig(level=logging.INFO)
            logger.info("info logging level set")
        else:
            print("Invalid Option: %s", opt)
            usage()
            sys.exit(2)

def usage():
    print "Usage: doood.py [-v]"


if __name__ == "__main__":

    handle_cmdargs()
    
    load_settings()
    bus.add_signal_receiver(dood,
                            dbus_interface="im.pidgin.purple.PurpleInterface",
                            signal_name="ReceivedImMsg")

    loop = gobject.MainLoop()
    loop.run()
