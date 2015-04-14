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
#flight_ready = vidro.connect()
vidro.connect_mavlink()
controller = PositionController(vidro)
start_time = time.time()
# Load gains
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

off_cnt = 0

# Err Bounds
pos_bound_err = 100

# RC Over-ride reset initialization
reset_val = 1

ADC.setup()

logging.basicConfig(filename = 'flight1.log', level = logging.INFO)

print('Heading to main loop')

#####################
# Main Software Loop#
#####################

while(1):
	vidro.update_mavlink() # Grab updated rc channel values. This is the right command for it, but it doesn't always seem to update RC channels

	#Auto Loop
	while vidro.current_rc_channels[4] > 1600:
		if(reset_val):
			print 'Reset Over-rides'
			controller.vidro.rc_throttle_reset()
			reset_val = 0

		vidro.update_mavlink() # Grab updated rc channel values. This is the right command for it, but it doesn't always seem to update RC channels

		#Reset of errors after each time control loop finishes
		controller.I_error_alt = 0

		controller.previous_time_alt = (time.time() - controller.timer) * 10
		vidro.previous_error_alt = 0

		controller.update_gains()
		vidro.update_mavlink() # Grab updated rc channel values

		print('Auto Loop')

		# Seq. 0: Takeoff to 1 m
		if sequence == 0:
			# Assign Commands
			alt_com = take_off_alt
			error_z = controller.rc_alt(alt_com)
			if error_z is None:
			    error_z = 0
			elif abs(error_z) > 3500:
			    error_z = 800
			else:
			    error_z = error_z
		        #print('Sequence 0')
			#print('Error z is %f' %error_z)
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
			    error_z = 0
			elif abs(error_z) > 3500:
			    error_z = 800
			else:
			    error_z = error_z

			#print('Error z is %f' %error_z)

			if abs(error_z) < pos_bound_err and abs(error_z) > 0:# Closes Error
				seq1_cnt += 1
				if seq1_cnt == 100:
					#Go to Land
					sequence = 2

		#Move to landing position
		if sequence == 2:
			error_z = controller.rc_alt(alt_com)
			#print('Seq: '+repr(sequence)+' Err Z: '+repr(round(error_z)))

		        #print('Sequence 2')
			if error_z is None:
			    error_z = 0
			elif abs(error_z) > 3500:
			    error_z = 800
			else:
			    error_z = error_z

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
		off_count += 1
		if off_count == 100
			controller.vidro.set_rc_throttle = 0
			off_count = 0




