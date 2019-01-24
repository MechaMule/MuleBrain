#nothing much to do here yet. (:

import sys
sys.path.insert(0, './MuleLibs')
import RPi.GPIO as IO
from pwm import *


IO.setwarnings(False)
IO.setmode(IO.BOARD)

pwm1 = PWM(1)
pwm1.Init(100)
pwm1.SetDutyCycle(50)

input("press return to stop.")

pwm1.Stop()

IO.cleanup()
