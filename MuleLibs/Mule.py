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
import matplotlib.pyplot as plt
from simple_pid import PID
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
        out = (new[0] + ( ((new[1]-new[0])*(x-old[0]))/(old[1]-old[0]) ))
        if out <= new[0]:
            return new[0]
        elif out >= new[1]:
            return new[1]
        return out
    try:
        killswitch = threading.Event()
        mule = MULE(killswitch, [6,13,19,26], [20,21])
        mule.MTR.Halt()

        Kp, Ki, Kd = 10, 0, 0
        
        Mmax = 70
        Mmin = 30
        dGoal = 3
        idle = True
        mb = mL = mR = 0
        dL = dR = 0
        adjL = adjR = 0
        motor_offset = 0

        pidL = PID(Kp, Ki, Kd, setpoint=0)
        pidR = PID(Kp, Ki, Kd, setpoint=0)

        pidL.tunings = (99, 0, 10)
        pidR.tunings = (99, 0, 10)
        pidL.output_limits = (-99, 99)
        pidR.output_limits = (-99, 99)
        
        pidL.auto_mode = True
        pidR.auto_mode = True

        x_axis, y_mL, y_mR, y_dL, y_dR = [], [], [], [], []
        
        time.sleep(0.5)
        iteration = 0
        while True:
            time.sleep(1E-1)
            dL = mule.echo[0].GetFeet()
            dR = mule.echo[1].GetFeet()
            dc = (dL+dR)/2
            if idle==True:
                if dc >= dGoal + 2:
                    idle = False
                    pidL.tunings = (10, 0, 0.5)
                    pidR.tunings = (10, 0, 0.5)
                    pidL.output_limits = (-15, 30)
                    pidR.output_limits = (-15, 30)
##                    mule.MTR.Motor_L(80)
##                    mule.MTR.Motor_R(80-motor_offset)
                else:
                    mb = 0
                    adjL = pidL(dR-dL)
                    adjR = pidR(dL-dR)
            else:
                if dc >= dGoal:
                    mb = MapRange(dc, [dGoal, dGoal+10], [Mmin,Mmax])
                    adjL = pidL(dR-dL)
                    adjR = pidR(dL-dR)
                    
##                    mule.MTR.Motor_L((mb + Kp*(0-(dR-dL))))
##                    mule.MTR.Motor_R((mb + Kp*(0-(dL-dR))) - motor_offset)
                else:
                    mL = 0
                    mR = 0
                    mule.MTR.Halt()
                    idle = True
                    pidL.tunings = (99, 0, 10)
                    pidR.tunings = (99, 0, 10)
                    pidL.output_limits = (-99, 99)
                    pidR.output_limits = (-99, 99)
                    
            mL = mb + adjL
            mR = mb + adjR
            mule.MTR.Motor_L(mL)
            mule.MTR.Motor_R(mR)
            
            x_axis += [round(iteration * 1E-1,1)]
            y_dL.append(round(dL,3))
            y_dR.append(round(dR,3))
            y_mL.append(round(mL,3))
            y_mR.append(round(mR,3))
            iteration += 1 
            
            print("Distance: ", round(dL,3), "   ||   ", round(dR,3))
            
##            print("d: [",dL,",",dR,"]   ||   m: [",round(mule.MTR.GetLSpeed(),3),",",round(mule.MTR.GetRSpeed(),3),"]")
##            # f.write(str(dL)+","+str(dR)+","+str(round(mule.MTR.GetLSpeed(),3))+","+str(round(mule.MTR.GetRSpeed(),3))+"\n")



    except KeyboardInterrupt:
        print("pressed ctrl+c")
        f.close()
        mule.MTR.Halt()
        killswitch.set()
        mule.clean()
        
        plt.subplot(2,1,1)
        plt.plot(x_axis, y_dL, label='dL')
        plt.plot(x_axis, y_dR, label='dR')
        plt.xlabel('time')
        plt.ylabel('distance')
        plt.legend()

        plt.subplot(2,1,2)
        plt.plot(x_axis, y_mL, label='mL')
        plt.plot(x_axis, y_mR, label='mR')
        plt.xlabel('time')
        plt.ylabel('Motor Speed')
        plt.legend()
        plt.show()
    finally:
        print("goodbye")
        time.sleep(0.5)
