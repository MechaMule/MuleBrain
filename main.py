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
import RPi.GPIO as IO

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

        elif event == "go1":
            bts.send("go1")
        elif event == "go2":
            mule.pulser.Pulse(100)
            
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

def cb(channel):
##    p.Pulse(1000)
    mule.trigger.start()
    
#===============================================================================
# MAIN MAIN
#===============================================================================
if __name__ == '__main__':
    print("Mule starting up!")
    #initialize killswitch and pins for mule
    killswitch = threading.Event()
    mule = MULE(26, 19, 13, 6, \
                12, 21, 22, 23, 24, \
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
##        while(killswitch.is_set()==False):
##            time.sleep(0.5)
##            print(2*mule.echoL1.GetInch())


        ####RANDO TEST
##        p = Signal.Pulser(killswitch, 12, 10E-6, 60E-3)
        IO.setwarnings(False)
        IO.setmode(IO.BCM)
        IO.setup(19, IO.IN, pull_up_down=IO.PUD_DOWN)

        IO.add_event_detect(19, IO.RISING, cb, 300)
        while(killswitch.is_set()==False):
            time.sleep(0.5)

    except KeyboardInterrupt:
        pass
    finally:
        print("Closing Main")
        killswitch.set()
        mule.clean()
        IO.cleanup((26))
        time.sleep(.5)
