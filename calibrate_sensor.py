import serial
import datetime
import statistics

def get_mass(ser, f_offset):
    # counting = 0
    # mass_sum = 0
    # while counting < 20:

    #     value = ser.readline()
    #     value = (str(value)[2:9])
    #     if value != '' and value != "+\\n'":
    #         base_val = -force_offset + float(value)
    #         print(f'Read Value: {base_val}')
    #     counting += 1
    # mass_measured = mass_sum/20
    # print(f'Average Mass: {mass_measured}')
    force_list = []

    # f_unit = input('Choose unit for force: lbf or N')
    # t_unit = input('Choose unit for force: lb-in or Nm')

    new_time = start_time = datetime.datetime.now()
    end_time = start_time + datetime.timedelta(seconds = 10)

    # while new_time < end_time

    while new_time < end_time:
        value = ser.readline().decode().strip('lbs\r\n')
        if value != '' and value != "+\\n'":
            force_list.append(-f_offset + float(value)) 
        new_time = datetime.datetime.now()
    print(force_list)
    print(statistics.mean(force_list))

force_ser = serial.Serial(port='COM27', baudrate=9600)
counter = 0
val_list = 0

num_samples = 10

while counter < num_samples + 1:
        
    val = force_ser.readline()
    val = (str(val, 'UTF-8').strip().strip('lbs'))
    if counter > 0:    
        val_list += (float(val))
        print(f'Force Reading: {val}')
    counter += 1

# tare the sensor
force_offset = val_list/num_samples
print(force_offset)
print(type(force_offset))
counter = 0



#Sensor has been tared

# Take mass of known weights
answer = input("Click Y: ")

new_time = start_time = datetime.datetime.now()
end_time = start_time + datetime.timedelta(seconds = 5)
true_val_list = []

while new_time < end_time:

    val = force_ser.readline()
    val = (str(val, 'UTF-8').strip().strip('lbs'))
    val = val[:-7]
    if counter > 0:    
        if val != '' and val != '+' and val.count('.') != 2:
            val_list += (float(val))
            true_val = (-float(val) + force_offset) * 0.9979366668002273 * 1.0011572505878394 * 0.9990991939859979 *  0.9992328055174383 * 0.9981109383988359 * 0.99875058457423 * 0.9997503917419301 * 1.002537306756004 * 0.9976642714189242
            #true_val = (-float(val) + force_offset) * 0.99424399386
            print(f'Force Reading: {true_val}')
            if ((end_time - new_time).seconds + (end_time - new_time).microseconds/1000000) < 2:
                true_val_list.append(true_val)
    counter += 1
    new_time = datetime.datetime.now()
print(len(true_val_list))
print(f'Mass Recorded by Futek: {statistics.mean(true_val_list)}')
# calculate calibration ratio
actual = float(input("Enter the actual mass (in pounds): of the item being weighed: "))
cal_ratio = actual/statistics.mean(true_val_list)
print(f'Calibration Ratio: {cal_ratio}')
