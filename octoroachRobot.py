from struct import pack,unpack
import BMLRobot

## Constants
###
MOVE_SEG_CONSTANT = 0
MOVE_SEG_RAMP = 1
MOVE_SEG_SIN = 2
MOVE_SEG_TRI = 3
MOVE_SEG_SAW = 4
MOVE_SEG_IDLE = 5
MOVE_SEG_LOOP_DECL = 6
MOVE_SEG_LOOP_CLEAR = 7
MOVE_SEG_QFLUSH = 8

###
TAIL_SEG_CONSTANT = 0
TAIL_SEG_RAMP = 1
TAIL_SEG_SIN = 2
TAIL_SEG_TRI = 3
TAIL_SEG_SAW = 4
TAIL_SEG_IDLE = 5
TAIL_GYRO_CONTROL = 6

##
STEER_MODE_OFF = 0
STEER_MODE_INCREASE = 1
STEER_MODE_DECREASE = 2
STEER_MODE_SPLIT = 3
STEER_MODE_YAW_DEC = 4
STEER_MODE_YAW_SPLIT = 5


class OctoroachRobot(BMLRobot):
    """An interface class for controlling an OctoRoACH robot."""
    #Motor PID controllers
    motorGains = []
    motorSpeeds = [0, 0]
    
    #Gyro steering controller
    steeringGains = [0,0,0,0,0]
    angRateDeg = 0;
    angRate = 0;

    #Movement queue
    moveq = []
    moves = 0
    
    telemFormatString = '%d,' + '%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%f'
    
    
    def setSteeringRate(self, rate, retries = 8):
        tries = 1
        self.angRateDeg = rate
        self.angRate = round( self.angRateDeg * 14.375)
        while not(self.steering_rate_set) and (tries <= retries):
            self.clAnnounce()
            print "Setting steering rate...   ",tries,"/",retries
            tries = tries + 1
            self.tx( 0, command.SET_CTRLD_TURN_RATE, pack('h', self.angRate))
            time.sleep(0.3)

    def setSteeringGains(self, gains, retries = 8):
        tries = 1
        self.steeringGains = gains
        while not (self.steering_gains_set) and (tries <= retries):
            self.clAnnounce()
            print "Setting steering gains...   ",tries,"/",retries
            self.tx( 0, command.SET_STEERING_GAINS, pack('6h',*gains))
            tries = tries + 1
            time.sleep(0.3)
            
    def setTailGains(self, gains, retries = 8):
        tries = 1
        self.tailGains = gains
        while not (self.tail_gains_set) and (tries <= retries):
            self.clAnnounce()
            print "Setting TAIL gains...   ",tries,"/8"
            self.tx( 0, command.SET_TAIL_GAINS, pack('5h',*gains))
            tries = tries + 1
            time.sleep(0.3)
            
    def startTelemetrySave(self):
        self.clAnnounce()
        print "Started telemtry save"
        self.tx( 0, command.SPECIAL_TELEMETRY, pack('L',self.numSamples))
        
    def sendMoveQueue(self, moveq):
        SEG_LENGTH = 9  #might be changed in the future
        
        n = moveq[0]
        if len(moveq[1:]) != n * SEG_LENGTH:
            print "CRITICAL: Move queue length specification invalid."
            print "Wrong number of entries, len(moveq) = ",len(moveque)
            xb_safe_exit()
            
        self.nummoves = n
        self.moveq = moveq
        
        self.clAnnounce()
        print "Sending move queue with",self.nummoves," segments"
        
        segments = moveq[1:]
        #Convert to a list of lists, each sublist is one entry
        segments = [segments[i:i+SEG_LENGTH] for i in range(0,len(segments),SEG_LENGTH)]
        toSend = segments[0:4]
        
        pktCount = 1
        
        while toSend != []:
            self.clAnnounce()
            print "Move queue packet",pktCount
            numToSend = len(toSend)         #Could be < 4, since toSend still a list of lists
            toSend = [item for sublist in toSend for item in sublist]  #flatted toSend
            packet = [numToSend]
            packet.extend(toSend)    #Full moveq format to be given to pack()
            #Actual TX
            self.tx( 0, command.SET_MOVE_QUEUE, pack('=h'+numToSend*'hhLhhhhhh', *packet))
            time.sleep(0.01)                #simple holdoff, probably not neccesary
            segments = segments[4:]         #remanining unsent ones
            toSend = segments[0:4]          #Due to python indexing, this could be from 1-4
            pktCount = pktCount + 1
    
    def sendTailQueue(self, moveq):
        SEG_LENGTH = 6  #might be changed in the future
        
        n = moveq[0]
        if len(moveq[1:]) != n * SEG_LENGTH:
            print "CRITICAL: Tail queue length specification invalid."
            print "Wrong number of entries."
            xb_safe_exit()
            
        self.nummoves = n
        self.moveq = moveq
        
        self.clAnnounce()
        print "Sending TAIL queue with",self.nummoves," segments"
        
        segments = moveq[1:]
        #Convert to a list of lists, each sublist is one entry
        segments = [segments[i:i+SEG_LENGTH] for i in range(0,len(segments),SEG_LENGTH)]
        toSend = segments[0:4]
        
        pktCount = 1
        
        while toSend != []:
            self.clAnnounce()
            print "TAIL queue packet",pktCount
            numToSend = len(toSend)         #Could be < 4, since toSend still a list of lists
            toSend = [item for sublist in toSend for item in sublist]  #flatted toSend
            packet = [numToSend]
            packet.extend(toSend)    #Full moveq format to be given to pack()
            #Actual TX
            self.tx( 0, command.SET_TAIL_QUEUE, pack('=h'+numToSend*'hLhhhh', *packet))
            time.sleep(0.01)                #simple holdoff, probably not neccesary
            segments = segments[4:]         #remanining unsent ones
            toSend = segments[0:4]          #Due to python indexing, this could be from 1-4
            pktCount = pktCount + 1
    
    def setMotorSpeeds(self, spleft, spright):
        thrust = [spleft, 0, spright, 0, 0]
        self.tx( 0, command.SET_THRUST_CLOSED_LOOP, pack('5h',*thrust))
		
    def setTIH(self, channel, dc):
        thrust = [channel, dc]
        self.tx( 0, command.SET_THRUST_OPEN_LOOP, pack('2h',*thrust))
        
    def downloadTelemetry(self, timeout = 5, retry = True):
        #supress callback output messages for the duration of download
        self.VERBOSE = False
        self.clAnnounce()
        print "Started telemetry download"
        self.tx( 0, command.FLASH_READBACK, pack('=L',self.numSamples))
                
        dlStart = time.time()
        shared.last_packet_time = dlStart
        #bytesIn = 0
        while self.imudata.count([]) > 0:
            time.sleep(0.02)
            dlProgress(self.numSamples - self.imudata.count([]) , self.numSamples)
            if (time.time() - shared.last_packet_time) > timeout:
                print ""
                #Terminal message about missed packets
                self.clAnnounce()
                print "Readback timeout exceeded"
                print "Missed", self.imudata.count([]), "packets."
                print "Didn't get packets:"
                for index,item in enumerate(self.imudata):
                    if item == []:
                        print "#",index+1,
                print "" 
                break
                # Retry telem download            
                if retry == True:
                    raw_input("Press Enter to restart telemetry readback ...")
                    self.imudata = [ [] ] * self.numSamples
                    self.clAnnounce()
                    print "Started telemetry download"
                    dlStart = time.time()
                    shared.last_packet_time = dlStart
                    self.tx( 0, command.FLASH_READBACK, pack('=L',self.numSamples))
                else: #retry == false
                    print "Not trying telemetry download."          

        dlEnd = time.time()
        dlTime = dlEnd - dlStart
        #Final update to download progress bar to make it show 100%
        dlProgress(self.numSamples-self.imudata.count([]) , self.numSamples)
        #totBytes = 52*self.numSamples
        totBytes = 52*(self.numSamples - self.imudata.count([]))
        datarate = totBytes / dlTime / 1000.0
        print '\n'
        #self.clAnnounce()
        #print "Got ",self.numSamples,"samples in ",dlTime,"seconds"
        self.clAnnounce()
        print "DL rate: {0:.2f} KB/s".format(datarate)
        
        #enable callback output messages
        self.VERBOSE = True

        print ""
        self.saveImudata()
        #Done with flash download and save
    
    
    def saveImudata(self):
        self.findFileName()
        self.writeFileHeader()
        fileout = open(self.dataFileName, 'a')
        sanitized = [item for item in self.imudata if len(item) == 22]

        np.savetxt(fileout , np.array(sanitized), self.telemFormatString, delimiter = ',')
        #try:
        #    np.savetxt(fileout , np.array(sanitized), self.telemFormatString, delimiter = ',')
        #except ValueError:
        #    print "Error saving data to file"
        #    temp = np.array(self.imudata)
        #    print "terminal length: ", len(temp[-1])
        #    print "terminal array: ", temp[-1]
        #    print "lengths : ", map(len, self.imudata)

        fileout.close()
        self.clAnnounce()
        print "Telemtry data saved to", self.dataFileName
    
    def writeFileHeader(self):
        now = datetime.datetime.now()

        fileout = open(self.dataFileName,'w')
        #write out parameters
        fileout.write('% ' + now.strftime("%m/%d/%Y %H:%M") + '\n')
        fileout.write('%' + '  Robot: 0x%02X \n' % self.DEST_ADDR_int)
        fileout.write('%  angrate (deg) = ' + str(self.angRateDeg) + '\n')
        fileout.write('%  angrate (raw) = ' + str(self.angRate) + '\n')
        fileout.write('%  motorgains    = ' + repr(self.motorGains) + '\n')
        fileout.write('%  steeringGains = ' + repr(self.steeringGains) + '\n')
        fileout.write('%  runtime       = ' + repr(self.runtime) + '\n')
        fileout.write('%  numSamples    = ' + repr(self.numSamples) + '\n')
        fileout.write('%  moveq         = ' + repr(self.moveq) + '\n')
        fileout.write('% Columns: \n')
        fileout.write('% time | inputL | inputR| DCA | DCB | DCC | DCD | GyroX | GyroY | GyroZ | GryoZAvg | AccelX | AccelY |AccelZ | BEMFA | BEMFB | BEMFC | BEMFD | SteerIn | SteerOut | Vbatt | YawAngle\n')
        fileout.close()

    def setupImudata(self, moveq):
        MOVE_QUEUE_ENTRY_LEN = 9
        #Calculates the total movement time from the move queue above
        #done by striding over moveq array and summing times
        self.runtime = sum([moveq[i] for i in [(ind*MOVE_QUEUE_ENTRY_LEN)+3 for ind in range(0,moveq[0])]])
       
        #calculate the number of telemetry packets we expect
        self.numSamples = int(ceil(self.telemSampleFreq * (self.runtime + self.leadinTime + self.leadoutTime) / 1000.0))
        #allocate an array to write the downloaded telemetry data into
        self.imudata = [ [] ] * self.numSamples
        self.clAnnounce()
        print "Telemtry samples to save: ",self.numSamples

    def findFileName(self):
        filenames = glob.glob("*imudata*.txt");
        # Explicitly remove "imudata.txt", since that can mess up the pattern
        if 'imudata.txt' in filenames:
            filenames.remove('imudata.txt')

        if filenames == []:
            self.dataFileName = "imudata1.txt"
        else:
            filenames.sort()
            filenum = [int(fn[7:-4]) for fn in filenames]
            filenum.sort()
            filenum = filenum[-1] + 1
            self.dataFileName = "imudata" + str(filenum) + ".txt"
            
