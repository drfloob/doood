#!/usr/bin/env python
import the_purple as purp
import sys, gobject, logging, time, random

import delayed_reply
logger = logging.getLogger("other_guy")

if __name__ == "__main__":

    who = sys.argv[1]
    conversation = int( sys.argv[2] )
    saying = sys.argv[3]
    sleep_time_for_fake_thought = int( sys.argv[4] )
    sleep_time_for_fake_typing = int( sys.argv[5] )

    bus = purp.get_bus()

    purple = purp.get_purple(purp.get_bus())

    delayed_reply.do_delayed_reply( who
                                    , conversation
                                    , saying
                                    , sleep_time_for_fake_thought
                                    , sleep_time_for_fake_typing
                                    , purple
                                    , logger )

