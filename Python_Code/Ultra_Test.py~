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
logging.basicConfig(filename = '/logs/ultra1.log')
handler.setLevel(logging.INFO)
logging.addHandler(handler)
logger.info('Starting Log')

#Run Forever
while(1):  
 
    #Take a reading
    distance = ultra.get_dist()

    #Print and Log Distance values
    print "Distance is %f" %distance
    logging.info('Distance is %f' %distance)

    #Sleep so that we take readings at 20Hz to prevent terminal from stalling
    time.sleep(0.05)
 
