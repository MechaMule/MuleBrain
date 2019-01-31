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
# Param:    ch = channel. There are 3 pwm channels.
#           for board: ch1 = pin12, ch2 = pin32, ch3 = pin33
#           for bcm: bcm18,12,13
#===============================================================================
class PWM:
    def __init__(self, ch):
        #mapping channels to gpio pins
        if ch > 3:
            print("ERROR: Only 3 PWM channels.")
            raise SystemExit
        self.ch = ch
        if ch == 1:
            self.pin = 12
        elif ch == 2:
            self.pin = 32
        elif ch == 3:
            self.pin = 33

    #===============================================================================
    # Function: Init(self, f)
    # Desc:     Initialize PWM. Sets pin active. Starts at 0% duty cycle.
    # Params:   f = frequency that pwm will be set too.
    # Returns:  TRUE means success. FALSE = failed.
    #===============================================================================
    def Init(self, f):
        self.freq = f
        mode = IO.getmode()
        if mode == IO.BOARD:  
            if self.ch == 1:
                self.pin = 12
            elif self.ch == 2:
                self.pin = 32
            elif self.ch == 3:
                self.pin = 33
        elif mode == IO.BCM:
            if self.ch == 1:
                self.pin = 18
            elif self.ch == 2:
                self.pin = 12
            elif self.ch == 3:
                self.pin = 13
        
        try:
            IO.setup(self.pin, IO.OUT)
        except:
            print("ERROR: Could not initialize PWM. Is GPIO mode set?")
            IO.cleanup()
            raise SystemExit
            return False    #doesn't really get here but ye(:
        
        self.pwm = IO.PWM(self.pin, self.freq)
        self.pwm.start(0)
        self.duty = 0
        return True

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
    IO.setmode(IO.BOARD)

    pwm1 = PWM(1)
    pwm2 = PWM(3)
    pwm1.Init(100)
    pwm2.Init(1000)
    pwm1.SetDutyCycle(50)
    pwm2.SetDutyCycle(50)

    input("press return to stop.")

    pwm1.Stop()
    pwm2.Stop()

    IO.cleanup()
