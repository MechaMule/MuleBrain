#===============================================================================
# MechaMule!
# Name(s): Daniel Araujo
#          Johnson Le
# Date: January 27, 2019
# File: MuleMotor_Functions.py
# Desc: library to control Motors. Left Motor Direction pins are 16, and INV = 11
#       Right Motor Direction pins are 18, INV = 13
#===============================================================================
# IMPORTS
#===============================================================================
import RPi.GPIO as IO
from pwm import PWM

class MOTOR(object):
    """H-bridge driving class.
    Parameters (some left out but still needed):
    (1) pin_pwmL : left motor enable pin.
    (3) pin_dirL : left direction control pin.
    (5) pwm_freq : frequency for motor control
    """
    FORWARD = IO.LOW
    REVERSE = IO.HIGH
    def __init__(self, pin_pwmL, pin_pwmR, pin_dirL, pin_dirR, pwm_freq = 1000, IO_mode=IO.BCM):
        """onstructor for MOTOR class"""
        #store parameters
        self.pin_pwmL = pin_pwmL
        self.pin_pwmR = pin_pwmR
        
        self.pin_dirL = pin_dirL
        self.pin_dirR = pin_dirR
        
        self.pwm_freq = pwm_freq
        self.IO_mode = IO_mode
        #set up the GPIO
        IO.setwarnings(False)
        IO.setmode(self.IO_mode)
        #setting up direction pins for h-bridge
        IO.setup(self.pin_dirL, IO.OUT, initial = MOTOR.FORWARD)
        IO.setup(self.pin_dirR, IO.OUT, initial = MOTOR.FORWARD)
        #create pwm object for enabling motors
        self.pwmL = PWM(self.pin_pwmL, self.pwm_freq)
        self.pwmR = PWM(self.pin_pwmR, self.pwm_freq)

    def Motor_L(self, speed):
        """MOTOR Method for driving Left pwm.
        Parameters:
        (1) speed (float) : From -100 to 100. Controls pwm. Negative means reverse."""
        if(speed < 0):
            IO.output(self.pin_dirL, MOTOR.REVERSE)
        else:
            IO.output(self.pin_dirL, MOTOR.FORWARD)

        if(abs(speed)>100):
            print("ERROR: Motor speed to high.")
            self.clean()
        else:
            self.pwmL.SetDutyCycle(abs(speed))

    def Motor_R(self, speed):
        """MOTOR Method for driving right pwm.
        Parameters:
        (1) speed (float) : From -100 to 100. Controls pwm. Negative means reverse."""
        if(speed < 0):
            IO.output(self.pin_dirR, MOTOR.REVERSE)
        else:
            IO.output(self.pin_dirR, MOTOR.FORWARD)

        if(abs(speed)>100):
            print("ERROR: Motor speed to high.")
            self.clean()
        else:
            self.pwmR.SetDutyCycle(abs(speed))

    def Halt(self):
        """MOTOR method to stop the motor"""
        self.pwmL.SetDutyCycle(0)
        self.pwmR.SetDutyCycle(0)

    def clean(self):
        """Clean up the pins that were used."""
        self.Halt()
        print("Motor Pins Cleanup")
        IO.cleanup((self.pin_dirL, self.pin_pwmL, self.pin_dirR, self.pin_pwmR))

if __name__ == "__main__":
    print("Motor Test Start")
    mtr = MOTOR(13, 6, 26, 19)
##    mtr.Motor_R(70)
    mtr.Motor_L(50)
    try:
        input("enter to stop")
    except KeyboardInterrupt:
        pass
    finally:
        mtr.clean()


