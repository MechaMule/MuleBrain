from Mule import MULE
import time
import threading
import RPi.GPIO as IO
import math
import matplotlib.pyplot as plt
from simple_pid import PID


if __name__ == '__main__':
    print("Mule says hi")

    
    try:
        killswitch = threading.Event()
        mule = MULE(killswitch, [6,13,19,26], [20,21])
        mule.MTR.Halt()

        Kp, Ki, Kd = 45, 0, 0
        pidL = PID(Kp, Ki, Kd, setpoint=0)
        pidR = PID(Kp, Ki, Kd, setpoint=0)
        
        pidL.output_limits = (-90, 90)
        pidR.output_limits = (-90, 90)
        
        pidL.auto_mode = True
        pidR.auto_mode = True

        x_axis, y_mL, y_mR, y_dL, y_dR = [], [], [], [], []
        iteration = 0
        
        while True:
            time.sleep(1E-1)
            dL = mule.echo[0].GetFeet()
            dR = mule.echo[1].GetFeet()
            
            adjL = pidL(dL-dR)
            adjR = pidR(dR-dL)

            mb = 0

            mL = mb + adjL
            mR = mb + adjR
            mule.MTR.Motor_L(mL)
            mule.MTR.Motor_R(mR)

            x_axis += [round(iteration * 1E-1,1)]
            y_dL.append(round(dL,3))
            y_dR.append(round(dR,3))
            y_mL.append(round(mL,3))
            y_mR.append(round(mR,3))
            print("Distance: ", round(dL,3), "   ||   ", round(dR,3))
            
            
            

    except KeyboardInterrupt:
        print("pressed ctrl+c")
        plt.subplot(2,1,1)
        plt.plot(x_axis, y_dL, label='dL')
        plt.plot(x_axis, y_dR, label='dR')
        plt.xlabel('time')
        plt.ylabel('distance')
        plt.legend()

        plt.subplot(2,1,2)
        plt.plot(x_axis, y_mL, label='mL')
        plt.plot(x_axis, y_mR, label='mR')
        plt.xlabel('time')
        plt.ylabel('Motor Speed')
        plt.legend()
        plt.show()
    finally:
        print("goodbye")
        IO.cleanup((4,17))
        mule.MTR.Halt()
        killswitch.set()
        mule.clean()
        time.sleep(0.5)

