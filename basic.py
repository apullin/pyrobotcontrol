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
    
    print "Initial settings:"
    print "-----------------"
    chan = xb.getChannel()
    print "xbee CHAN : 0x%x" % chan
    src = xb.getSrcAddr()
    print "xbee SRC addr : 0x%x" % src
    pan = xb.getPanID()
    print "xbee PAN ID : 0x%x" % pan
    
    # Change xbee settings
    print "\n"
    print " -- changing xbee CHAN to 0xe"
    xb.setChannel('\x0e')
    print " -- changing xbee SRC to 0x1234"
    xb.setSrcAddr('\x12\x34')
    print " -- changing xbee PAN to 0x9999"
    xb.setPanID('\x99\x99')
    
    print "\n"
    print "Changed settings readback:"
    print "--------------------------"
    chan = xb.getChannel()
    print "xbee CHAN : 0x%x" % chan
    src = xb.getSrcAddr()
    print "xbee SRC addr : 0x%x" % src
    pan = xb.getPanID()
    print "xbee PAN ID : 0x%x" % pan
    
    print "\n"
    print "Writing settings to xbee storage."
    xb.writeParams()
    
    while True:
        try:
            time.sleep(0.1)
        except KeyboardInterrupt:
            break

    xb.close()
    sys.exit()