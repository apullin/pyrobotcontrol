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

#Define functions to use
def xbee_received(packet):
    
    #Check type of packet:
    name = packet.get('id')
    #The packet is a response to an AT command
    if name == 'at_response':
        print "Got AT response"
        frame_id = packet.get('frame_id')
        command = packet.get('command')
        status = packet.get('status')
        parameter = packet.get('parameter')
        #Handle packet in whatever way is appropriate
        print "command = ",command
        print "length = ",len(parameter)        

    #The packet is data recieved from the radio
    elif name == 'rx':
        print "Got RX"
        src_addr = packet.get('source_addr')
        rssi = packet.get('rssi')
        options = packet.get('options')
        data = packet.get('rf_data')
        #Handle packet in whatever way is appropriate
        print 'Packet received'
        
    
#Initialize the basestation and the helper functions
xb = BaseStation('COM3', 57600, callbackfn = xbee_received)

if __name__ == '__main__':
    
    chan = xb.getChannel('a')
    print chan
    src = xb.getSrcAddr('b')
    print src
    pan = xb.getPanID('c')
    print pan
    
    
    #base.setChannel('\x17')

    #robot.go(40)
    
    #time.sleep(1)
    
    #robot.stop()
    
    print '\n'
    xb.close()
    sys.exit()