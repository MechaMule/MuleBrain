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
from bluedot.btcomm import BluetoothServer
from simple_pid import PID
from MuleMotor_Functions import MOTOR
from queue import Queue

def MapRange(x, old, new):
        out = (new[0] + ( ((new[1]-new[0])*(x-old[0]))/(old[1]-old[0]) ))
        if out <= new[0]:
            return new[0]
        elif out >= new[1]:
            return new[1]
        return out

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

        #motor controllers
        self.pidL = PID(0, 0, 0, setpoint=0)
        self.pidR = PID(0, 0, 0, setpoint=0)
        self.pidL.auto_mode = True
        self.pidR.auto_mode = True
        
        #USR
        for i in range(0, len(self.pin_ECHOS)):
            self.echo.append(Echo.ECHO(self.pin_ECHOS[i]))

        #bluetooth
        self.bts = BluetoothServer(self.bt_received)

        #threaded queue
        self.queue = Queue(maxsize=0)
        for i in range(2):
            t = threading.Thread(target=self.qworker)#, kwargs=dict(stopper=self.killswitch))
            t.daemon = True
            t.start()

        #user configuration?:
        self.dGoal = 5

    def PIDConfig(self, K, lim):
        """Updates both PIDs gains and limits
        (1) K : Kp, Ki, Kd
        (2) lim : changes limits for pid output
        """
        self.pidL.tunings = (K[0], K[1], K[2])
        self.pidR.tunings = (K[0], K[1], K[2])
        self.pidL.output_limits = (lim[0], lim[1])
        self.pidR.output_limits = (lim[0], lim[1])

    def bt_received(self, data):
        self.queue.put(data)

    def qworker(self):
        while (self.killswitch.is_set() == False):
            event = self.queue.get()
            if (event == "STOP"):
                self.dGoal = 999

            elif (event == "RIGHT"):
                pass
            
            elif (event == "LEFT"):
                pass
            
            elif (event == "ONE80"):
                pass
            
            elif (event == "DIST_5FT"):
                self.dGoal = 5

            elif (event == "DIST_10FT"):
                self.dGoal = 10
                
            elif (event == "DIST_15FT"):
                self.dGoal = 15
##            print(event)
            self.queue.task_done()

    def clean(self):
        """Cleans up the echo and motor pins"""
        print("Initiating mule cleansing.")
        for i in range(0, len(self.pin_ECHOS)):
            self.echo[i].clean()
        self.MTR.clean()


if __name__ == '__main__':
    print("Mule says hi")
    import math
    
##    f = open("../Log/log.txt", "w+")

    try:
        killswitch = threading.Event()
        mule = MULE(killswitch, [6,13,19,26], [20,21])
        mule.MTR.Halt()
        
        state_idle, state_follow, state_leftCorner, state_rightCorner = 0,1,2,3
        state = state_idle

        x_axis, y_mL, y_mR, y_dL, y_dR , y_dGoal, y_mb= [], [], [], [], [], [], []
        sample_t = 1E-1
        iteration = 0

        Mmin, Mmax = 50, 69
        adjL = adjR = dL = dR = mb = mL = mR = motor_offset = 0
                
        mule.PIDConfig([50, 0, 5], [-50,50])

        time.sleep(0.5)
##        input("enter to start")
        while True:
            time.sleep(sample_t)
            dL = mule.echo[0].GetFeet()
            dR = mule.echo[1].GetFeet()
            dc = (dL+dR)/2
            if state == state_idle:
                if dc >= mule.dGoal+2:
                    state = state_follow
                    mule.PIDConfig([50, 0, 0], [-24,24])
                    mb = 40
                    motor_offset = 18
                else:
##                    mb = 0
##                    adjR = 0
##                    adjL = 0
                    adjR = mule.pidL(dR-dL)
                    adjL = mule.pidR(dL-dR)

                    
            elif state == state_follow:
                if dc >= mule.dGoal:
##                    mb = 50 #will need to change later to match distance to user
                    adjR = mule.pidL(dR-dL)
                    adjL = mule.pidR(dL-dR)
                else:
                    state = state_idle
                    mL = mR = mb = motor_offset = 0
                    mule.MTR.Halt()
                    mule.PIDConfig([50, 0, 5], [-50,50])
                    
            elif state == state_leftCorner:
                pass
            
            elif state == state_rightCorner:
                pass

            mL = mb + adjL + motor_offset
            mR = mb + adjR
            mule.MTR.Motor_L(mL - motor_offset)
            mule.MTR.Motor_R(mR)
            
            x_axis += [round(iteration * sample_t,3)]
            y_dGoal.append(round(mule.dGoal,3))
            y_mb.append(round(mb,3))
            y_dL.append(round(dL,3))
            y_dR.append(round(dR,3))
            y_mL.append(round(mL,3))
            y_mR.append(round(mR,3))
            iteration += 1

##            print("Distance: ", round(dL,3), "   ||   ", round(dR,3))

            
    except KeyboardInterrupt:
        mule.MTR.Halt()
        killswitch.set()
        mule.clean()

        plt.figure(1)
        plt.subplot(2,1,1)
        plt.title('Distance vs. Time', size = 20)
        plt.plot(x_axis, y_dL, label='Left Distance')
        plt.plot(x_axis, y_dR, label='Right Distance')
        plt.tick_params(axis='x', labelsize=12)
        plt.tick_params(axis='y', labelsize=12)
        plt.plot(x_axis, y_dGoal, label='Goal Distance', color='#A0A0A0', linestyle='dashed')
##        plt.xlabel('time(s)', size = 16)
        plt.ylabel('Distance(ft)', size = 16)
        plt.legend(prop={'size': 10})
        plt.show

##        plt.figure(2)
        plt.subplot(2,1,2)
        plt.title('Motor PWM vs. Time', size = 20)
        plt.plot(x_axis, y_mL, label='Left Motor')
        plt.plot(x_axis, y_mR, label='Right Motor')
        plt.plot(x_axis, y_mb, label='Moter Bias', color='#A0A0A0', linestyle='dashed')
        plt.tick_params(axis='x', labelsize=12)
        plt.tick_params(axis='y', labelsize=12)
        plt.xlabel('time(s)', size = 16)
        plt.ylabel('Motor Speeds(pwm)', size = 16)
        plt.legend(prop={'size': 10})
        plt.show()

    finally:
        print("Goodbye")
        time.sleep(0.5)
    
    
