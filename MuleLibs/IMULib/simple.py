#!/usr/bin/env python

from mpu9250 import mpu9250
from time import sleep
from bluedot.btcomm import BluetoothClient 

imu = mpu9250.mpu9250()

received = False

def data_received(data):
     print("received: ", data)
     c.send(data)
     global received
     received = True    

try:
	PiZero_Client = BluetoothClient("johnpi", data_received)
	while True:
		#a = imu.accel
		#print('Accel:', a[0], a[1], a[2])
		#PiZero_Client.send('Accel:', a[0], a[1], a[2])
		g = imu.gyro
		print 'Gyro: {:.3f} {:.3f} {:.3f} dps'.format(*g)
		m = imu.mag
		# print 'Magnet: {:.3Af} {:.3f} {:.3f} mT'.format(*m)
		#m = imu.temp
		#print 'Temperature: {:.3f} C'.format(m)
		sleep(1)
except KeyboardInterrupt:
	print('bye ...')
