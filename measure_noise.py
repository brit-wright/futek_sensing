# measure load in 5 second intervals
# plot the masses

import serial
import datetime
import csv
import time
from statistics import stdev

def tare_force():
    
    force_sample = []
    counter = 0
    response = input('About to Tare Sensor...Remove weight from sensor and press enter: ')
    while counter < 101:
        value = force_ser.readline()
        force_to_string = str(value, 'UTF-8')[:-5]

        if counter > 0:
            if force_to_string ==  '':
                counter -=1
            else:
                force_to_float = -float(force_to_string[:8])
                # print(f'{force_to_float} lbf')
                force_sample.append(force_to_float)
        counter += 1

    # Tare the sensor
    sum = 0

    # get the average gross number
    for num in force_sample:
        sum += num
    gross = sum/100
    print(f'GROSS FORCE: {gross}')
    print(f'Standard Deviation: {stdev(force_sample)}')
    return gross

def format_force(f_list, force_offset):

    force_list = []
    index = 0
    errors = []
    with open('noise_force_file.txt', 'w', newline = '') as f:
        for entry in f_list:
            # data processing
            # get rid of empty lines and fix the merged numbers
            # ask if this is the correct fix
            if entry == '' or entry == '     ' or entry == '   \n' or entry == '+\n':
                errors.append(index)
            elif entry.count('.') == 2:
                dindex = entry.find('.', entry.find('.') +1)
                entry = entry[:dindex]
                
                f.write(f'{str(entry)[:8]}\n')
            else:
                f.write(f'{str(entry)[:8]}\n')
            index += 1
    f.close()

    with open('noise_force_file.txt', 'r') as f:
        
        for line in f:
            # do another if statement where if there are two decimal places I should
            # delete the decimal place and everything after the decimal point
            if line != '+\n' and line != ' \n' and line!= '-    \n' and line!= '   \n' and line != '-\n' and line != '-  \n' and line != '    \n' and line != '  \n':
                floated = -(force_offset + float(line)) * 0.9979366668002273 * 1.0011572505878394 * 0.9990991939859979 *  0.9992328055174383 * 0.9981109383988359 * 0.99875058457423 * 0.9997503917419301 * 1.002537306756004 * 0.9976642714189242
                force_list.append(floated)
            
    f.close()
    # print(force_list[23])
    print(len(force_list))
    return [force_list, errors]

def format_force_time(start, times, force_errors):
    time_list = []
    counter = 0

    for time in times:
        if counter not in force_errors:
            diff = time - start # of type datetime.timedelta
            format_diff = diff.seconds + diff.microseconds/1000000
            time_list.append(format_diff)
        counter += 1

    with open('noise_force_freq_time_file.txt', 'w') as t:
         for time in time_list:
              t.write(f'{time}\n')
    t.close()

    print(len(times))
    print(len(time_list))

    return time_list

def generate_csv_force(start, times, forces):
    with open('noise_force'+start.strftime("%m_%d_%Y__%H_%M_%S") +'.csv', 'w', newline = '') as csvfile:
        force_writer = csv.writer(csvfile)
        # header = ['Time', 'Force_Reading']
        # force_writer.writerow(header)
        for num in range(len(forces)):
            force_writer.writerow([times[num], forces[num]])
        csvfile.close()

force_ser = serial.Serial(port='COM27', baudrate=9600)
print("Force Port Available")

print("Torque Port Available")

force_list = []
time_list = []

new_time = start_time = datetime.datetime.now()

answer = input('Press y to start test: ')
tared_force = tare_force()
while answer == 'y':
    force_list = []
    torque_list = []
    time_list = []

    new_time = start_time = datetime.datetime.now()
    
    response = input('Put first load on the sensor and press enter....')

    f = 2000 # frequency
    dt = 1 / f #time period  
    start = time.time()
    t0 = time.time()
    T = 10

    print("Beginning test")
    force_ser.reset_input_buffer()
    while time.time() - start <= T: # time elapsed since test started
        delta = time.time() - t0
        if delta >= dt:
            t0 = time.time()
            time_list.append(datetime.datetime.now())
            if force_ser.in_waiting > 1024:
                force_ser.reset_input_buffer()
            force_list.append(force_ser.readline().decode().strip('lbs\r\n'))
            # time.sleep(0.01)
    print('Test has ended')

    [forces, f_errors] = format_force(force_list, tared_force)
    f_times = format_force_time(start_time, time_list, f_errors)

    generate_csv_force(start_time, f_times, forces)
    
    answer = input('Place new load on sensor and press y to start new test: ')