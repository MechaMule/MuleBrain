#===============================================================================
# MechaMule!
# Name(s): Johnson Le
# Date: January 24, 2019
# File: pwm.py
# Desc: library to control pwm. main PWM pins are 12, 32, 33
#===============================================================================
# IMPORTS
#===============================================================================
import RPi.GPIO as IO
#might want to use pigpio for pwm instead of RPi.GPIO
class PWM(object):
    """Class for controlling PWM.
    Parameters:
    (1) pin : provide pin for pwm.
    (2) freq: frequency for pwm. default = 1000.
    (3) duty: initial duty from 0-100. default = 0.
    """
    def __init__(self, pin, freq = 1000, duty = 0, IO_mode=IO.BCM):
        """Constructor for PWM class"""
        self.pin = pin
        self.freq = freq
        self.duty = duty
        self.IO_mode = IO_mode

        #set up the GPIO
        IO.setwarnings(False)
        IO.setmode(self.IO_mode)
        #set up pin
        IO.setup(self.pin, IO.OUT)
        #create pwm
        self.pwm = IO.PWM(self.pin, self.freq)
        self.pwm.start(self.duty)

    def SetFrequency(self, freq):
        """PWM Method for changing frequency.
        Parameters:
        (1) f : change frequency of signal
        """
        self.freq = freq
        self.pwm.ChangeFrequency(self.freq)

    def SetDutyCycle(self, duty):
        """PWM Method for changing duty cycle.
        Parameters:
        (1) duty : change duty cycle of signal
        """
        self.duty = duty
        self.pwm.start(self.duty)

    def Stop(self):
        """PWM Method for stopping PWM"""
        self.pwm.stop()

    def Start(self):
        """PWM method for starting PWM"""
        self.pwm.start(freq)

    def clean(self):
        """clean up the pwm io pin"""
        IO.cleanup((self.pin))

if __name__ == "__main__":
    print("Running PWM test code")
    pwm = PWM(18,1000,50)
    input("press return to stop.")
    pwm.clean()
