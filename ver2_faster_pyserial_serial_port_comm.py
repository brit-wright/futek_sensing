# TO DO
# Problem: FOR SOME REASON WHEN I TRY TO READ THE TORQUE VALUES
# it only prints the zeroed values and doesn't actually read besides new masses
# also sometimes when I call the readline() method, it will read an empty string
# or it'll read two values at once:
# '' or '    ' or '0.2323 0.2434'
import serial
import datetime
import csv
import time
from statistics import stdev

def convert_to_newtons(pound_force):
    newton_force = pound_force * 4.44822
    return newton_force

def convert_to_new_met(pound_inch):
    new_met = pound_inch * 0.112985
    return new_met

def format_force(f_list):

    force_list = []

    with open('force_file.txt', 'w', newline = '') as f:
        for entry in f_list:
            # data processing
            # get rid of empty lines and fix the merged numbers
            # ask if this is the correct fix
            if entry != '' and entry != '     ' and entry != '   \n':
                if entry.count('.') == 2:
                            dindex = entry.find('.', entry.find('.') +1)
                            entry = entry[:dindex]
                
                f.write(f'{str(entry)}\n')
    
    f.close()
    
    force_offset = tare_force()

    with open('force_file.txt', 'r') as f:
        
        for line in f:
            # do another if statement where if there are two decimal places I should
            # delete the decimal place and everything after the decimal point
            
            floated = -(force_offset + float(line))
            force_list.append(floated)
            
    f.close()
    # print(force_list[23])
    print(len(force_list))
    return force_list

def format_torque(t_list):

    torque_list = []

    with open('torque_file.txt', 'w', newline = '') as f:
        for entry in t_list:
            if entry != '' and entry != '+\n' and entry!= '     ' and entry != '   \n' and entry != '   \n':

                if entry.count('.') == 2:
                            dindex = entry.find('.', entry.find('.') +1)
                            entry = entry[:dindex]
                
                f.write(f'{str(entry)}\n')

    f.close()

    torque_offset = tare_torque()

    with open('torque_file.txt', 'r') as f:
        
        for line in f:
            if line != '' and line != '+\n' and line!= '     ' and line != '   \n' and line != '  \n'and line!= '+  \n':

                floated = torque_offset + float(line[:7])
                torque_list.append(floated)
    f.close()
    # print(torque_list[23])
    print(len(torque_list))
    return torque_list

def format_time(start, times):

    time_list = []

    for time in times:
        diff = time - start # of type datetime.timedelta
        format_diff = diff.seconds + diff.microseconds/1000000
        time_list.append(format_diff)

    with open('time_file.txt', 'w') as t:
         for time in time_list:
              t.write(f'{time}\n')
    t.close()

    print(time_list[23])
    print(len(times))
    print(len(time_list))

    # with open('time_file.txt', 'w', newline = '') as f:
    #     for entry in times:
    #         f.write(f'{str(entry)}\n')
    # f.close()

    return time_list

def generate_csv_force(start, times, forces):
    with open('force'+start.strftime("%m_%d_%Y__%H_%M_%S") +'.csv', 'w', newline = '') as csvfile:
        force_writer = csv.writer(csvfile)
        # header = ['Time', 'Force_Reading']
        # force_writer.writerow(header)
        for num in range(len(forces)):
            force_writer.writerow([times[num], forces[num]])
        csvfile.close()

def generate_csv_torque(start, times, torques):
    with open('torque'+start.strftime("%m_%d_%Y__%H_%M_%S") +'.csv', 'w', newline = '') as csvfile:
        torque_writer = csv.writer(csvfile)
        # header = ['Time', 'Torque_Reading']
        # torque_writer.writerow(header)
        for num in range(len(torques)): ### THEY'RE NOT THE SAME SIZE GAAHHHH
            torque_writer.writerow([times[num], torques[num]])
        csvfile.close()

def tare_force():
    force_sample = []
    counter = 0
    while counter < 101:
        value = force_ser.readline()
        force_to_string = str(value, 'UTF-8')[:-5]

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
    gross = sum/100
    print(f'GROSS FORCE: {gross}')
    print(f'Standard Deviation: {stdev(force_sample)}')
    return gross

def tare_torque():
    torque_sample = []
    counter = 0
    while counter < 101:
        value = torque_ser.readline()
        torque_to_string = str(value, 'UTF-8')[:-7]

        if counter > 0:
            if torque_to_string != '':

                if torque_to_string.count('.') == 2:
                            dindex = torque_to_string.find('.', torque_to_string.find('.') +1)
                            torque_to_string = torque_to_string[:dindex]

                torque_to_float = -float(torque_to_string[:8])
                print(f'{torque_to_float} pound-inches')
                torque_sample.append(torque_to_float)
        
        counter += 1

    # Tare the sensor
    sum = 0

    # get the average gross number
    for num in torque_sample:
        sum += num
    gross = sum/100
    print(f'GROSS TORQUE: {gross}')
    print(f'Standard Deviation: {stdev(torque_sample)}')
    return gross

def execute_test(f_ser, t_ser):

    force_list = []
    torque_list = []
    time_list = []

    # f_unit = input('Choose unit for force: lbf or N')
    # t_unit = input('Choose unit for force: lb-in or Nm')

    new_time = start_time = datetime.datetime.now()
    end_time = start_time + datetime.timedelta(seconds = 10)

    # while new_time < end_time

    while new_time < end_time:
        time_list.append(new_time)
        #f_ser.flushInput()
        force_list.append(f_ser.readline().decode().strip('lbs\r\n'))
        #t_ser.flushInput()
        torque_list.append(t_ser.readline().decode().strip('in-lb\r\n'))
        
        new_time = datetime.datetime.now()
    print('Test finished')
    print(len(force_list))
    print(len(torque_list))
    print(len(time_list))

    time.sleep(40)

    forces = format_force(force_list)
    torques = format_torque(torque_list)
    times = format_time(start_time, time_list)

    generate_csv_force(start_time, times, forces)
    generate_csv_torque(start_time, times, torques)

if __name__ == "__main__":
    print('Sensor script has begun executing')
    try:
        force_ser = serial.Serial(port='COM27', baudrate=9600)
        print("Force Port Available")
    except:
        print("Force Port Unavailable")
        force_ser = 0
    try:
        torque_ser = serial.Serial(port = 'COM26', baudrate = 9600)
        print("Torque Port Available")
    except:
        print("Torque Port Unavailable")
        force_ser = 0
    execute_test(force_ser, torque_ser)
else:
    print("Error. Program cannot be accessed.")