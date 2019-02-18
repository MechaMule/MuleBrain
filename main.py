import sys
sys.path.insert(0, './MuleLibs')

from queue import Queue
import Keyboard
import threading
import time
import Signal
import math


def qworker(stopper):
    """Thread Method to process the queue"""
    while (stopper.is_set() == False):
        print(q1.get())
        q1.task_done()

if __name__ == '__main__':
    #declare pins
    p_trig = 13
    p_echo = 19
    
    #creating threaded queue
    q1 = Queue(maxsize=0)
    closer = threading.Event()
    for i in range(3):
        t = threading.Thread(target=qworker, kwargs=dict(stopper=closer))
        t.daemon = True
        t.start()

    #creating threaded keyboard. has access to the queue
    kb = Keyboard.KB(closer,q1)
    kb.start()

    #creating the trigger signal
    trig = Signal.Generator(closer, p_trig, 10E-6, 10E-6)
    trig.start()
    
    
    try:
        while(closer.is_set()==False):
            time.sleep(1)
            pass
    except KeyboardInterrupt:
        pass
    finally:
        print("closing program in .5 seconds")
        time.sleep(.5)
