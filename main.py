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
from Mule import *
from MuleMotor_Functions import MOTOR
from bluedot.btcomm import BluetoothServer

#===============================================================================
# Methods
#===============================================================================
def qworker(stopper):
    """Thread Method to process the queue"""
    while (stopper.is_set() == False):
        event = q1.get()

        if event == "START":
            print("BT link success. Starting trigger signals.")
            global btsuccess
            btsuccess = True
            
        elif event == "STOP" or event == "0":
            stopper.set()
            
        elif event == "go":
            mule.pulser.Pulse()
            
        elif event == "DIST_5" or event == "1":
            pass
        
        else:
            print("Useless Press: ", event)
        q1.task_done()

def MapRange(x, in_min, in_max, out_min, out_max):
    return (out_min + ( ((out_max-out_min)*(x-in_min))/(in_max-in_min) ))

def bt_received(data):
##    bts.send(data)
    q1.put(data)
    
#===============================================================================
# MAIN MAIN
#===============================================================================
if __name__ == '__main__':
    print("Mule starting up!")
    #initialize killswitch and pins for mule
    killswitch = threading.Event()
    mule = MULE(26, 19, 13, 6, \
                17, 27, 22, 23, 24, \
                killswitch)

    #creating threaded queue
    q1 = Queue(maxsize=0)
    for i in range(2): #change to increase num of threads for processing queue.
        t = threading.Thread(target=qworker, kwargs=dict(stopper=killswitch))
        t.daemon = True
        t.start()

    #creating threaded keyboard. has access to the queue
    kb = Keyboard.KB(killswitch,q1)
    kb.start()

    #create bt server host
    bts = BluetoothServer(bt_received)

    #variables
    btsuccess = False

    try:
##        print("Waiting for bt link")
##        while(btsuccess == False and killswitch.is_set()==False):
##            pass
##        mule.trigger.start() #btsucess true so start trigger.
        while(killswitch.is_set()==False):
            time.sleep(0.5)
            print(2*mule.echoL1.GetInch())

    except KeyboardInterrupt:
        pass
    finally:
        print("Closing Main")
        mule.MTR.Halt()
        killswitch.set()
        mule.clean()
        time.sleep(.5)
