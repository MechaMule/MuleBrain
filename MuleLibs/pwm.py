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
# Param:    ch = channel. There are 3 pwm channels. ch1 = pin12, ch2 = pin32, ch3 = pin33
#===============================================================================
class PWM:
    def __init__(self, ch):
        self.ch = ch
        if ch > 3:
            print("ERROR: Only 3 PWM channels.")
            raise SystemExit
        if ch == 1:
            self.pin = 12
        elif ch == 2:
            self.pin = 32
        elif ch == 3:
            self.pin = 33

    #===============================================================================
    # Function: PWM_init(pin_PWM, f)
    # Desc:     Initialize PWM. Sets pin active. Starts at 0% duty cycle.
    # Params:   pin_PWM is the pin that will drive pwm signal
    #           f = frequency that pwm will be set too.
    # Returns:  TRUE means success. FALSE = failed.
    #===============================================================================
    def Init(self, f):
        self.freq = f
        try:
            IO.setup(self.pin, IO.OUT)
        except:
            print("ERROR: Could not initialize PWM. Is GPIO mode set?")
            IO.cleanup()
            raise SystemExit
            return False
        
        self.pwm = IO.PWM(self.pin, self.freq)
        self.pwm.start(0)
        self.duty = 0
        return True

    #===============================================================================
    # Function: PWM_SetFrequency(f)
    # Desc:     Sets PWM Frequency
    # Params:   f = frequency for pwm
    # Returns:  TRUE means success. False = failed.
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
    # Function: PWM_SetDutyCycle(d)
    # Desc:     Sets Duty Cycle
    # Params:   d = duty cycle percentage
    # Returns:  
    #===============================================================================
    def SetDutyCycle(self, d):
        self.duty = d
        self.pwm.start(self.duty)

    #===============================================================================
    # Function: 
    # Desc:     
    # Params:   
    # Returns:  
    #===============================================================================
    def Stop(self):
        self.pwm.stop()

    #===============================================================================
    # Function: 
    # Desc:     
    # Params:   
    # Returns:  
    #===============================================================================
    def Start(self):
        self.pwm.start(freq)


#Testing code.
TEST = False
if TEST == True:
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
