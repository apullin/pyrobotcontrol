def verifyAllMotorGainsSet(ROBOTS_LIST):
    #Verify all robots have motor gains set
    for r in ROBOTS_LIST:
        if not(r.motor_gains_set):
            print "CRITICAL : Could not SET MOTOR GAINS on robot 0x%04X" % r.DEST_ADDR_int
            xb_safe_exit()

def verifyAllSteeringGainsSet(ROBOTS_LIST):
    #Verify all robots have motor gains set
    for r in ROBOTS_LIST:
        if not(r.steering_gains_set):
            print "CRITICAL : Could not SET STEERING GAINS on robot 0x%04X" % r.DEST_ADDR_int
            xb_safe_exit()
            
def verifyAllSteeringRateSet(ROBOTS_LIST):
    #Verify all robots have motor gains set
    for r in ROBOTS_LIST:
        if not(r.steering_gains_set):
            print "CRITICAL : Could not SET STEERING GAINS on robot 0x%04X" % r.DEST_ADDR_int
            xb_safe_exit()
            
def verifyAllTailGainsSet(ROBOTS_LIST):
    #Verify all robots have motor gains set
    for r in ROBOTS_LIST:
        if not(r.tail_gains_set):
            print "CRITICAL : Could not SET TAIL GAINS on robot 0x%04X" % r.DEST_ADDR_int
            xb_safe_exit()
            
def verifyAllQueried(ROBOTS_LIST):            
    for r in ROBOTS_LIST:
        if not(r.robot_queried):
            print "CRITICAL : Could not query robot 0x%02X" % r.DEST_ADDR_int
            xb_safe_exit()
