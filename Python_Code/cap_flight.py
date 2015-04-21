#!/usr/bin/env python
# -*- coding: utf-8 -*-

from vidro import Vidro, ViconStreamer
from position_controller import PositionController
import sys, math, time
import socket, struct, threading
import numpy as np
import Adafruit_BBIO.ADC as ADC
import logging

###############################
#Setup of vidro and controller#
###############################

vidro = Vidro(False, 1)
#TODO Will have to use vidro.connect() or vicon.connect_vicon()
#flight_ready = vidro.connect()
vidro.connect_mavlink()
controller = PositionController(vidro)
start_time = time.time()

#Load gains
controller.update_gains() 

####################
# Controller Values#
####################

take_off_alt = 1000
# Pos Commands
alt_com = 0
# Pos Values
alt_pos = 0

#############
# FSM Values#
#############
sequence = 0
seq0_cnt = 0
seq1_cnt = 0
seq2_cnt = 0
seq3_cnt = 0

# Err Bounds
pos_bound_err = 150

# RC Over-ride reset initialization
reset_val = 1

#Variable for last value
last_error = 0

#Setup ADC
ADC.setup()

#Setup Logging file 1 (For RC Values and Ultrasonic Readings)
logging.basicConfig(level = logging.INFO)
logger1 = logging.getLogger('1')
handler1 = logging.FileHandler(filename = 'logs/Flight8_1.log', mode = 'w')
handler1.setLevel(logging.INFO)
logger1.addHandler(handler1)
logger1.info('Starting Log 1')

#Setup Logging file 2 (For Vicon Values)
logging.basicConfig(level=logging.INFO)
logger2 = logging.getLogger('2')
handler2 = logging.FileHandler(filename = 'logs/Flight*_2.log', mode = 'w')
handler2.setLevel(logging.INFO)
logger2.addHandler(handler2)
logger2.info('Starting Log 2')



print('Heading to main loop')

#####################
# Main Software Loop#
#####################

while(1):
	vidro.update_mavlink() # Grab updated rc channel values. This is the right command for it, but it doesn't always seem to update RC channels

	#Logging
	current_time = time.time() - start_time
	logger1.info('Time is %f' %current_time)
	logger1.info('Commanded RC Throttle is %f' %vidro.current_rc_channels[2])
	logger1.info('Error z is %f' %error_z)
	

	#Auto Loop
	#print('Outer Loop')
	while vidro.current_rc_channels[4] > 1600:

		vidro.update_mavlink() # Grab updated rc channel values. This is the right command for it, but it doesn't always seem to update RC channels

		#Reset of errors after each time control loop finishes
		controller.I_error_alt = 0

		controller.previous_time_alt = (time.time() - controller.timer) * 10
		vidro.previous_error_alt = 0

		controller.update_gains()
		vidro.update_mavlink() # Grab updated rc channel values

		#print('Inner Loop')

		# Seq. 0: Takeoff to 1 m
		if sequence == 0:
			# Assign Commands
			alt_com = take_off_alt
			error_z = controller.rc_alt(alt_com)
			if error_z is None:
			    error_z = last_error
			elif abs(error_z) > 3500:
			    error_z = 800
			else:
			    error_z = error_z

			#Store the Last error
    		        last_error = error_z

			logger1.info('Commanded RC Throttle is %f' %vidro.current_rc_channels[2])
			logger1.info('Error z is %f' %error_z)
			if abs(error_z) < pos_bound_err and abs(error_z) > 0:# Closes Error
				seq0_cnt += 1 # just update the sequence if the loop is closed for 20 software loops
				if seq0_cnt == 20:
					sequence = 1

		#Seq. 1: Hold Altitude
		if sequence == 1:
			error_z = controller.rc_alt(alt_com)
			#print('Seq: '+repr(sequence)+' Err Z: '+repr(round(error_z)))

		        #print('Sequence 1')
			if error_z is None:
			    error_z = last_error
			elif abs(error_z) > 3500:
			    error_z = 800
			else:
			    error_z = error_z
    		        
			#Store the Last Error
		        last_error = error_z

			#print('Error z is %f' %error_z)

			if abs(error_z) < pos_bound_err and abs(error_z) > 0:# Closes Error
				seq1_cnt += 1
				if seq1_cnt == 1000:
					#Go to Land
					sequence = 2

		#Move to landing position
		if sequence == 2:
			error_z = controller.rc_alt(alt_com)
			#print('Seq: '+repr(sequence)+' Err Z: '+repr(round(error_z)))

		        #print('Sequence 2')
			if error_z is None:
			    error_z = last_error
			elif abs(error_z) > 3500:
			    error_z = 800
			else:
			    error_z = error_z
	    		   
			#Store the Last Error
			last_error = error_z

			#print('Error z is %f' %error_z)
			if abs(error_z) < pos_bound_err and abs(error_z) > 0:# Closes Error
				alt_com -= 1
				if(alt_com<170):
					sequence = 3

		# Land
		if sequence == 3:
			controller.vidro.set_rc_throttle(0)# it'll round it to minimum which is like 1100
			controller.vidro.rc_throttle_reset()
			reset_val = 0
			vidro.close()
			break	# this break won't break all the loops, just the auto loop



	if vidro.current_rc_channels[4] < 1600:
		controller.vidro.rc_throttle_reset()




