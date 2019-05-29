#===============================================================================
# MechaMule!
# Name(s):  April Zitkovich
# Date: May 14, 2019
# File: CornerDetectionEvent.py
# Desc: Program that sends a message over bluetooth when it detects a turn.
#===============================================================================
# IMPORTS
#===============================================================================

from mpu9250 import mpu9250
from time import sleep
import operator as op
import math
import sys


class cornerDetect():
	def __init__(self):
		imu = mpu9250()
		prev = [0] * 10
		i = 0
		gbias = (-3.80503, 1.851525, 0.497668)
		#RETURN VALUES
		RIGHT, LEFT, ONE80, NOTURN = 1, 2, 3, 0
	
	def getData(self):
		while(1):
			degrees = (0,0,0)
			g = tuple(map(op.sub, imu.gyro, gbias))
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
					avg= tuple(map(op.add, avg, integrate))
					j = j+1
				mov_avg = tuple([x/10 for x in avg])
				mov_avg = tuple(round(x,4) for x in mov_avg)
				z = mov_avg[2]
				
				if(abs(z) > 0.05):
					degrees = tuple(map(op.add, degrees, mov_avg))
				if mov_avg[2]>80 and mov_avg[2]<100:
					print("Right turn, baby turn")
					return RIGHT
				if mov_avg[2]<-80 and mov_avg[2]>-100:
					print("Left turn, baby turn")
					return LEFT
				if abs(mov_avg[2])>150:
					return ONE80
				else: return NOTURN
				#print(mov_avg)

				sleep(0.05)

if __name__ == '__main__':
	#print("started Gyro Logging")
	#orig_stdout = sys.stdout
	#f = open('gyroStillCal.txt', 'w')
	#sys.stdout = f
	try:
		while True:
			detection = cornerDetect()
			detection.getData()
	except KeyboardInterrupt:
		#sys.stdout = orig_stdout
		#f.close()
		print 'bye ...'
