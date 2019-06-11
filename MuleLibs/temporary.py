from Mule import MULE
import time
import threading
import RPi.GPIO as IO
import math


if __name__ == '__main__':
    print("Mule says hi")
    
    try:
        killswitch = threading.Event()
        mule = MULE(killswitch, [13, 6,26,19], [20,21])
        mule.MTR.Halt()

        time.sleep(0.5)
        while True:
            mL = int(input("L: "))
            mR = int(input("R: "))
            mule.MTR.Motor_L(80)
            mule.MTR.Motor_R(80)
            time.sleep(0.5)
            mule.MTR.Motor_L(mL+20)
            mule.MTR.Motor_R(mR)
            input("enter to stop")
            mule.MTR.Halt()
            time.sleep(0.5)
            
    except KeyboardInterrupt:
        print("pressed ctrl+c")
        mule.MTR.Halt()
        killswitch.set()
        mule.clean()
    finally:
        print("goodbye")
        time.sleep(0.5)

