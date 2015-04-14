"""
Class for handling the Ultrasonic Sensor
"""
import Adafruit_BBIO.ADC as ADC
import logging
import time

class Ultrasonic:
    def __init__(self):

        #setup ADC
        ADC.setup()
        logging.basicConfig(filename = 'testlog.log', filemode = 'w', level=logging.DEBUG)

        self.value = 0
        self.voltage = 0
        self.distance = 0
        self.count = 0
        self.readings = []
        self.summed = 0
        self.average = 0

    def get_distance(self):

        while self.count < 10:

            #Take a reading
            self.value = ADC.read("P9_40")
            self.voltage = self.value * 1.5

            #Do conversion math here
            self.distance = self.voltage / 0.00008901 * 1.175

            if self.distance > (self.readings(count - 1) + 500):
                self.distance = self.readings(count - 1)
            elif self.distance <= (self.readings(count - 1) - 500):
                self.distance = self.readings(count - 1)

            self.readings.append(self.distance)

            self.summed = sum(self.readings)

            self.count += 1

        self.average = self.summed/10.0


        self.count = 0
        del self.readings[:]

        time.sleep(0.025)
        print "Distance is %d" %self.average
        logging.debug('Distance is %f' %self.average)
        return self.average

 
