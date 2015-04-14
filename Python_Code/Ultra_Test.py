"""
Class for handling the Ultrasonic Sensor
"""
import Adafruit_BBIO.ADC as ADC
import logging
import time

#Run once

ADC.setup()
logging.basicConfig(filename = 'testlog.log', filemode = 'w', level=logging.DEBUG)

#Run Forever
while(1):   
    #Take a reading
    value = ADC.read("P9_40")
    voltage = value * 1.5

    #Do conversion math here
    distance = voltage / 0.00008901 * 1.175 #0.00013841

    print "Distance is %f" %distance
    logging.debug('Distance is %f' %distance)
    #print "Voltage is %f" %voltage
    #print "Value is %f" %value
    time.sleep(0.1)
 
