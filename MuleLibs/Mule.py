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
    """Holds pins and setings for Mule.
    Parameters:
    (1) killswitch : Thread event to close all threads
    (2) pin_MTRS   : Array holding motor pins. enL, enR, dirL, dirR
    (3) pin_trig   : Int. Trigger pin
    (4) pin_ECHOS  : Array. Holds all echo pins. Ideally from left to right
    """
    def __init__(self, killswitch, pin_MTRS, pin_trig, pin_ECHOS, trig_hi=20E-6, trig_lo=120E-3):
        #store pins. might make them enum arrays.
        self.killswitch = killswitch
        self.pin_MTRS = pin_MTRS
        self.pin_trig = pin_trig
        self.pin_ECHOS = pin_ECHOS
        
        #main settings for 
        self.trig_hi = trig_hi
        self.trig_lo = trig_lo
        
        #ping stuff. need to start trigger. echo works right away.
        self.pulser = Signal.Pulser(self.killswitch, self.pin_trig, self.trig_hi, self.trig_lo)
        for i in range(0, len(self.pin_ECHOS)):
            self.echo[i] = Echo.ECHO(self.pin_ECHOS[i])
            
        #motor
        self.MTR = MOTOR(self.pin_MTRS[0], self.pin_MTRS[1], self.pin_MTRS[2], self.pin_MTRS[3])
        
    def clean(self):
        """Cleans up the echo and motor pins"""
        print("Initiating mule cleansing.")
        for i in range(0, len(self.pin_ECHOS)):
            self.echo[i].clean()
        self.MTR.clean()
            
        
        

if __name__ == '__main__':
    print("Mule says hi")
    try:
        killswitch = threading.Event()
        mule = MULE(killswitch, [13,6,26,19], 17, [])
        mule.MTR.Halt()
        mule.MTR.Motor_L(-30)
        mule.MTR.Motor_R(-80)
        while True:
            time.sleep(1)
        
    except KeyboardInterrupt:
        print("pressed ctrl+c")
    finally:
        print("goodbye")
        mule.MTR.Halt()
        killswitch.set()
        mule.clean()
        time.sleep(0.5)

            
    

        
