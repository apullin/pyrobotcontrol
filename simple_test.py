"""
authors: apullin

"""

import sys
from lib.BaseStation import BaseStation
from callbackFunc import xbee_received

def main(): 
    bs = BaseStation("COM4", 57600, 0x19, 0x2050, 0x2051, call_back = xbee_received)
    print bs
    bs.close()
    
    
if __name__ == '__main__':
    main()