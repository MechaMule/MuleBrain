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
from enum import Enum

class IR:
    _instances=[]
    def __init__(self):
        if(len(self._instances) >= 1):
            print("ERROR: Only one instance of IR should be made.")
            IO.cleanup()
            raise SystemExit
        self._instances.append(self)
    
    def Init(self):
        mode = IO.getmode()
        if mode == IO.BOARD:
            self.pin_N = 13
            self.pin_S = 15
            self.pin_E = 16
            self.pin_W = 18
        elif mode == IO.BCM:
            self.pin_N = 27
            self.pin_S = 22
            self.pin_E = 23
            self.pin_W = 24
        try:
            IO.setup(self.pin_N, IO.IN, pull_up_down=IO.PUD_DOWN)
            IO.setup(self.pin_S, IO.IN, pull_up_down=IO.PUD_DOWN)
            IO.setup(self.pin_E, IO.IN, pull_up_down=IO.PUD_DOWN)
            IO.setup(self.pin_W, IO.IN, pull_up_down=IO.PUD_DOWN)
        except:
            print("IR ERROR: Could not initialize. Is GPIO mode set?")
            IO.cleanup()
            raise SystemExit
        
    def Status(self):
        self.state_N = IO.input(self.pin_N)
        self.state_S = IO.input(self.pin_S)
        self.state_E = IO.input(self.pin_E)
        self.state_W = IO.input(self.pin_W)
        return (self.state_N<<3 | self.state_W<<2 | self.state_E<<1 | self.state_S)

    def Clean(self):
        IO.cleanup()
        
if __name__ == "__main__":
    IO.setwarnings(False)
    IO.setmode(IO.BCM)

    
    IR = IR()
    IR.Init()
    print(IR.Status())
        
    IO.cleanup()

    

    
