#===============================================================================
# MechaMule!
# Name(s):  Johnson Le
# Date: February 17, 2019
# File: Keyboard.py
# Desc: Handles keyboard presses
#===============================================================================
# IMPORTS
#===============================================================================
from pynput import keyboard
from queue import Queue
import time
import threading

class KB(threading.Thread):
    """Threaded Keyboard Event detection handling thread.
    Parameters:
    (1) stopper : threaded event for stopping threads
    (2) q : the queue to place the keyboard stuff too
    """
    def __init__(self, stopper, q):
        """Constructor for Keyboard Threaded Class"""
        threading.Thread.__init__(self)
        self.q = q
        self.stopper = stopper
        self.listener = keyboard.Listener(on_press=self.on_press)

    def on_press(self, key):
        """When keyboard press caught. Stores key into queue."""
        try:
            if key == keyboard.Key.esc:
                self.stopper.set()
                self.listener.stop()
                print("ESC pressed")
                raise MyException(key)
            self.q.put(key.char)
        except AttributeError:
            print('special key {0} pressed'.format(
                key))

    def run(self):
        """Starts the keyboard detection thread"""
        self.listener.start()

#===============================================================================
# Module Main
#===============================================================================
if __name__ == '__main__':
    def qworker(stopper):
        while (stopper.is_set() == False):
            print(q1.get())
            q1.task_done()

    q1 = Queue(maxsize=0)
    closer = threading.Event()
    for i in range(3):
        t = threading.Thread(target=qworker, kwargs=dict(stopper=closer))
        t.daemon = True
        t.start()

    kb = KB(closer, q1)
    kb.start()

    try:
        while (closer.is_set() == False):
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        print("closing program in .5 seconds")
        time.sleep(.5)
