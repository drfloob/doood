#!/usr/bin/env python

CONFIG_FILENAME= ".doood_config.json"

import sys, time, random, os.path, json
import logging
import conversation_info as ci
import the_purple as purp

ConfigData= None
logger = logging.getLogger("doood")

import dbus, gobject, string
from dbus.mainloop.glib import DBusGMainLoop


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
    logging.debug("account = %s", str(account))
    logging.debug("sender = %s", str(sender))
    logging.debug("message = %s", str(message))
    logging.debug("conversation = %s", str(conversation))
    logging.debug("flags = %s", str(flags))

    purple = purp.get_purple()
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
        logger.debug("%s said: '%s'", sender, message)
        for key in ConfigData[u"replies"].iterkeys():
            if string.find(string.lower(message), string.lower(key)) != -1:
                #debug info
                logger.debug("responding to: '%s'", key)

                try:
                    respond(sender, conversation, ConfigData[u"replies"][key])
                except dbus.exceptions.DBusException:
                    import traceback

                    (type, value, tb) = sys.exc_info()
                    logger.error("DBus Error. Run in debug mode for more information.")
                    logger.debug(string.join(traceback.format_exception(type, value, tb)))
                break


def respond(who, conversation, saying):
    purple = purp.get_purple()

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
    purp.bus.add_signal_receiver(dood,
                            dbus_interface="im.pidgin.purple.PurpleInterface",
                            signal_name="ReceivedImMsg")
    purp.bus.add_signal_receiver(ci.on_wrote_im_message,
                            dbus_interface="im.pidgin.purple.PurpleInterface",
                            signal_name="WroteImMsg")

    loop = gobject.MainLoop()
    loop.run()
