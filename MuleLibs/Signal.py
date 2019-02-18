#===============================================================================
# MechaMule!
# Name(s):  Johnson Le
# Date: February 17, 2019
# File: Signal.py
# Desc: library to generate square signals.
#===============================================================================
# IMPORTS
#===============================================================================
import threading
import time
import RPi.GPIO as IO

#===============================================================================
# Main Object Thread
#===============================================================================
class Generator(threading.Thread):
    """This thread class loops a pin high for some time and low for some time.
    Parameters:
    (1) closer (threading.Event()) : used to detect when to end thread.
    (2) pin       (int) : help= give pin to send signal.
    (3) time_high (sec) : help= how long signal will go high
    (4) time_low  (sec) : help= how long the signal should stay low
    (5) IO_mode         : help= BCM or BOARD
    """
    def __init__(self, stopper, pin, time_high, time_low, IO_mode = IO.BCM):
        """Constructor for Signal Class"""
        threading.Thread.__init__(self)
        self.pin = pin
        self.time_high = time_high
        self.time_low = time_low
        self.stopper = stopper
        self.IO_mode = IO_mode

        IO.setwarnings(False)
        IO.setmode(self.IO_mode)
        IO.setup(self.pin, IO.OUT)

    def ChangeTime(self, time_high, time_low):
        """Signal Method to update high and low time
        Parameters:
        (1) time_high (sec) : help= how long signal will go high
        (2) time_low  (sec) : help= how long the signal should stay low
        """
        self.time_high = time_high
        self.time_low = time_low

    def Work(self):
        """Working thread for creating signal"""
        while (self.stopper.is_set() == False):
            time.sleep(self.time_low)
            IO.output(self.pin, IO.HIGH)
            time.sleep(self.time_high)
            IO.output(self.pin, IO.LOW)
        self.clean()
        print("Signal Thread Exit")


    def run(self):
        """Starts the signal thread"""
        t = threading.Thread(target=self.Work)
        t.daemon = True
        t.start()

    def clean(self):
        """Resets and cleans up the signal pin"""
        IO.output(self.pin, IO.LOW)
        IO.cleanup((self.pin))

#===============================================================================
# Module Main
#===============================================================================
if __name__ == '__main__':
    closer = threading.Event()
    p = 26

    trig = Generator(closer, p, 10e-6, 60e-3)
    trig.start()

    try:
        input("press to stop")
        closer.set()
    except KeyboardIntterupt:
        pass
    finally:
        print("exit")
        closer.set()
        time.sleep(.5)
        IO.cleanup()
