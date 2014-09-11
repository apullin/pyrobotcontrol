#!/usr/bin/env python
"""
authors: Kevin Peterson
Modification on 2011-03-7:

"""

import numpy as np
from lib import command
from struct import *
import time, serial, sys, os
from BaseStation import *

#Define constants to use
DEST_ADDR = '\x20\x12'

#Initialize the basestation and the helper functions
xb = BaseStation('COM3', 57600, verbose = False)

if __name__ == '__main__':
    
    print "Type Ctrl+C to exit at any time."
    
    chan = xb.getChannel()
    print "xbee CHAN : 0x%x" % chan
    src = xb.getSrcAddr()
    print "xbee SRC addr : 0x%x" % src
    pan = xb.getPanID()
    print "xbee PAN ID : 0x%x" % pan
    
    #base.setChannel('\x17')

    #robot.go(40)
    
    #time.sleep(1)
    
    #robot.stop()
    
    while True:
        try:
            time.sleep(0.1)
        except KeyboardInterrupt:
            break

    xb.close()
    sys.exit()