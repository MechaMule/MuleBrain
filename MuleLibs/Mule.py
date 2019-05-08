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
    f = open("../Log/log.txt", "w+")
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

        Mmax = 50
        Mmin = 15
        dGoal = 3
        Kp = 2
        Bmax = Mmax - (Kp*mule.eargap)
        idle = True
        mL = mR = 0

        time.sleep(.5)
        while True:
            time.sleep(.1)
            dL = mule.echo[0].GetFeet()
            dR = mule.echo[1].GetFeet()
            dc = (dL+dR)/2
            if idle==True:
                if dc >= dGoal +1:
                    idle = False
                else:
                    pass #swivel?
            else:
                if dc >= dGoal:
                    mb = MapRange(dc, [dGoal, dGoal+3], [Mmin,Bmax-1]) 
                    mule.MTR.Motor_L(mb + Kp*(0-(dR-dL)))
                    mule.MTR.Motor_R(mb + Kp*(0-(dL-dR)))
                else:
                    mule.MTR.Halt()
                    idle = True

            print("dL: ",dL,"   ||   dR: ",dR,"   ||   mL: ",round(mule.MTR.GetLSpeed(),3),"  ||  mR: ",round(mule.MTR.GetRSpeed(),3))
            f.write(str(dL)+","+str(dR)+","+str(round(mule.MTR.GetLSpeed(),3))+","+str(round(mule.MTR.GetRSpeed(),3))+"\n")
            


    except KeyboardInterrupt:
        print("pressed ctrl+c")
    finally:
        print("goodbye")
        f.close()
        mule.MTR.Halt()
        killswitch.set()
        mule.clean()
        time.sleep(0.5)
