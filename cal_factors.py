"""This script is used to calculate and store the calibration factors
for the futek sensor"""

import serial
import time

# define the ports

force_port = serial.Serial(port = 'COM30', baudrate = 9600)
thrust_port = serial.Serial(port = 'COM31', baudrate = 9600)

time.sleep(2) #chatgpt says this waits for the connection to establish

# read the values from sensor and print them out


# start with force sensing

"""
use KNOWN weights to calibrate the scale my making a relationship between
that mass and the bits
"""


"""General Steps
1. Zero the sensor
2. Calibrate the sensor using a known weight to get the calibration factor
3. Use some test weights to measure. 
If there's jittering use a different averaging method that uses
50% of the current value and 50% of the new value"""
# start by zeroing the sensor

val = 0
count = 0

while count <100:
    count += 1
    val = (count-1/count) * val + (1/count) * force_port.readline()
    print(str(val, 'UTF-8'))


while True:
    force_bits= force_port.readline() - val
    valueInString = str(force_bits, 'UTF-8')
    print(valueInString)

count = 0
force_bits = 0
# or try this averaging FOR CALIBRATION ONLY :)
while True:
    counter += 1
    force_bits = (count-1/count) * force_bits + (1/count) * force_port.readline()
    print(force_bits)


