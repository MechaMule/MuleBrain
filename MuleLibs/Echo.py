#===============================================================================
# MechaMule!
# Name(s):  Johnson Le
# Date: February 17, 2019
# File: Echo.py
# Desc: Module for catching echo for HC-SR04
#===============================================================================
# IMPORTS
#===============================================================================
import RPi.GPIO as IO
import time
import math
import threading

#===============================================================================
# Main Object Class
#===============================================================================
class ECHO(object):
    """ECHO class will catch hardware changes ie the echo.
    Parameters:
    (2) pin   (int) : help= give pin number
    (4) temp  (sec) : default = 20,     help= temperature in celsius
    (5) IO_mode     : default = IO.BCM, help= BCM or BOARD
    """
    def __init__(self, pin, temp=20, IO_mode=IO.BCM):
        """Constructor for ECHO Class"""
        self.pin = pin
        self.temp = temp # temperature in celsius
        self.IO_mode = IO_mode

        self.t_start = 0    #just used for holding time when echo start
        self.TOF = 0    #raw time of flight in seconds
        self.dist = 0   #raw distance in meters


        self.speed_of_sound = 331.3 * math.sqrt(1+(self.temp / 273.15)) #m/s
        self.timeout = 6 / self.speed_of_sound
        self.TOF_1m = 1 / self.speed_of_sound

        self.arr = [0]*10
        self.i = 0

        IO.setwarnings(False)
        IO.setmode(self.IO_mode)
        IO.setup(self.pin, IO.IN, pull_up_down=IO.PUD_UP)

        IO.add_event_detect(self.pin, IO.BOTH, callback=self.callback)


    def callback(self, channel):
        """Function to be called caught a pin state changesself.
        Calculates time of flight and distance in meters"""
        if(self.i >=10):
            self.i=0
        if (IO.input(self.pin) == IO.HIGH):
            self.t_start = time.time()
        elif (IO.input(self.pin) == IO.LOW):
            tof = time.time() - self.t_start
            if((self.TOF == 0 and tof<self.timeout) or tof < self.TOF + self.TOF_1m):
                self.TOF = tof
                self.arr[self.i]=self.TOF * ((self.speed_of_sound)/(2)) #note div 2
                self.i+=1
                self.dist = sum(self.arr)/len(self.arr)
##                self.dist = self.TOF * ((self.speed_of_sound)/(2)) #note div 2


    def GetMeters(self):
        return round(self.dist, 5)

    def GetFeet(self):
        return round(self.dist * 3.28084, 5)

    def GetInch(self):
        return round(self.dist * 3.28084 * 12, 5)

    def clean(self):
        """Resets and cleans up the echo pin"""
        IO.cleanup((self.pin))

#===============================================================================
# Module Main
#===============================================================================
if __name__ == '__main__':
    import Signal
    p_trig = 5
    p_echoL = 13
    p_echoR = 24
    closer = threading.Event()

    trig = Signal.Generator(closer, p_trig, 10E-6, 60E-3)
    trig.start()

    echoL = ECHO(p_echoL)
    echoR = ECHO(p_echoR)

    try:
        while True:
            print(2*echoL.GetInch(), "||", 2*echoR.GetInch())
            time.sleep(0.5)
    except KeyboardInterrupt:
        pass
    finally:
        echoL.clean()
        echoR.clean()
        print("exiting")
