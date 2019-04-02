#===============================================================================
# MechaMule!
# Name(s):  Johnson Le
# Date: March 31, 2019
# File: Mule.py
# Desc: Hold settings for the mule. No handling.
#===============================================================================
# IMPORTS
#===============================================================================
import Echo
import Signal
import threading
import time
from MuleMotor_Functions import MOTOR

class MULE(object):
    def __init__(self, pin_dirL, pin_dirR, pin_mtrL, pin_mtrR, \
                 pin_trig, pin_echoL1, pin_echoL2, pin_echoR1, pin_echoR2, \
                 killswitch, speed_default=20, speed_max=100, \
                 speed_max_offset=30, dist_bot=5, \
                 trig_hi=10E-6, trig_lo=60E-3):

        #store pins. might make them enum arrays.
        self.pin_dirL = pin_dirL
        self.pin_dirR = pin_dirR
        self.pin_mtrL = pin_mtrL
        self.pin_mtrR = pin_mtrR
        self.pin_trig = pin_trig
        self.pin_echoL1 = pin_echoL1
        self.pin_echoL2 = pin_echoL2
        self.pin_echoR1 = pin_echoR1
        self.pin_echoR2 = pin_echoR2
        self.killswitch = killswitch

        #main settings for 
        self.speed_default = speed_default
        self.speed_max = speed_max
        self.speed_max_offset = speed_max_offset
        self.dist_bot = dist_bot
        self.trig_hi = trig_hi
        self.trig_lo = trig_lo

        #ping stuff. need to start trigger. echo works right away.
##        self.trigger = Signal.Generator(self.killswitch, self.pin_trig, self.trig_hi, self.trig_lo)
        self.pulser = Signal.Pulser(self.killswitch, self.pin_trig, 0.5, 0.5)
        self.echoL1 = Echo.ECHO(self.pin_echoL1)
##        self.echoR1 = Echo.ECHO(self.pin_echoR1)
##        self.echoL2 = Echo.ECHO(self.pin_echoL2)
##        self.echoR2 = Echo.ECHO(self.pin_echoR2)

        #motor
        self.MTR = MOTOR(self.pin_mtrL, self.pin_mtrR, self.pin_dirL, self.pin_dirR)
        
    def clean(self):
        print("Initiating mule cleansing.")
        self.echoL1.clean()
##        self.echoL2.clean()
##        self.echoR1.clean()
##        self.echoR2.clean()
        self.MTR.clean()
            
        
        

if __name__ == '__main__':
    print("Mule says hi")
    killswitch = threading.Event()
    mule = MULE(26, 19, 13, 6, \
                17, 27, 22, 23, 24, \
                killswitch)
##    mule.trigger.start()
    mule.MTR.Halt()
    mule.MTR.Motor_L(-30)
    mule.MTR.Motor_R(-80)

    try:
        while True:
            input("enter to pulse")
            mule.pulser.Pulse(3)
    except KeyboardInterrupt:
        pass
    finally:
        mule.MTR.Halt()
        killswitch.set()
        mule.clean()
        time.sleep(0.5)
            
    

        
