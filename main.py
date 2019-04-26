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
from Mule import *
from bluedot.btcomm import BluetoothServer

#===============================================================================
# Methods
#===============================================================================
def qworker(stopper):
    """Thread Method to process the queue"""
    while (stopper.is_set() == False):
        event = q1.get()
        if event == "STOP" or event == "0":
            stopper.set()
        else:
            print("Useless Press: ", event)
        q1.task_done()

def MapRange(x, in_min, in_max, out_min, out_max):
    return (out_min + ( ((out_max-out_min)*(x-in_min))/(in_max-in_min) ))

def bt_received(data):
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
    mule = MULE(killswitch, [13,6,26,19], [20])

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

    try:
        while True:
            time.sleep(0.5)

    except KeyboardInterrupt:
        pass
    finally:
        print("Closing Main")
        killswitch.set()
        mule.clean()
        time.sleep(.5)
