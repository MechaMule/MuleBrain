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
    (1) killswitch (threading.Event()) : used to detect when to end thread.
    (2) pin       (int) : help= give pin to send signal.
    (3) time_high (sec) : help= how long signal will go high
    (4) time_low  (sec) : help= how long the signal should stay low
    (5) IO_mode         : help= BCM or BOARD
    """
    def __init__(self, killswitch, pin, time_high, time_low, IO_mode = IO.BCM):
        """Constructor for Signal Class"""
        threading.Thread.__init__(self)
        self.pin = pin
        self.time_high = time_high
        self.time_low = time_low
        self.killswitch = killswitch
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
        while (self.killswitch.is_set() == False):
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


class Pulser(threading.Thread):
    """Pulser to pulse pin N times:
    (1) killswitch (threading.Event()) : used to detect when to end thread.
    (2) pin       (int) : help= give pin to send signal.
    (3) time_high (sec) : help= how long signal will go high
    (4) time_low  (sec) : help= how long the signal should stay low
    (5) amnt      (int) : help=amnt to pulse
    (5) IO_mode         : help= BCM or BOARD
    """
    def __init__(self, killswitch, pin, time_high, time_low, IO_mode = IO.BCM):
        """Constructor for Pulser"""
        threading.Thread.__init__(self)
        self.pin = pin
        self.killswitch = killswitch
        self.time_high = time_high
        self.time_low = time_low
        self.IO_mode = IO_mode

        self.amnt = 0
        self.pulseit = threading.Event()
        self.pulseit.clear()

        IO.setwarnings(False)
        IO.setmode(self.IO_mode)
        IO.setup(self.pin, IO.OUT)

        self.start()
        
    def ChangeTime(self, time_high, time_low):
        """Signal Method to update high and low time
        Parameters:
        (1) time_high (sec) : help= how long signal will go high
        (2) time_low  (sec) : help= how long the signal should stay low
        """
        self.time_high = time_high
        self.time_low = time_low

    def Pulse(self, amnt=1):
        """Pulse for N amount
        (1) amnt (int) : help= number of times to pulse
        """
        if(self.pulseit.is_set()==True):
            print("already in a pulse")
            return
        self.amnt = amnt
        self.pulseit.set()
        
    def Work(self):
        """Working thread for creating signal"""
        while (self.killswitch.is_set() == False):
            event_is_set = self.pulseit.wait()
            for i in range(0, self.amnt):
                time.sleep(self.time_low)
                IO.output(self.pin, IO.HIGH)
                time.sleep(self.time_high)
                IO.output(self.pin, IO.LOW)
            self.pulseit.clear()
        self.clean()
        print("Signal Thread Exit")


    def run(self):
        """Starts the signal thread"""
        t = threading.Thread(target=self.Work)
        t.daemon = True
        t.start()
    
    def clean(self):
        """Resets and cleans up the signal pin"""
        self.pulseit.clear()
        IO.output(self.pin, IO.LOW)
        IO.cleanup((self.pin))
#===============================================================================
# Module Main
#===============================================================================
if __name__ == '__main__':
    killme = threading.Event()
    p = 14

##    trig = Generator(closer, p, 10e-6, 60e-3)
##    trig.start()

    pulser = Pulser(killme, p, .5, .5)

    try:
        while True:
            input("enter to pulse")
            pulser.Pulse(2)
    except KeyboardInterrupt:
        pass
    finally:
        print("exit")
        killme.set()
        time.sleep(.5)
        
