import sys
sys.path.insert(0, './MuleLibs')

from queue import Queue
import Keyboard
import threading
import time

def qworker(stopper):
    """Thread Method to process the queue"""
    while (stopper.is_set() == False):
        print(q1.get())
        q1.task_done()

if __name__ == '__main__':
    q1 = Queue(maxsize=0)
    closer = threading.Event()
    for i in range(3):
        t = threading.Thread(target=qworker, kwargs=dict(stopper=closer))
        t.daemon = True
        t.start()

    kb = Keyboard.KB(closer,q1)
    kb.start()

    try:
        while(closer.is_set()==False):
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        print("closing program in .5 seconds")
        time.sleep(.5)
