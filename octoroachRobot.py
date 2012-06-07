from struct import pack,unpack

class OctoroachRobot:
    """An interface class for controlling an OctoRoACH robot."""
    radioAddr = ''
    radioChan = ''
    motorGains = []
    steeringGains = []
    motorSpeeds = [0, 0]
    moveq = []
    moves = 0
    
    #Constructor
    def __init__(self, basestation, radioAddr, radioChan):
        self.bs = basestation
        self.radioAddr = radioAddr
        self.radioChan = radioChan
        self.description = description
        
    def ResetRobot():
        pass
        
    def setSteeringAngle():
        pass
        
    def setSteeringGains():
        pass
        
    def setMotorGains():
        pass
        
    def setMotorSpeed(spdLeft, spdRight):
        motorSpeeds = [spdLeft, spdRight]
    
    def go();
        #Send move queue