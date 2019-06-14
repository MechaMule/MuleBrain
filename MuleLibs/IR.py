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

#===============================================================================
# Class:    IR
# Desc:     Class for IR. Should only have one instance.
# Param:    none atm. Might add pin param init.
#===============================================================================
class IR:
    def __init__(self):
        if getattr(self.__class__, '_has_instance', False):
            raise RuntimeError('Cannot create another instance')
        self.__class__._has_instance = True
        
    #===============================================================================
    # Function: Init(self)
    # Desc:     Initialize IR. Sets pin active input with software pull down
    #           resistor.
    # Params:   none
    # Returns:  none, will stop program if bad.
    #===============================================================================
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

    #===============================================================================
    # Function: Status(self)
    # Desc:     Reads the status of all the pins
    # Params:   none
    # Returns:  4-bit number. 0bNWES
    #===============================================================================
    def Status(self):
        try:
            self.state_N = IO.input(self.pin_N)
            self.state_S = IO.input(self.pin_S)
            self.state_E = IO.input(self.pin_E)
            self.state_W = IO.input(self.pin_W)
        except:
            print("ERROR: Could not read pin states. Has pin or GPIO mode been set?")
            IO.cleanup()
            raise SystemExit
        
        return ((self.state_N<<3 | self.state_W<<2 | self.state_E<<1 | self.state_S) & 0b1111)

    def Clean(self):
        IO.cleanup()


#===============================================================================
# Testing code
#===============================================================================
if __name__ == "__main__":
    IO.setwarnings(False)
    IO.setmode(IO.BCM)

    IR = IR()
    IR.Init()
    print('======= Now starting test to see if both IR sensors can see target')
    try:
        while 1:
            print(IR.Status())
            if(IR.Status() == 0b0011):
                print('FOV between N & W: In front of bot')
                #break
            elif(IR.Status() == 0b0111):
                print('FOV of N only: Left side of bot')
            elif(IR.Status() == 0b1011):
                print('FOV of W only: Right side of bot')
  
    except KeyboardInterrupt:
        print('Exiting program via CTRL + C')
    finally:
        IO.cleanup()

    

    
