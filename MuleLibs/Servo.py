#===============================================================================
# MechaMule!
# Name(s): Johnson Le, Danny Araujo
# Date: Februrary 9, 2019
# File: Servo.py
# Desc: driving rc servo
#===============================================================================
from pwm import *
import RPi.GPIO as IO
import time

#===============================================================================
# Class:    Servo
# Desc:     Class for Servo
# Param:    
#===============================================================================

class ServoDriver(object):
    def __init__(self, pin, freq=1000, duty=0):
        self.pwm = PWM(pin, freq, duty)
#======================== Added this - Danny ==================================
    # Going to add more functions to the servo ========= as of 2/12/19

#===============================================================================
# Function:     Degree(angle)
# Desc:         Will output the degree/angle on the Servo, value is estimated
#               to be close to the desired angle
# Param:        angle, integer value, cannot be more than 180-degrees, or less
#               than 0-degrees.
#===============================================================================    
    def Degree(self, angle):
        if angle >= 181:
            print("ERROR: This servo cannot handle an angle greater than 180-degrees")
        elif angle <= -1:
            print("ERROR: This servo cannot handle an angle lower than 0-degrees")
        else:

            if angle == 0:
                self.pwm.SetDutyCycle(2)
                #self.pwm.Stop()

            elif angle == 45:
                self.pwm.SetDutyCycle(5)
                #self.pwm.Stop()

            elif angle == 90:
                self.pwm.SetDutyCycle(7)
                #self.pwm.Stop()

            elif angle == 135:
                self.pwm.SetDutyCycle(9)
                #self.pwm.Stop()

            elif angle == 180:
                self.pwm.SetDutyCycle(12)
                #self.pwm.Stop()

            else:
                print("This angle has not been handled yet, please try: 0, 45, 90, 135, or 180")
                
#=============================================================================
    
if __name__ == "__main__":
    print("start test")
    IO.setmode(IO.BCM)
    batman = ServoDriver(18,50,0)
    tog = 0
    x = 2
 
    try:
# ============== Added this - Danny ===========================================        
        print("=========== Test 1: Servo degree manipulation ===========")
        batman.Degree(0)
        print("0 degrees")
        time.sleep(2)

        batman.Degree(45)
        print("45 degrees")
        time.sleep(2)

        batman.Degree(90)
        print("90 degrees")
        time.sleep(2)

        batman.Degree(135)
        print("135 degrees")
        time.sleep(2)

        batman.Degree(180)
        print("180 degrees")
        #time.sleep(2)
    
        print("=========== Test 1 Complete, Test 2 will begin in 5 seconds =======")
        time.sleep(5)           # Will sleep before starting Test2
        print("=========== Test 2: Servo sweep ============")
#==============================================================================
        while True:
            if tog == 0:
                x+=2        # Changed the increment rate from 0.1 to 2
            else:
                x-=2        # Changed the bounds so that they don't below
            if x >= 12:      # threshold that the servo cannot work with
                tog = 1
                #time.sleep(0.5) # This sleeps between alternating directions
            elif x <= 2:
                tog = 0
                #time.sleep(0.5)
            time.sleep(.2)  # This sleeps between each movement
            batman.pwm.SetDutyCycle(x)
            print("duty: ", x)
    except KeyboardInterrupt:
        IO.cleanup()
        print("ending program")
    else:
        IO.cleanup()
        print("ending program")

