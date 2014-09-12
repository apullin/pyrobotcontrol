"""
Contents of this file are copyright Andrew Pullin, 2013
"""

#Base station
#BS_COMPORT = 'COM3'
#BS_BAUDRATE = 230400
#XBee
BS_COMPORT = 'COM4'
BS_BAUDRATE = 57600

BS_CHANNEL = '\x19'
BS_PAN_ID = '\x20\x50'
BS_SRC_ADDR = '\x20\x51'

def setupBasestation(bs):
    bs.setChannel(XBEE_CHANNEL)
    bs.setSrcAddr(XBEE_SRC_ADDR)
    bs.setPanID(XBEE_PAN_ID)

deg2count = 14.375
count2deg = 1/deg2count

#For download timeout
last_packet_time = 0
pkts = 0

ROBOTS = []