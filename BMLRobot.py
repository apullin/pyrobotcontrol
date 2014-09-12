class BMLRobot:
    VERBOSE = True
    
    DEST_ADDR = None
    PAN_ID = None
    CHANNEL = None
    
    robot_queried = False
    motor_gains_set = False
    flash_erased = False
    #robot_awake = True
    motorGains = [0,0,0,0,0,  0,0,0,0,0] #TODO, change motor gains to 4x list
    dataFileName = ''
    imudata = [ [] ]
    numSamples = 0
    telemSampleFreq = 1000
    
    
    def __init__(self, dest_addr, pan_id = None, channel = None, basestation = xb):
        #DEST_ADDR is stricly required to construct a robot object
        self.DEST_ADDR = dest_addr
        self.DEST_ADDR_int = unpack('>H',self.DEST_ADDR)[0] #DEST addr as integer
        
        if pan_id is not None:
            self.PAN_ID = pan_id
            self.PAN_ID_int = unpack('>H',self.PAN_ID)[0] #PAN ID as integer
        if channel is not None:
            self.CHANNEL = channel
            self.CHANNEL_int = ord(self.CHANNEL)
            
        self.basestation = xb
        print "Robot with DEST_ADDR = 0x%04X " % self.DEST_ADDR_int
    
    def clAnnounce(self):
        print "DST: 0x%04X | " % self.DEST_ADDR_int,
    
    def tx(self, status, type, data):
        payload = chr(status) + chr(type) + ''.join(data)
        self.xb.tx(dest_addr = self.DEST_ADDR, data = payload)
        
    def reset(self):
        self.clAnnounce()
        print "Resetting robot..."
        self.tx( 0, command.SOFTWARE_RESET, pack('h',1))
        
    def sendEcho(self, msg):
        self.tx( 0, command.ECHO, msg)
    
    #def wake(self, period = 0.2, retries = 8):
    #    self.robot_awake = False;
    #    while not(self.robot_awake):
    #        self.clAnnounce()
    #        print "Waking robot ... "
    #        self.tx(0, command.SLEEP, pack('b',0))
    #        time.sleep(period)
    #     
    #def sleep(self):
    #    self.clAnnounce()
    #    print "Sleeping robot ... "
    #    self.tx( 0, command.SLEEP, pack('b',1))
    
    def setMotorGains(self, gains, retries = 8):
        tries = 1
        self.motorGains = gains
        while not(self.motor_gains_set) and (tries <= retries):
            self.clAnnounce()
            print "Setting motor gains...   ",tries,"/8"
            self.tx( 0, command.SET_PID_GAINS, pack('10h',*gains))
            tries = tries + 1
            time.sleep(0.1)
            
    def eraseFlashMem(self, timeout = 8):
        eraseStartTime = time.time()
        self.tx( 0, command.ERASE_SECTORS, pack('L',self.numSamples))
        self.clAnnounce()
        print "Started flash erase ..."
        while not (self.flash_erased):
            #sys.stdout.write('.')
            time.sleep(0.25)
            if (time.time() - eraseStartTime) > timeout:
                print"Flash erase timeout, retrying;"
                self.tx( 0, command.ERASE_SECTORS, pack('L',self.numSamples))
                eraseStartTime = time.time()
                
    def query(self, retries = 8):
        self.robot_queried = False
        tries = 1
        while not(self.robot_queried) and (tries <= retries):
            self.clAnnounce()
            print "Querying robot , ",tries,"/",retries
            self.tx( 0,  command.WHO_AM_I, "Robot Echo") #sent text is unimportant
            tries = tries + 1
            time.sleep(0.1)
            
    