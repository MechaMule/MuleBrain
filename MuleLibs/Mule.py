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
    def __init__(self, killswitch, pin_MTRS, pin_ECHOS, eargap=13/12):
        #store pins. might make them enum arrays.
        self.killswitch = killswitch
        self.pin_MTRS = pin_MTRS
        self.pin_ECHOS = pin_ECHOS
        self.echo = []
        self.eargap = 13

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
    import math
    def MapRange(x, old, new):
        if x<=old[0]:
            return 0
        elif x>=old[1]:
            return new[1]
        return(new[0] + ( ((new[1]-new[0])*(x-old[0]))/(old[1]-old[0]) ))

    try:
        killswitch = threading.Event()
        mule = MULE(killswitch, [13,6,26,19], [20,21])
        mule.MTR.Halt()

        Mmax = 95-7
        Mmin = 0
        dGoal = 4
        Kp = 10
        Bmax = Mmax - (Kp*mule.eargap)

        while True:
            time.sleep(.1)
            dL = mule.echo[0].GetFeet()
            dR = mule.echo[1].GetFeet()
            dc = (dL+dR)/2
            mb = MapRange(dc, [dGoal-2, dGoal+5], [Mmin,Mmax])

            mL = mb + Kp*(0-(dR-dL))
            mR = mb + Kp*(0-(dL-dR))

            mule.MTR.Motor_L(mL)
            mule.MTR.Motor_R(mR-7)

            print("dL: ",dL,"   ||   dR: ",dR,"   ||   mL: ",round(mL,3),"  ||  mR: ",round(mR,3))
            


    except KeyboardInterrupt:
        print("pressed ctrl+c")
    finally:
        print("goodbye")
        mule.MTR.Halt()
        killswitch.set()
        mule.clean()
        time.sleep(0.5)
