"""
Test to verify that distance sensor is working
"""

import Adafruit_BBIO.ADC as ADC
import Ultrasonic as ultra
import logging
import time

ADC.setup()

#Setup Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
handler = logging.FileHandler(filename = 'logs/ultra1.log', mode = 'w')
handler.setLevel(logging.INFO)
logger.addHandler(handler)
logger.info('Starting Log')

#Run Forever
while(1):  
 
    #Take a reading
    distance = ultra.get_dist()
    error = 1000 - distance

    #Print and Log Distance values
    #print "Distance is %f" %distance
    logging.info('Distance is %f' %distance)


    #Print and Log Error values
    #print "Error is %f" %error
    logging.info('Error is %f' %error)

    #Sleep so that we take readings at 20Hz to prevent terminal from stalling
    time.sleep(0.05)
 
