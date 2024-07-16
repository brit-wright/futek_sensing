# TO DO
# Measure the standard deviation --> will help with figuring out how much noise
# is in the system

import serial
import datetime
import csv
import time
from statistics import stdev

try:
    force_ser = serial.Serial(port='COM27', baudrate=9600)
except:
    print("Force Port Unavailable")
    force_ser = 0

try:
    torque_ser = serial.Serial(port = 'COM26', baudrate = 9600)
except:
    print("Torque Port Unavailable")
    force_ser = 0

counter = 0

def convert_to_newtons(pound_force):
    newton_force = pound_force * 4.44822
    return newton_force

def convert_to_new_met(pound_inch):
    new_met = pound_inch * 0.112985
    return new_met

def force_write_to_csv(f_dict, filename):
    with open('force'+filename+'.csv', 'w', newline = '') as csvfile:
        force_writer = csv.DictWriter(csvfile, fieldnames=['Time', 'Force_Reading'])
        force_writer.writeheader()
        for entry in f_dict:
            force_writer.writerow({'Time': entry, 'Force_Reading': f_dict[entry]})

def torque_write_to_csv(t_dict, filename):
    with open('torque'+filename+'.csv', 'w', newline = '') as csvfile:
        torque_writer = csv.DictWriter(csvfile, fieldnames=['Time', 'Torque_Reading'])
        torque_writer.writeheader()
        for entry in t_dict:
            torque_writer.writerow({'Time': entry, 'Torque_Reading': t_dict[entry]})

def tare_force():
    force_sample = []
    while counter < 1001:
        value = force_ser.readline()
        force_to_string = str(value, 'UTF-8')[:-6]

        if counter > 0:
            force_to_float = -float(force_to_string)
            print(f'{force_to_float} lbf')
            force_sample.append(force_to_float)
        
        counter += 1

    # Tare the sensor
    sum = 0

    # get the average gross number
    for num in force_sample:
        sum += num
    gross = sum/1000
    print(f'GROSS FORCE: {gross}')
    print(f'Standard Deviation: {stdev(force_sample)}')
    time.sleep(5)
    return gross

def tare_torque():
    torque_sample = []
    while counter < 1001:
        value = torque_ser.readline()
        torque_to_string = str(value, 'UTF-8')[:-6]

        if counter > 0:
            torque_to_float = -float(torque_to_string)
            print(f'{torque_to_float} pounds')
            torque_sample.append(torque_to_float)
        
        counter += 1

    # Tare the sensor
    sum = 0

    # get the average gross number
    for num in torque_sample:
        sum += num
    gross = sum/1000
    print(f'GROSS TORQUE: {gross}')
    print(f'Standard Deviation: {stdev(torque_sample)}')
    time.sleep(5)
    return gross

def execute_test():
    new_time = start_time = datetime.datetime.now()
    end_time = start_time + datetime.timedelta(seconds = 3)

    force_dict = {}
    torque_dict = {}

    f_unit = input('Choose unit for force: lbf or N')
    t_unit = input('Choose unit for force: lb-in or Nm')

    while new_time < end_time:
        f_reading = force_ser.readline()
        t_reading = torque_ser.readline()
        torque_to_float = -float(str(t_reading, 'UTF-8')[:-6]) # !!!not sure about the 6
        force_to_float = -float(str(f_reading, 'UTF-8')[:-6])
        
        true_torque = -tare_torque() + torque_to_float
        true_force = -tare_force() + force_to_float

        if f_unit == 'N':
            true_force = convert_to_newtons(true_force)
        print('%.2f' % true_force, f_unit)

        if t_unit == 'Nm':
            true_torque = convert_to_new_met(true_torque)
        print('%.2f' % true_torque, t_unit)

        new_time = datetime.datetime.now()
        index_val = new_time - start_time
        force_dict[index_val] = true_force
        torque_dict[index_val] = true_torque

    force_write_to_csv(force_dict, start_time)
    torque_write_to_csv(torque_dict, start_time)

if __name__ == "__main__":
    print('Sensor script has begun executing')
else:
    print("Error. Program cannot be accessed.")