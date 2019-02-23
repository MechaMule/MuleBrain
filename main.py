#===============================================================================
# MechaMule!
# Name(s):  Johnson Le
# Date: February 17, 2019
# File: Main.py
# Desc: The main file that initializes everything for the mule.
#===============================================================================
# IMPORTS
#===============================================================================
import sys
sys.path.insert(0, './MuleLibs')

from queue import Queue
import Keyboard
import threading
import time
import Signal
import Echo
from MuleMotor_Functions import MOTOR
##from bluedot.btcomm import BluetoothServer

#===============================================================================
# Methods
#===============================================================================
def qworker(stopper):
    """Thread Method to process the queue"""
    while (stopper.is_set() == False):
        print(q1.get())
        q1.task_done()

def MapRange(x, in_min, in_max, out_min, out_max):
    return (out_min + ( ((out_max-out_min)*(x-in_min))/(in_max-in_min) ))

def bt_received(data):
    pass
#===============================================================================
# MAIN MAIN
#===============================================================================
if __name__ == '__main__':
    closer = threading.Event()
    #declare pins
    p_trig = 5
    p_mtrL = 13
    p_mtrR = 6
    p_dirL = 16
    p_dirR = 20
    p_echoL = 26
    p_echoR = 19
    

    #creating the trigger signal
    trig = Signal.Generator(closer, p_trig, 10E-6, 60E-3)
    trig.start()

    #creating threaded queue
    q1 = Queue(maxsize=0)
    for i in range(1): #change to increase num of threads for processing queue.
        t = threading.Thread(target=qworker, kwargs=dict(stopper=closer))
        t.daemon = True
        t.start()

    #creating threaded keyboard. has access to the queue
    kb = Keyboard.KB(closer,q1)
    kb.start()

    #create echo object for the ping sensor don't forget to clean
    echoL = Echo.ECHO(p_echoL)
    echoR = Echo.ECHO(p_echoR)

    #create h-bridge motor control class
    mtr = MOTOR(p_mtrL, p_mtrR, p_dirL, p_dirR)

    #create bt server host
    bts = BluetoothServer(bt_recieved)

    try:
        while(closer.is_set()==False):
            L = 2*echoL.GetInch()
            R = 2*echoR.GetInch()
            l = 0
            r = 0
            if L < R:
                l = 20
            if R < L:
                r = 20
            print(L, "||", R)
            if(L <= 12 or L >= 60):
                mtr.Motor_L(0)
            else:
                mtr.Motor_L(l+MapRange(L, 12, 60, 30, 70))
                
            if(R <= 12 or R >= 60):
                mtr.Motor_R(0)
            else:
                mtr.Motor_R(r+MapRange(L, 12, 60, 30, 70))
            time.sleep(0.5)
    except KeyboardInterrupt:
        pass
    finally:
        print("closing program in .5 seconds")
        echoL.clean()
        echoR.clean()
        mtr.clean()
        closer.set()
        time.sleep(.5)
