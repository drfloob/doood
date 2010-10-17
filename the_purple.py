import sys, dbus

import dbus, gobject, string
from dbus.mainloop.glib import DBusGMainLoop
DBusGMainLoop(set_as_default=True)

def get_bus():
    return dbus.SessionBus()

def get_purple(bus):
    obj = bus.get_object("im.pidgin.purple.PurpleService", "/im/pidgin/purple/PurpleObject")
    purple = dbus.Interface(obj, "im.pidgin.purple.PurpleInterface")
    return purple
