#!/usr/bin/env python

CONFIG_FILENAME= ".doood_config.json"

import sys, time, random, os.path, json
import logging
import conversation_info as ci
import the_purple as purp
import multiprocessing

ConfigData= None
logger = logging.getLogger("doood")
ParallelRespond = False

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
    logger.debug("entering 'dood' signal-handler")
    logger.debug("\taccount = %s", str(account))
    logger.debug("\tsender = %s", str(sender))
    logger.debug("\tmessage = %s", str(message))
    logger.debug("\tconversation = %s", str(conversation))
    logger.debug("\tflags = %s", str(flags))

    purple = purp.get_purple(purp.get_bus())
    cd = purple.PurpleConversationGetChatData( conversation )
    the_im = purple.PurpleConvIm( conversation )
    logger.debug("\tdata = %s", str(the_im))

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
                    logger.debug("i = %d; msg = %s", i, msgtxt)

    if sender in ConfigData[u"users"]:
        logger.debug("\t%s said: '%s'", sender, message)
        for key in ConfigData[u"replies"].iterkeys():
            if string.find(string.lower(message), string.lower(key)) != -1:
                #debug info
                logger.debug("responding to: '%s'", key)

                try:
                    if ParallelRespond:
                        #print "not running in parallel yet"
                        #respond(sender, conversation, ConfigData[u"replies"][key])
                        logger.debug("Spawning new process to handle '%s' message from %s" % (key, sender))
                        p = multiprocessing.Process(target=respond, args=(sender, conversation, ConfigData[u"replies"][key]))
                        p.start()
                    else:
                        respond(sender, conversation, ConfigData[u"replies"][key])
                except dbus.exceptions.DBusException:
                    import traceback

                    (type, value, tb) = sys.exc_info()
                    logger.error("DBus Error. Run in debug mode for more information.")
                    logger.debug(string.join(traceback.format_exception(type, value, tb)))
                break

def respond(who, conversation, saying):
    purple = purp.get_purple(purp.get_bus())

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
        oplist, args = getopt.getopt(args, "vd", ["parallel"])
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
        elif opt == "--parallel":
            global ParallelRespond
            ParallelRespond = True
            logger.info("Parallel execution ON")
        else:
            print("Invalid Option: %s", opt)
            usage()
            sys.exit(2)

def usage():
    print "Usage: doood.py [-v]"


if __name__ == "__main__":
    handle_cmdargs()
    load_settings()
    bus = purp.get_bus()
    bus.add_signal_receiver(dood,
                            dbus_interface="im.pidgin.purple.PurpleInterface",
                            signal_name="ReceivedImMsg")
    bus.add_signal_receiver(ci.on_wrote_im_message,
                            dbus_interface="im.pidgin.purple.PurpleInterface",
                            signal_name="WroteImMsg")

    loop = gobject.MainLoop()
    loop.run()

