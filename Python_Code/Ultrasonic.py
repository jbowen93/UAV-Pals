"""
Class for handling the Ultrasonic Sensor
"""
import Adafruit_BBIO.ADC as ADC

class Ultrasonic:
    def __init__(self):

        #setup ADC
        ADC.setup()
        self.voltage = 0
        self.distance = 0
        self.count = 0
        self.readings = []
        self.summed = 0
        self.average = 0


    def get_distance(self):

        while self.count < 10:

            #Take a reading
            self.voltage = ADC.read("P9_40")

            #Do conversion math here
            self.distance = self.voltage / 0.1776 # 1/5.63

            self.readings.append(self.distance)

            self.summed = sum(self.readings)

            self.count += 1

        self.average = self.summed/10.0

        return self.average
