"""
Test to check that we can log to sub-directories
"""

import logging
import time

start_time = time.time()

#Setup Logging 1
logging.basicConfig(level = logging.INFO)
logger1 = logging.getLogger('1')
handler1 = logging.FileHandler(filename = 'logs/Test1.log', mode = 'w')
handler1.setLevel(logging.INFO)
logger1.addHandler(handler1)
logger1.info('Starting Log 1')

#Setup Logging 2
logging.basicConfig(level=logging.INFO)
logger2 = logging.getLogger('2')
handler2 = logging.FileHandler(filename = 'logs/Test2.log', mode = 'w')
handler2.setLevel(logging.INFO)
logger2.addHandler(handler2)
logger2.info('Starting Log 2')

#Run Forever
for x in range (0, 20):  
 
    #Create a log value
    val1 = x
    val2 = x*2

    #Print and Log value
    current_time = time.time() - start_time
    logger1.info('Time Stamp: %f' %current_time)
    logger1.info('Log value is %f' %val1)
    logger2.info('Log value is %f' %val2)

    #Sleep so that we take readings at 20Hz to prevent terminal from stalling
    time.sleep(0.05)


 
