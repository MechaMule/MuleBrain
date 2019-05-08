#!/usr/bin/env python

import numpy as np
import csv
from mpu9250 import mpu9250
from time import sleep


#imu = mpu9250()
xn_mean = -0.970696467
yn_mean = -0.999342827
zn_mean = -0.993932267

xp_mean = 1.028695111
yp_mean = 1.00728988
zp_mean = 1.034684613


try:
	xrawn= []
	yrawn= []
	zrawn= []
	xrawp= []
	yrawp= []
	zrawp= []
	
	#~ #open csv files that have +g and -g recorded on the specified axis
	#~ #and isolate that data then put it together
	#~ with open("xrawn.csv") as csvfile:
		#~ reader = csv.reader(csvfile, delimiter=',', quotechar='|')
		#~ for column in reader:
			#~ xrawn.append(column)
	#~ xrawn = np.delete(xrawn, 2, 1)
	#~ xrawn = np.delete(xrawn, 1, 1)
	#~ xrawnf = []
	#~ for sublist in xrawn:
		#~ for item in sublist:
			#~ xrawnf.append(float(item))
	
	
	#~ with open("yawn.csv") as csvfile:
		#~ reader = csv.reader(csvfile, delimiter=',', quotechar='|')
		#~ for column in reader:
			#~ yrawn.append(column)
	#~ yrawn = np.delete(yrawn, 2, 1)
	#~ yrawn = np.delete(yrawn, 0, 1)
	#~ yrawnf = []
	#~ for sublist in yrawn:
		#~ for item in sublist:
			#~ yrawnf.append(float(item))	
	#~ yn_mean= sum(yrawnf) / len(yrawnf)	
	
	#~ with open("zrawn.csv") as csvfile:
		#~ reader = csv.reader(csvfile, delimiter=',', quotechar='|')
		#~ for column in reader:
			#~ zrawn.append(column)
	#~ zrawn = np.delete(zrawn, 0, 1)
	#~ zrawn = np.delete(zrawn, 0, 1)	
	#~ zrawnf = []
	#~ for sublist in zrawn:
		#~ for item in sublist:
			#~ zrawnf.append(float(item))
	#~ zn_mean= sum(zrawnf) / len(zrawnf)
	
	#~ print(xn_mean,yn_mean,zn_mean)

	#open csv files that have +g and -g recorded on the specified axis
	#and isolate that data then put it together	
	with open("xrawp.csv") as csvfile:
		reader = csv.reader(csvfile, delimiter=',', quotechar='|')
		for column in reader:
			xrawp.append(column)
	xrawp = np.delete(xrawp, 2, 1)
	xrawp = np.delete(xrawp, 1, 1)
	xrawpf = []
	for sublist in xrawp:
		for item in sublist:
			xrawpf.append(float(item))
	xp_mean= sum(xrawpf) / len(xrawpf)
	
	with open("yrawp.csv") as csvfile:
		reader = csv.reader(csvfile, delimiter=',', quotechar='|')
		for column in reader:
			yrawp.append(column)
	yrawp = np.delete(yrawp, 2, 1)
	yrawp = np.delete(yrawp, 0, 1)
	yrawpf = []
	for sublist in yrawp:
		for item in sublist:
			yrawpf.append(float(item))	
	yp_mean= sum(yrawpf) / len(yrawpf)	
	
	with open("zrawp.csv") as csvfile:
		reader = csv.reader(csvfile, delimiter=',', quotechar='|')
		for column in reader:
			zrawp.append(column)
	zp = [row[2] for row in zrawp]
	print(zp)
	zrawpf = []
	for sublist in zp:
		for item in sublist:
			zrawpf.append(float(item))
	zp_mean= sum(zrawpf) / len(zrawpf)
	
	print(xp_mean,yp_mean,zp_mean)
	
	while True:
		#a = imu.accel
		#print 'Accel: {:.3f} {:.3f} {:.3f} mg'.format(*a)
		# g = imu.gyro
		# print 'Gyro: {:.3f} {:.3f} {:.3f} dps'.format(*g)
		# m = imu.mag
		# print 'Magnet: {:.3Af} {:.3f} {:.3f} mT'.format(*m)
		#m = imu.temp
		#print 'Temperature: {:.3f} C'.format(m)
		sleep(0.5)
except KeyboardInterrupt:
	print 'bye ...'
