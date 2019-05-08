#!/usr/bin/env python

from mpu9250 import mpu9250
from time import sleep
import sys

imu = mpu9250()

print("start")
orig_stdout = sys.stdout
f = open('x_rawn.txt', 'w')
sys.stdout = f
samples = 60000
try:
	while samples > 0:
		a = imu.accel
		print 'Accel: {:.3f} {:.3f} {:.3f}'.format(*a)
		#g = imu.gyro
		#print 'Gyro: {:.3f} {:.3f} {:.3f} dps'.format(*g)
		#m = imu.mag
		#print 'Magnet: {:.3f} {:.3f} {:.3f} mT'.format(*m)
		#m = imu.temp
		#print 'Temperature: {:.3f} C'.format(m)
		sleep(0.01)
		samples = samples - 1
	sys.stdout = orig_stdout
	f.close()
	print("done")
except KeyboardInterrupt:
	print 'bye ...'
	
finally:
	sys.stdout = orig_stdout
	f.close()

