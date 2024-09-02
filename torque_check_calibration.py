import serial
import datetime
import statistics

torque_ser = serial.Serial(port='COM26', baudrate=9600)
counter = 0
val_list = 0

num_samples = 10
torque_ser.reset_input_buffer()
while counter < num_samples + 1:
        
    val = torque_ser.readline()
    val = (str(val, 'UTF-8').strip().strip('in-lbs'))
    if counter > 0:    
        val_list += (float(val))
        print(f'Torque Reading: {val}')
    counter += 1

# tare the sensor
torque_offset = val_list/num_samples
print(torque_offset)
print(type(torque_offset))
counter = 0

# Take mass of known weights
answer = input("Click Y: ")

new_time = start_time = datetime.datetime.now()
end_time = start_time + datetime.timedelta(seconds = 5)
true_val_list = []

torque_ser.reset_input_buffer()
while new_time < end_time:
    val = torque_ser.readline()
    val = (str(val, 'UTF-8').strip().strip('in-lbs'))
    # val = val[:-7]
    if counter > 0:    
        if val != '' and val != '+' and val.count('.') != 2 and val != '  ': 
            val_list += (float(val))
            true_val = (float(val))
            print(f'Torque Reading: {true_val}')
            # if ((end_time - new_time).seconds + (end_time - new_time).microseconds/1000000) < 2:
            if true_val > 1:
                true_val_list.append(true_val)
    counter += 1
    new_time = datetime.datetime.now()
print(len(true_val_list))
print(true_val_list)
recorded_torque = ((statistics.mean(true_val_list) - torque_offset)) * (1.042734793904364 * 0.9973240913059526 * 1.0024564494210493 * 1.0234968035481375*0.9774168633129849) * (0.9798849015665653 * 0.9987893176305618 * 1.0007100078419715) * 1.0108
print(f'Average torque measured (without adjustments): {statistics.mean(true_val_list)}')
print(f'Adjusted Torque Recorded by Futek: {recorded_torque}')
print(f'Torque Offset: {torque_offset}')
# calculate calibration ratio
actual = float(input("Enter the actual torque (in lb-in): "))
cal_ratio = actual/recorded_torque
print(f'Calibration Ratio: {cal_ratio}')
