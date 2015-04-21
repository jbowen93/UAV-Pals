"""
Test to check that we can log to sub-directories
"""

import logging
import time

#Setup Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
handler = logging.FileHandler(filename = 'logs/ultra1.log', mode = 'w')
handler.setLevel(logging.INFO)
logger.addHandler(handler)
logger.info('Starting Log')

#Run Forever
for x in range (0, 20):  
 
    #Create a log value
    val = x

    #Print and Log value
    print "Log value is %f" %val
    logger.info('Log value is %f' %val)

    #Sleep so that we take readings at 20Hz to prevent terminal from stalling
    time.sleep(0.05)
 