#!/usr/bin/env python

from mpu9250 import mpu9250
from time import sleep
import sys

imu = mpu9250()

bias = (0.029, 0.0039, 0.02)
print("started Accel Logging")
orig_stdout = sys.stdout
f = open('accelStraightcorner.txt', 'w')
sys.stdout = f

try:
	while True:
		a = imu.accel
		c = (a[0] - bias[0], a[1] - bias[1], a[2]-bias[2])
		print '{:.3f}, {:.3f}, {:.3f}'.format(*c)
		#g = imu.gyro
		#print 'Gyro: {:.3f}, {:.3f}, {:.3f}'.format(*g)
		# m = imu.mag
		# print 'Magnet: {:.3f} {:.3f} {:.3f} mT'.format(*m)
		#m = imu.temp
		#print 'Temperature: {:.3f} C'.format(m)
		sleep(0.1)
except KeyboardInterrupt:
	sys.stdout = orig_stdout
	f.close()
	print 'bye ...'
