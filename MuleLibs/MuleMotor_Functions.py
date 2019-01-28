#===============================================================================
# MechaMule!
# Name(s): Johnson Le
# Date: January 24, 2019
# File: pwm.py
# Desc: library to control pwm. PWM pins are 12, 32, 33
#===============================================================================
# IMPORTS
#===============================================================================
#import RPi.GPIO as IO

# Might need to install GPIO library into this comp using this command in term:
# $ sudo pip install RPi.GPIO
#
#   This command might let me compile the program correctly

from pwm.py import *
import RPi.GPIO as GPIO

Right_Dir_GPIO = 4          #Using Pin 4 and Pin 5 on GPIO of RaspPi
Left_Dir_GPIO = 5

#===============================================================================
# Function: Motor_Init
# Desc:    Initializes the PWM, sets frequency and intial direction
# Params:   None
#
# Returns:  N/A
#===============================================================================
def Motor_Init():
    Left_PWM = PWM(1)
    Right_PWM = PWM(2)

    Left_PWM.Init(1000)
    Right_PWM.Init(1000)



        #PWM_SetFrequency(1000)
    GPIO.setup(Right_Dir_GPIO, GPIO.OUT, initial = 0)
    GPIO.setup(Left_Dir_GPIO, GPIO.OUT, initial = 0)

#===============================================================================
# Function: LeftMtrSpeed(Left_Speed)
# Desc:     User can set the duty cycle between -100 and 100 to move left motor
#           in either  forward or reverse direction
# Params:   speed = the duty cycle frequency. Must be -100 >= Speed <= 100
#
# Returns:  N/A
#===============================================================================
def LeftMtrSpeed(Left_Speed):

    if(Left_Speed < 0):
        GPIO.output(Left_Dir_GPIO, 0) # motor is going in reverse
        Left_Speed = Left_Speed * (-1)          # Make the value positive
    else:
        GPIO.output(Left_Dir_GPIO, 1) # otherwise speed is positive
                                          # so motors are moving in forward dir
    if((Left_Speed < -100) or (Left_Speed > 100)):
        print("ERROR: Too much speed in either direction!")
    else:
        Left_PWM.SetDutyCycle(Left_Speed)


#===============================================================================
# Function: RightMtrSpeed(Right_Speed)
# Desc:     User can set the duty cycle between -100 and 100 to move Right motor
#           in either forward or reverse direction
# Params:   speed = the duty cycle frequency. Must be -100 >= Speed <= 100
#
# Returns:  N/A
#===============================================================================
def RightMtrSpeed(Right_Speed):

    if(Right_Speed < 0):
        GPIO.output(Right_Dir_GPIO, 0)  # motor is going in reverse
        Right_Speed = Right_Speed * (-1)    # setting back to positive value
                                                # for valid input
    else:
        GPIO.output(Right_Dir_GPIO, 1)  # motor is going forward

    if((Right_Speed < -100) or (Right_Speed > 100)):
        print("ERROR: Too much speed in either direction!")
    else:
        Right_PWM.SetDutyCycle(Right_Speed)

#===============================================================================
# Function: Forward_Dir(Speed)
# Desc:     Motors will move in forward direction
# Params:   speed = the duty cycle frequency. Speed <= 100
#
# Returns:  N/A
#===============================================================================
def Forward_Dir(Speed):
    LeftMtrSpeed(Speed)
    RightMtrSpeed(Speed)


#===============================================================================
# Function: Reverse_Dir(Speed)
# Desc:     Motors will move in Reverse Direction, input must be positive
#           because it is inverted inside this function
# Params:   speed = the duty cycle frequency. Speed <= 100
#
# Returns:  N/A
    #===============================================================================
def Reverse_dir(Speed):
    LeftMtrSpeed((-1)*Speed)
    RightMtrSpeed((-1)*Speed)


#===============================================================================
# Function: Turn(Left_Speed, Right_Speed)
# Desc:     User can define what kind of turn they want.
# Params:   Left_Speed and Right_Speed = the duty cycle frequency.
#           Must be -100 >= Left_Speed and Right_Speed <= 100
#
# Returns:  N/A
#===============================================================================
def Turn(Left_Speed, Right_Speed):
    LeftMtrSpeed(Left_Speed)
    RightMtrSpeed(Right_Speed)
