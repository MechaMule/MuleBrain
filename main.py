#===============================================================================
# MechaMule!
# Name(s):  Johnson Le
# Date: February 17, 2019
# File: Main.py
# Desc: The main file that initializes everything for the mule.
#===============================================================================
# IMPORTS
#===============================================================================
import sys
sys.path.insert(0, './MuleLibs')

from queue import Queue
import Keyboard
import threading
import time
import Signal
import Echo
from MuleMotor_Functions import MOTOR
##from bluedot.btcomm import BluetoothServer

#===============================================================================
# Methods
#===============================================================================
def qworker(stopper):
    """Thread Method to process the queue"""
    while (stopper.is_set() == False):
        event = q1.get()

        if event == "STOP" or event == "0":
            stopper.set()
        elif event == "DIST_5" or event == "1":
            Update_Bot_Distance(5)
        elif event == "DIST_10" or event == "2":
            Update_Bot_Distance(10)
        elif event == "DIST_15" or event == "3":
            Update_Bot_Distance(15)
        elif event == "p":
            Update_Bot_Distance(0)
        else:
            print("Useless Press: ", event)
        q1.task_done()

def MapRange(x, in_min, in_max, out_min, out_max):
    return (out_min + ( ((out_max-out_min)*(x-in_min))/(in_max-in_min) ))

def Update_Bot_Distance(dist):
    if(dist == 0):
        global pause
        pause ^= True
        print("Pausing =", pause)
        return

    global dist_bot
    dist_bot = dist
    print("Changing Mule distance to ", dist)

def bt_received(data):
    pass
#===============================================================================
# MAIN MAIN
#===============================================================================
if __name__ == '__main__':
    printf("Mule starting up!")
    closer = threading.Event()
    #declare pins
    p_trig = 19
    p_mtrL = 18
    p_mtrR = 12
    p_dirL = 20
    p_dirR = 21
    p_echoL1 = 13
    p_echoL2 = 26
    p_echoR1 = 24
    p_echoR2 = 23

    #creating the trigger signal
    trig = Signal.Generator(closer, p_trig, 10E-6, 60E-3)
    trig.start()

    #creating threaded queue
    q1 = Queue(maxsize=0)
    for i in range(1): #change to increase num of threads for processing queue.
        t = threading.Thread(target=qworker, kwargs=dict(stopper=closer))
        t.daemon = True
        t.start()

    #creating threaded keyboard. has access to the queue
    kb = Keyboard.KB(closer,q1)
    kb.start()

    #create echo object for the ping sensor don't forget to clean
    echoL1 = Echo.ECHO(p_echoL1)
    echoR1 = Echo.ECHO(p_echoR1)
    echoL2 = Echo.ECHO(p_echoL2)
    echoR2 = Echo.ECHO(p_echoR2)

    #create h-bridge motor control class
    mtr = MOTOR(p_mtrL, p_mtrR, p_dirL, p_dirR)

    #create bt server host
    bts = BluetoothServer(bt_recieved)

    #settings
    kbcontrol = False
    pause = False
    speed_default = 20 #will later change to speed of user
    speed_max = 100
    speed_max_offset = 30
    dist_bot = 5
    speed_offset = 30

    #variables



    try:
        while(closer.is_set()==False):
            time.sleep(0.5)
            if pause == True:
                mtr.Motor_L(0)
                mtr.Motor_R(0)
            elif(kbcontrol == False):
                # L = 2*echoL.GetInch()
                # R = 2*echoR.GetInch()
                # l = 0
                # r = 0
                # if L < R:
                #     l = 20
                # if R < L:
                #     r = 20
                # print(L, "||", R)
                # if(L <= 12 or L >= 60):
                #     mtr.Motor_L(0)
                # else:
                #     mtr.Motor_L(l+MapRange(L, 12, 60, 30, 70))
                # if(R <= 12 or R >= 60):
                #     mtr.Motor_R(0)
                # else:
                #     mtr.Motor_R(r+MapRange(L, 12, 60, 30, 70))
                dL1 = 2*echoL1.GetInch()
                dR1 = 2*echoR1.GetInch()
                dL2 = 2*echoL2.GetInch()
                dR2 = 2*echoR2.GetInch()

                dL = max(dL1, dL2)
                dR = max(dR1, dR2)

                if(dL > dR + 5):
                    offL = speed_offset
                    offR = 0
                elif (dR > dL + 5):
                    offR = speed_offset
                    offL = 0
                else:
                    offL = 0
                    offR = 0

                if(dL <= dist_bot):
                    mtr.Motor_L(0)
                elif(dL>dist_bot and dL<=dist_bot+6):
                    mtr.Motor_L(offL + speed_default)
                elif(dL>dist+6+60):
                    mtr.Motor_L(offL+100-speed_default)
                else:
                    mtr.Motor_L(offL + MapRange(dL, dist_bot+6, dist_bot+120, speed_default, 100-speed_default))


                if(dR <= dist_bot):
                    mtr.Motor_R(0)
                elif(dR>dist_bot and dR<=dist_bot+6):
                    mtr.Motor_R(offR + speed_default)
                elif(dR>dist+6+60):
                    mtr.Motor_R(offR+100-speed_default)
                else:
                    mtr.Motor_R(offR + MapRange(dR, dist_bot+6, dist_bot+120, speed_default, 100-speed_default))


    except KeyboardInterrupt:
        pass
    finally:
        print("Mule go bye bye now")
        echoL.clean()
        echoR.clean()
        mtr.clean()
        closer.set()
        time.sleep(.5)
