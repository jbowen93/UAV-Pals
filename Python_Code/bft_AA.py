#!/usr/bin/env python
# -*- coding: utf-8 -*-

from vidro import Vidro, ViconStreamer
from position_controller import PositionController
import sys, math, time
import socket, struct, threading
import numpy as np

###############################
#Setup of vidro and controller#
###############################

vidro = Vidro(False, 1)
flight_ready = vidro.connect()
controller = PositionController(vidro)
start_time = time.time()
# Load gains
controller.update_gains() 

####################
# Controller Values#
####################

take_off_alt = 1000
# Pos Commands
x_com = 0
y_com = 0
alt_com = 0
yaw_com = 0
# Pos Values
x_pos = 0
y_pos = 0
alt_pos = 0
yaw_pos = 0
guid_adv = 500 # Guidance advancing value, ie move n mm towards estimated bearing and re-check

#############
# FSM Values#
#############
sequence = 0
seq0_cnt = 0
seq1_cnt = 0
seq2_cnt = 0
seq3_cnt = 0

# Err Bounds
pos_bound_err = 100
yaw_bound_err = 0.2
# RC Over-ride reset initialization
reset_val = 1

print('Heading to main loop')

#####################
# Main Software Loop#
#####################

while(1):
	vidro.update_mavlink() # Grab updated rc channel values. This is the right command for it, but it doesn't always seem to update RC channels
	# Auto Loop
	while vidro.current_rc_channels[4] > 1600 and flight_ready == True:
		if(reset_val):
			print 'Reset Over-rides'
			controller.vidro.rc_throttle_reset()
			controller.vidro.rc_yaw_reset()
			controller.vidro.rc_pitch_reset()
			controller.vidro.rc_roll_reset()
			reset_val = 0

		vidro.update_mavlink() # Grab updated rc channel values. This is the right command for it, but it doesn't always seem to update RC channels
		#Reset of errors after each time control loop finishes
		controller.I_error_alt = 0
		controller.I_error_pitch = 0
		controller.I_error_roll = 0
		controller.I_error_yaw = 0
		controller.previous_time_alt = (time.time() - controller.timer) * 10
		controller.previous_time_yaw = (time.time() - controller.timer) * 10
		controller.previous_time_xy = (time.time() - controller.timer) * 10
		vidro.previous_error_alt = 0
		vidro.previous_error_yaw = 0
		vidro.previous_error_roll = 0
		vidro.previous_error_pitch = 0

        controller.update_gains()
        vidro.update_mavlink() # Grab updated rc channel values
        print('Auto Loop')

        # Seq. 0: Takeoff to 1 m and origin
        if sequence == 0:
            # Assign Commands
            alt_com = take_off_alt
            error_z = controller.rc_alt(alt_com)
            error_yaw = controller.rc_yaw(yaw_com)
            #error_x_y = controller.rc_xy(x_com, y_com)
            err_x = 0#error_x_y[0]
            err_y = 0#error_x_y[1]
            print('Seq: '+repr(sequence)+' Err Z: '+repr(round(error_z))+' Err Yaw: '+repr(round(error_yaw))+' Err X: '+repr(round(err_x))+' Err y: '+repr(round(err_y)))
            if ((abs(error_z) < pos_bound_err) and (abs(error_yaw) < yaw_bound_err) and (abs(err_y) < pos_bound_err) and (abs(err_x) < pos_bound_err)):# Closes Error
                seq0_cnt += 1 # just update the sequence if the loop is closed for 3 software loops
                if seq0_cnt == 10:
                    sequence = 1

        #Seq. 1: Guidance
        if sequence == 1:
            error_z = controller.rc_alt(alt_com)
            error_yaw = controller.rc_yaw(yaw_com)
            err_x = 0
            err_y = 0
            print('Seq: '+repr(sequence)+' Err Z: '+repr(round(error_z))+' Err Yaw: '+repr(round(error_yaw))+' Err X: '+repr(round(err_x))+' Err y: '+repr(round(err_y)))
            if ((abs(error_z) < pos_bound_err) and (abs(error_yaw) < yaw_bound_err) and (abs(err_y) < pos_bound_err) and (abs(err_x) < pos_bound_err)):# Closes Error
                # Hold her steady while we img proc
                vidro.set_rc_throttle(vidro.base_rc_throttle)
                vidro.set_rc_roll(vidro.base_rc_roll)
                vidro.set_rc_pitch(vidro.base_rc_pitch)
                vidro.set_rc_yaw(vidro.base_rc_yaw)
                #Go to Land
                sequence = 2

        #Move to landing position
        if sequence == 2:
            error_z = controller.rc_alt(alt_com)
            print('Seq: '+repr(sequence)+' Err Z: '+repr(round(error_z))+' Err Yaw: '+repr(round(error_yaw))+' Err X: '+repr(round(err_x))+' Err y: '+repr(round(err_y)))
            if ((abs(error_z) < pos_bound_err) and (abs(error_yaw) < yaw_bound_err) and (abs(err_y) < pos_bound_err) and (abs(err_x) < pos_bound_err)):# Closes Error
                alt_com-=1
                if(alt_com<170):
                    sequence = 3

        # Land
        if sequence == 3:
            controller.vidro.set_rc_throttle(0)# it'll round it to minimum which is like 1100
            controller.vidro.rc_throttle_reset()
            controller.vidro.rc_yaw_reset()
            controller.vidro.rc_pitch_reset()
            controller.vidro.rc_roll_reset()
            reset_val = 0
            vidro.close()
            break	# this break won't break all the loops, just the auto loop

        if vidro.current_rc_channels[4] < 1600:
            reset_val = 1



