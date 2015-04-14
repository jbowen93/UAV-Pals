#Testing Functionality

import Ultrasonic
import time
import Adafruit_BBIO.ADC as ADC
import logging

#Init Stuff
logging.basicConfig(filename = 'testlog2.log', filemode = 'w', level = logging.DEBUG)

ADC.setup()

readings = [0]
count = 1

while(1):

    #Distance Conversion Function
    while count < 10:

        #Take a reading
        value = ADC.read("P9_40")
        voltage = value * 1.5

        #Do conversion math here
        distance = voltage / 0.00008901 * 1.175
        #print('readings at %d' %count)
        #print('is %f' %readings[count -1])

        if count > 2:
            if distance > (readings[count - 1] + 500):
                distance = readings[count - 1]
            elif distance <= (readings[count - 1] - 500):
                distance = readings[count - 1]

        readings.append(distance)

        summed = sum(readings)

        count += 1

    average = summed/9.0

    count = 1
    readings = [0]

    time.sleep(0.025)

    logging.debug('Distance is %f' %distance)
    print('Distance is %f' %distance)
    time.sleep(0.05)
