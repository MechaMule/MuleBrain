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
        else:
            self.pwmR.SetDutyCycle(abs(speed))

    def Halt(self):
        """MOTOR method to stop the motor"""
        self.pwmL.SetDutyCycle(0)
        self.pwmR.SetDutyCycle(0)

    def clean(self):
        """Clean up the pins that were used."""
        self.Halt()
        IO.cleanup((self.pin_dirL, self.pin_pwmL, self.pin_dirR, self.pin_pwmR))

if __name__ == "__main__":
    print("Motor Test Start")
    mtr = MOTOR(13, 6, 16, 20)
    mtr.Motor_R(100)
    mtr.Motor_L(100)
    try:
        input("enter to stop")
    except KeyboardInterrupt:
        pass
    finally:
        mtr.clean()


#import RPi.GPIO as IO

# Might need to install GPIO library into this comp using this command in term:
# $ sudo pip install RPi.GPIO
#
#   This command might let me compile the program correctly

# from pwm import *
# import RPi.GPIO as GPIO
#
# Left_Dir_GPIO = 17          #
# Left_Dir_INV = 27
#
# Right_Dir_GPIO = 23          #Using Pin 4 and Pin 5 on GPIO of RaspPi
# Right_Dir_INV = 24

# #===============================================================================
# # Function: Motor_Init
# # Desc:    Initializes the PWM, sets frequency and intial direction
# # Params:   None
# # Returns:  N/A
# #===============================================================================
# def Motor_Init():
#     global Left_PWM
#     global Right_PWM
#     Left_PWM = PWM(18, 1000, 0)
#     Right_PWM = PWM(13, 1000, 0)
#
# #    Left_PWM.Init(1000)
# #    Right_PWM.Init(1000)
#
#         #PWM_SetFrequency(1000)
#     GPIO.setup(Right_Dir_GPIO, GPIO.OUT, initial = 0)
#     GPIO.setup(Right_Dir_INV, GPIO.OUT, initial = 1)
#
#     GPIO.setup(Left_Dir_GPIO, GPIO.OUT, initial = 0)
#     GPIO.setup(Left_Dir_INV, GPIO.OUT, initial = 1)
#
# #===============================================================================
# # Function: LeftMtrSpeed(Left_Speed)
# # Desc:     User can set the duty cycle between -100 and 100 to move left motor
# #           in either  forward or reverse direction
# # Params:   speed = the duty cycle frequency. Must be -100 >= Speed <= 100
# #
# # Returns:  N/A
# #===============================================================================
# def LeftMtrSpeed(Left_Speed):
#
#     if(Left_Speed < 0):
#         GPIO.output(Left_Dir_GPIO, GPIO.LOW) # motor is going in reverse
#         GPIO.output(Left_Dir_INV, GPIO.HIGH)
#
#         out = Left_Speed * (-1)
#         #Left_Speed = Left_Speed * (-1)          # Make the value positive
#     else:
#         GPIO.output(Left_Dir_GPIO, GPIO.HIGH) # otherwise motor goes forward
#         GPIO.output(Left_Dir_INV, GPIO.LOW)
#         out = Left_Speed
#                                           # so motors are moving in forward dir
#     if((Left_Speed < -100) or (Left_Speed > 100)):
#         print("ERROR: Too much speed in either direction!")
#     else:
#         Left_PWM.SetDutyCycle(out)
#
#
# #===============================================================================
# # Function: RightMtrSpeed(Right_Speed)
# # Desc:     User can set the duty cycle between -100 and 100 to move Right motor
# #           in either forward or reverse direction
# # Params:   speed = the duty cycle frequency. Must be -100 >= Speed <= 100
# #
# # Returns:  N/A
# #===============================================================================
# def RightMtrSpeed(Right_Speed):
#
#     if(Right_Speed < 0):
#         GPIO.output(Right_Dir_GPIO, GPIO.LOW)  # motor is going in reverse
#         GPIO.output(Right_Dir_INV, GPIO.HIGH)
#
#         out = Right_Speed * (-1)
#         #Right_Speed = Right_Speed * (-1)    # setting back to positive value
#                                                 # for valid input
#     else:
#         GPIO.output(Right_Dir_GPIO, GPIO.HIGH)  # motor is going forward
#         GPIO.output(Right_Dir_INV, GPIO.LOW)
#
#         out = Right_Speed
#
#     if((Right_Speed < -100) or (Right_Speed > 100)):
#         print("ERROR: Too much speed in either direction!")
#     else:
#         Right_PWM.SetDutyCycle(out)
#
# #===============================================================================
# # Function: Forward_Dir(Speed)
# # Desc:     Motors will move in forward direction
# # Params:   speed = the duty cycle frequency. Speed <= 100
# #
# # Returns:  N/A
# #===============================================================================
# def Forward_Dir(Speed):
#     LeftMtrSpeed(Speed)
#     RightMtrSpeed(Speed)
#
#
# #===============================================================================
# # Function: Reverse_Dir(Speed)
#
# # Desc:     Motors will move in Reverse Direction, input must be positive
# #           because it is inverted inside this function
# # Params:   speed = the duty cycle frequency. Speed <= 100
# #
# # Returns:  N/A
# #===============================================================================
# def Reverse_dir(Speed):
#     LeftMtrSpeed((-1)*Speed)
#     RightMtrSpeed((-1)*Speed)
#
#
# #===============================================================================
# # Function: Turn(Left_Speed, Right_Speed)
# # Desc:     User can define what kind of turn they want.
# # Params:   Left_Speed and Right_Speed = the duty cycle frequency.
# #           Must be -100 >= Left_Speed and Right_Speed <= 100
# #
# # Returns:  N/A
# #===============================================================================
# def Turn(Left_Speed, Right_Speed):
#     LeftMtrSpeed(Left_Speed)
#     RightMtrSpeed(Right_Speed)
#
#
#
# TEST = True
#
# if(TEST == True):
#     print("Running Motor functions test")
#     GPIO.setwarnings(False)
#     GPIO.setmode(IO.BCM)
#
#     Motor_Init()
#     sp = 50
#     counter = 0
#     try:
#         while 1:
#             if counter < 250000:
#                 LeftMtrSpeed(sp) #should be low
#                 RightMtrSpeed(sp)
#
#             #input("press return to continue")
#             elif counter > 250000 and counter < 400000:
#                 LeftMtrSpeed(0)
#                 RightMtrSpeed(0)
#
#             #input("press return to continue again")
#             elif counter > 400000:
#                 LeftMtrSpeed(-sp)  #should be high
#                 RightMtrSpeed(-sp)
#
#             #input("press return to stop")
#             counter += 1
#
#     except KeyboardInterrupt:
#         GPIO.cleanup()
#         print("Ending Program")
#
#     else:
#         GPIO.cleanup()
#         print("Ending program")
