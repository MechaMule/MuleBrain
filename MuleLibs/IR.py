#===============================================================================
# MechaMule!
# Name(s): Johnson Le
# Date: January 24, 2019
# File: IR.py
# Desc: interface IR beacons
#===============================================================================
# IMPORTS
#===============================================================================
import RPi.GPIO as IO

class IR:
    def __init__(self):
        #nothing yet
        exit()

    def Init(self):
        #nothing yet
        exit()

    def Read(self):
        #return binary 0b0000
        exit()
        

IO.setmode(IO.BOARD)
mode = IO.getmode()
print(mode)
