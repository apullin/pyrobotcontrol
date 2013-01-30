#!/usr/bin/env python
"""
authors: Kevin Peterson, Stan Baek, Andrew Pullin
Modification on 2011-10-4:

This file creates a class BaseStation that can be used to send commands 
to the custom basestation or an XBee module

Wrapper functions are provided for this class, see:
base_functions and robot_functions

Modification on 2013-1-30: (apullin)
Brining in functions from base_functions to create a unified Basestation class.

"""


import time, os, sys
import command 
import serial
from scan import *
from xbee import XBee

class BaseStation(object):

    def __init__(self, port, baud, channel = None, PANid = None, base_addr = None, call_back = None):
        
        try:
            self.ser = serial.Serial(port, baud, timeout = 1)
        except serial.SerialException:
            print
            print "Could not open serial port:",port
            print
            print "Scanning for available COM ports:"
            print "------------------------------------"
            scanSerialPorts()
            print "------------------------------------"
            print "Check your BaseStation declaration --OR--"
            print " you may need to change the port in shared.py"
            sys.exit() #force exit
            
        print "serial open"
            
        self.ser.writeTimeout = 5

        #Set up callback
        if call_back == None:
            self.xb = XBee(self.ser)   #Snchronous mode, not used by BML!
        else:
            self.xb = XBee(self.ser, callback = call_back)

    def close(self):
        try:
            self.xb.halt()
            self.ser.close()
            print "BaseStation halted and close."
        except SerialException:
            print "SerialException on Basestation close() attempt."

    def sendTX(self, status, type, data ):
        pld = chr(status) + chr(type)  + ''.join(data)
        self.xb.tx(dest_addr = self.dest_addr, data = pld)
        time.sleep(0.1)
        
    def sendAT(self, command, parameter = None, frame_id = None):
        if parameter is not None:
            if frame_id is not None:
                self.xb.at(frame_id = frame_id, command = command, parameter = parameter)
            else:
                self.xb.at(command = command, parameter = parameter)
        elif frame_id is not None:
            self.xb.at(frame_id = frame_id, command = command)
        else:
            self.xb.at(command = command)


    def read(self):
        packet = self.xb.wait_read_frame()

        return packet

    def getChannel(self, frame_id):
        self.bs.sendAT(command='CH',frame_id=frame_id)

    def setChannel(self, param, frame_id = None):
        self.bs.sendAT(command='CH',parameter=param,frame_id = frame_id)

    def getPanID(self, frame_id):
        self.bs.sendAT(command='ID',frame_id=frame_id)
        
    def setPanID(self, param, frame_id = None):
        self.bs.sendAT(command='ID',parameter=param,frame_id = frame_id)
        
    def getSrcAddr(self, frame_id):
        self.bs.sendAT(command='MY',frame_id=frame_id)
        
    def setSrcAddr(self, param, frame_id = None):
        self.bs.sendAT(command='MY',parameter=param,frame_id = frame_id)

    def getLastAckd(self, frame_id):
        self.bs.sendAT(command='EA',frame_id=frame_id)

