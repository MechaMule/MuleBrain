#===============================================================================
# MechaMule!
# Name(s): Johnson Le
# Date: January 24, 2019
# File: pwm.py
# Desc: library to control pwm. PWM pins are 12, 32, 33
#===============================================================================
# IMPORTS
#===============================================================================
import RPi.GPIO as IO

#===============================================================================
# Class:    PWM
# Desc:     Class for PWM
# Param:    pin = pin number. There are 3 main pwm channels.
#           for board: ch1 = pin12, ch2 = pin32, ch3 = pin33
#           for bcm: bcm18,12,13
#===============================================================================
class PWM(object):
    #===============================================================================
    # Function: PWM constructor
    # Desc:     create the pwm object with some parameters
    # Params:   f = frequency for pwm
    #           pin = what pin
    #           duty = duty cycle
    # Returns:  Nothing. Might add TRUE means success. False = failed.
    #===============================================================================
    def __init__(self, pin, freq = 1000, duty = 0):
        self.pin = pin
        self.freq = freq
        self.duty = duty
        try:
            IO.setup(self.pin, IO.OUT)
        except:
            print("ERROR: Could not initialize this PWM. IS GPIO mode set?")
            IO.cleanup()
            raise SystemExit
        self.pwm = IO.PWM(self.pin, self.freq)
        self.pwm.start(self.duty)

    #===============================================================================
    # Function: PWM_SetFrequency(self, f)
    # Desc:     Sets PWM Frequency
    # Params:   f = frequency for pwm
    # Returns:  Nothing. Might add TRUE means success. False = failed.
    #===============================================================================
    def SetFrequency(self, f):
        try:
            self.freq = f
            self.pwm.ChangeFrequency(self.freq)
        except:
            print("ERROR: Could not set frequency. Did you initialize?")
            IO.cleanup()
            raise SystemExit


    #===============================================================================
    # Function: PWM_SetDutyCycle(self, d)
    # Desc:     Sets Duty Cycle
    # Params:   d = duty cycle percentage
    # Returns:
    #===============================================================================
    def SetDutyCycle(self, d):
        self.duty = d
        self.pwm.start(self.duty)

    #===============================================================================
    # Function: Stop(self)
    # Desc:     Stops the PWM from outputting
    # Params:   none
    # Returns:  none
    #===============================================================================
    def Stop(self):
        self.pwm.stop()

    #===============================================================================
    # Function: Start(self)
    # Desc:     Restarts/Starts PWM for output
    # Params:   none
    # Returns:  none
    #===============================================================================
    def Start(self):
        self.pwm.start(freq)

    #===============================================================================
    # Function: Close(self)
    # Desc:     Cleanup IO
    # Params:   none
    # Returns:  none
    #===============================================================================
    def Clean(self):
        IO.cleanup()

if __name__ == "__main__":
    print("Running PWM test code")
    IO.setwarnings(False)
    IO.setmode(IO.BCM)
    pwm = PWM(18)
    input("press return to stop.")
    pwm.Clean()
