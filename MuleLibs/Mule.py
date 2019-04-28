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
    def __init__(self, killswitch, pin_MTRS, pin_ECHOS):
        #store pins. might make them enum arrays.
        self.killswitch = killswitch
        self.pin_MTRS = pin_MTRS
        self.pin_ECHOS = pin_ECHOS
        self.echo = []

        #motor
        self.MTR = MOTOR(self.pin_MTRS[0], self.pin_MTRS[1], self.pin_MTRS[2], self.pin_MTRS[3])
        
        #USR
        for i in range(0, len(self.pin_ECHOS)):
            self.echo.append(Echo.ECHO(self.pin_ECHOS[i]))
        
    def clean(self):
        """Cleans up the echo and motor pins"""
        print("Initiating mule cleansing.")
        for i in range(0, len(self.pin_ECHOS)):
            self.echo[i].clean()
        self.MTR.clean()



if __name__ == '__main__':
    print("Mule says hi")
    def MapRange(x, in_min, in_max, out_min, out_max):
        return (out_min + ( ((out_max-out_min)*(x-in_min))/(in_max-in_min) ))
    try:
        killswitch = threading.Event()
        mule = MULE(killswitch, [13,6,26,19], [20,21])
        mule.MTR.Halt()
        dl = 0
        dr = 0
        minD = 2
        maxD = 3
        minspd = 20
        maxspd = 98
        while True:
            time.sleep(0.1)
            dl = mule.echo[0].GetFeet()
            dr = mule.echo[1].GetFeet()
            print("LEFT: ",dl,"   ||   RIGHT: ",dr)
            if dl<minD:
               mule.MTR.Motor_L(0)
            elif dl<maxD:     
                mule.MTR.Motor_L(MapRange(dl, minD, maxD, minspd, maxspd))
                
            if dr<minD:
               mule.MTR.Motor_R(0)
            elif dr<maxD:    
                mule.MTR.Motor_R(MapRange(dr, minD, maxD, minspd, maxspd))
            
##            print(mule.echo[0].GetInch())
            

    except KeyboardInterrupt:
        print("pressed ctrl+c")
    finally:
        print("goodbye")
        mule.MTR.Halt()
        killswitch.set()
        mule.clean()
        time.sleep(0.5)
