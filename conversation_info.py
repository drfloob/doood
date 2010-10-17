#!/usr/bin/env python

import sys, time, random, os.path, json
import logging

def get_reasonable_pause_before_reply():
    logging.debug("test debug output: %d", 5 )
    return random.randrange(1,3)


