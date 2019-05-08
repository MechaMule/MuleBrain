#!/usr/bin/env python

from mpu9250 import mpu9250
from time import sleep
import operator as op
import math
import sys

imu = mpu9250()
prev = [0] * 10
i = 0
print("started Gyro Logging")
orig_stdout = sys.stdout
f = open('gyroStillCal.txt', 'w')
sys.stdout = f

try:
	while i<100:
		g = imu.gyro
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
				integrate = tuple(0.05*x for x in prev[j])
				avg= tuple(map(op.add, avg, prev[j]))
				j = j+1
			mov_avg = tuple([x/10 for x in avg])
			mov_avg = tuple(round(x,4) for x in mov_avg)
			print(mov_avg)
		#print 'Gyro: {:.3f} {:.3f} {:.3f} dps'.format(*prev[0])
		# m = imu.mag
		# print 'Magnet: {:.3Af} {:.3f} {:.3f} mT'.format(*m)
		#m = imu.temp
		#print 'Temperature: {:.3f} C'.format(m)
		sleep(0.05)
except KeyboardInterrupt:
	print 'bye ...'
