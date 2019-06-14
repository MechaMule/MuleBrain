#!/usr/bin/env python

#===============================================================================
# MechaMule!
# Name(s):  April Zitkovich
# Date: May 14, 2019
# File: CornerDetectionEvent.py
# Desc: Program that sends a message over bluetooth when it detects a turn.
#===============================================================================
# IMPORTS
#===============================================================================
import os
import sys
import operator as op
import math
import matplotlib.pyplot as plt
from time import sleep
from bluedot.btcomm import BluetoothClient 
from mpu9250 import mpu9250

#===============================================================================
# DECLARE GLOBAL VARIABLES
#===============================================================================
imu = mpu9250.mpu9250()
prev = [0] * 10
i = 0
gbias = (-3.80503, 1.851525, 0.497668)
xa = []
ya = []
za = []
t = []
time =0

received = False

def data_received(data):
    #print("received: ", data)
    c.send(data)
    global received
    received = True    
    

if __name__ == "__main__":

    PiZero_Client = BluetoothClient("johnpi", data_received)
    PiZero_Client.send("Hello Fren")
    print("============= Starting Gyro activation test ============")
    try:               
        while True:            
            degrees = (0,0,0)
            g = tuple(map(op.sub, imu.gyro, gbias))
            #print("gyroD:", g[0], g[1],g[2])
            #If there are not yet 10 items in an array, then fill array
            if i<10:
                prev[i] = g
                i += 1		
            #Shift array and add new values then take the average	
            if i>=10:
                j=9
                while j > 0 :
                    prev[j] = prev[j-1]
                    j = j-1
                prev[0] = g

                avg = (0,0,0)
                j=0
                while j<10:
                    #integrate = tuple(0.05*x for x in prev[j])
                    avg= tuple(map(op.add, avg, prev[j]))
                    j = j+1
                mov_avg = tuple([x/10 for x in avg])
                mov_avg = tuple(round(x,4) for x in mov_avg)
                z = mov_avg[2]
                xa.append(mov_avg[0])
                ya.append(mov_avg[1])
                za.append(z)
                t.append(time)
                #print("z:", z)
                if(abs(z) > 0.05):
                    degrees = tuple(map(op.add, degrees, mov_avg))
                if z>80 and z<100:
                    print("Right turn, baby turn")
                    PiZero_Client.send("RIGHT")
                if z<-80 and z>-100:
                    print("Left turn, baby turn")
                    PiZero_Client.send("LEFT")
                if abs(z)>150:
                    print("ONE80")
                    PiZero_Client.send("ONE80")

                #print(mov_avg)
            time += 0.05
            sleep(0.05)
            
    except KeyboardInterrupt:
        plt.plot(t, xa, "b-", label = "X")
        plt.plot(t, ya, "r-", label = "Y")
        plt.plot(t, za, "g-", label = "Z")
        plt.title("GYRO Corner Detection Data")
        plt.legend()
        plt.show()
        print("Closing program via CTRL + C")

