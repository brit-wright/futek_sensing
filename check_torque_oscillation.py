# records the torque oscillations in a csv file

import serial
import datetime
import csv
import time
import statistics
import re

def format_torque(t_list, torque_offset):

    torque_list = []
    index = 0
    errors = []

    pattern = re.compile(r'\d-\d+\.\d+')

    with open('1600_vib_torque_file.txt', 'w', newline = '') as f:
        for entry in t_list:
            # data processing
            # get rid of empty lines and fix the merged numbers
            # ask if this is the correct fix
            if entry == '' or entry == '     ' or entry == '   \n' or entry == '+\n' or pattern.search(entry):  #  or len(entry) > 10
                errors.append(index)
            elif entry.count('.') == 2:
                dindex = entry.find('.', entry.find('.') +1)
                entry = entry[:dindex]
                
                f.write(f'{str(entry)[:8]}\n')
            else:
                f.write(f'{str(entry)[:8]}\n')
            index += 1
    f.close()

    with open('1600_vib_torque_file.txt', 'r') as f:
        
        for line in f:
            # do another if statement where if there are two decimal places I should
            # delete the decimal place and everything after the decimal point
            if line != '+\n' and line != ' \n' and line!= '-    \n' and line!= '   \n' and line != '-\n' and line != '-  \n' and line != '    \n' and line != '  \n':
                floated = (float(line) - torque_offset) * (1.042734793904364 * 0.9973240913059526 * 1.0024564494210493 * 1.0234968035481375*0.9774168633129849) * (0.9798849015665653 * 0.9987893176305618 * 1.0007100078419715) * 1.0108
                torque_list.append(floated)
            
    f.close()
    # print(force_list[23])
    print(len(torque_list))
    return [torque_list, errors]

def format_torque_time(start, times, torque_errors):
    time_list = []
    counter = 0

    for time in times:
        if counter not in torque_errors:
            diff = time - start # of type datetime.timedelta
            format_diff = diff.seconds + diff.microseconds/1000000
            time_list.append(format_diff)
        counter += 1

    with open('1600_vib_torque_time_file.txt', 'w') as t:
         for time in time_list:
              t.write(f'{time}\n')
    t.close()

    print(len(times))
    print(len(time_list))

    return time_list

# writes the torque list to a csv file which will be used to make plots
# in a separate file

def generate_csv_torque(start, times, torques):
    with open('1600_sampling_vibr_torque'+start.strftime("%m_%d_%Y__%H_%M_%S") +'_2000_freq_method2.csv', 'w', newline = '') as csvfile:
        torque_writer = csv.writer(csvfile)
        for num in range(len(torques)):
            torque_writer.writerow([times[num], torques[num]])
        csvfile.close()

# measures the torque of the sensor including the arm. This torque is the torque
# offset and will be subtracted from the torque of the object placed on the arm.

arm_num_samples = 30
counter = 0
num_samples = 30
torque_ser = serial.Serial(port = 'COM26', baudrate = 9600)
arm_val_list = 0
val_list = 0

# while counter < num_samples + 1:
#     torque_ser.reset_input_buffer()
#     print(torque_ser.in_waiting)
#     arm_val = torque_ser.readline()
#     arm_val = (str(arm_val, 'UTF-8').strip().strip('lbs-in'))
#     if counter > 0:
#         arm_val_float = float(arm_val[:8])    
#         arm_val_list += arm_val_float
#         print(f'Torque Reading: {arm_val_float}')
#     counter += 1

torque_ser.reset_input_buffer()
while counter < num_samples + 1:
        
    val = torque_ser.readline()
    val = (str(val, 'UTF-8').strip().strip('in-lbs'))
    if counter > 0:    
        arm_val_list += (float(val))
        print(f'Torque Reading: {val}')
    counter += 1


# tare the sensor
arm_torque_offset = arm_val_list/arm_num_samples
print(arm_torque_offset)
print(type(arm_torque_offset))
counter = 0
#Sensor has been tared




# Take torque using known weight
answer = input("Click Y: ")

new_time = start_time = datetime.datetime.now()
end_time = start_time + datetime.timedelta(seconds = 5)
true_val_list = []
time_list = []
torque_list = []

# while new_time < end_time:
#     torque_ser.reset_input_buffer()
#     val = torque_ser.readline()
#     val = (str(val, 'UTF-8').strip().strip('lbs'))
#     val = val[:-7]
#     if counter > 0:    
#         if val != '' and val != '+' and val.count('.') != 2:
#             val_list += (float(val))
#             true_val = (float(val))
#             print(f'Torque Reading: {true_val}')
#             # if ((end_time - new_time).seconds + (end_time - new_time).microseconds/1000000) < 2:
#             if true_val < 0:
#                 true_val_list.append(true_val)
#     counter += 1
#     new_time = datetime.datetime.now()
# print(len(true_val_list))
# print(true_val_list)
# recorded_torque = (statistics.mean(true_val_list) - arm_torque_offset) * (-0.9980242908389914 * 1.0159514656155124 * 1.0061498743216253 * 0.994759255032 * 0.9992285428459807) *(1.0044194447822277*1.0058888387503069*0.9963883760432045*0.992546236350996*0.9972841255742625) * 1.0051329185997395 * 0.9971789475175031


"""
f = 1000 # frequency
dt = 1 / f #time period  
start = time.time()
t0 = time.time()
T = 10


print("Beginning test")
torque_ser.reset_input_buffer()
torque_ser.reset_output_buffer()
while time.time() - start <= T: # time elapsed since test started
    delta = time.time() - t0
    if delta >= dt:
        t0 = time.time()
        time_list.append(datetime.datetime.now())
        # if torque_ser.in_waiting > 1024:
        #     torque_ser.reset_input_buffer()
        torque_list.append(torque_ser.readline().decode().strip('in-lb\r\n'))
        # time.sleep(0.01)
print('Test has ended')
"""

"""THIS IS THE BEST METHOD SO FAR"""

f = 2000  # frequency in Hz
dt = 1 / f  # time period in seconds
start = time.perf_counter()
T = 10  # duration in seconds

print("Beginning test")
torque_ser.reset_input_buffer()
torque_ser.reset_output_buffer()

next_sample_time = start

while time.perf_counter() - start <= T:
    current_time = time.perf_counter()
    if current_time >= next_sample_time:
        next_sample_time += dt
        time_list.append(datetime.datetime.now())
        torque_list.append(torque_ser.readline().decode().strip('in-lb\r\n'))

print('Test has ended')


"""This method is the worst in terms of getting evenly spaces measurements"""
# print("Beginning test")

# while time.perf_counter() - start <= T:
#     loop_start = time.perf_counter()
#     time_list.append(datetime.datetime.now())
#     torque_list.append(torque_ser.readline().decode().strip('in-lb\r\n'))
#     loop_end = time.perf_counter()
    
#     elapsed = loop_end - loop_start
#     if elapsed < dt:
#         time.sleep(dt - elapsed)

# print('Test has ended')




[torques, t_errors] = format_torque(torque_list, arm_torque_offset)
t_times = format_torque_time(start_time, time_list, t_errors)

generate_csv_torque(start_time, t_times, torques)
    