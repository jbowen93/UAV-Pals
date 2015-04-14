"""
Function for handling the Ultrasonic Sensor
"""
import Adafruit_BBIO.ADC as ADC
import logging
import time

#Function for Ultrasonic
def get_dist():
    count = 1
    readings = [0]
    while count < 10:
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

    return average
