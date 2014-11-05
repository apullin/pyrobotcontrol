#!/usr/bin/env python
"""
authors: Kevin Peterson
Modification on 2011-03-7:

"""

import numpy as np
from lib import command
from struct import *
import time, serial, sys, os
import traceback
from BaseStation import *

#Define constants to use
XB1_ADDR = '\x20\x00'
XB2_ADDR = '\x30\x00'
XB_CHAN  = '\x0e'
XB_PANID = '\x99\x99'

#Initialize the basestation and the helper functions
xb1 = BaseStation('COM3', baudrate = 57600 , verbose = False)
xb2 = BaseStation('COM4', baudrate = 57600 , verbose = False)

if __name__ == '__main__':
    
    XBEES = [xb1, xb2]
    
    print "Setting temporary XBee config..."
    
    # Change xbee settings
    xb1.setChannel(XB_CHAN)
    xb1.setSrcAddr(XB1_ADDR)
    xb1.setPanID(XB_PANID)
    
    print "--------  XBee #1  ----------"
    chan = xb1.getChannel()
    print "xbee CHAN : 0x%x" % chan
    src = xb1.getSrcAddr()
    print "xbee SRC addr : 0x%x" % src
    pan = xb1.getPanID()
    print "xbee PAN ID : 0x%x" % pan
    print "\n",
    
    # Change xbee settings
    xb2.setChannel(XB_CHAN)
    xb2.setSrcAddr(XB2_ADDR)
    xb2.setPanID(XB_PANID)
    
    print "--------  XBee #2  ----------"
    chan = xb2.getChannel()
    print "xbee CHAN : 0x%x" % chan
    src = xb2.getSrcAddr()
    print "xbee SRC addr : 0x%x" % src
    pan = xb2.getPanID()
    print "xbee PAN ID : 0x%x" % pan
    print "\n",
    
    # Try sending between xbees:
    print "Sending test packets at 10Hz  ;  Ctrl + C to stop"
    while True:
        try:
            xb2.xb.tx(dest_addr = XB1_ADDR, data = 'Test data')
            time.sleep(0.1)
        except KeyboardInterrupt:
            break    
            
    print "Stopped test packets."
    
    while True:
        try:
            time.sleep(0.1)
        except KeyboardInterrupt:
            break

    for xb in XBEES:
        xb.close()
        
    sys.exit()