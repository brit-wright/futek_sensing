import serial
import datetime
import statistics


torque_ser = serial.Serial(port='COM26', baudrate=9600)
counter = 0
val_list = 0
arm_val_list = 0


prompt = 'Press Y to input your own values and N to re-measure the tare torque and arm torque. '
response = input(prompt)

if (response == 'Y') or (response == 'y'):
    torque_offset = float(input('Enter the gross torque of the sensor: '))
    arm_torque_offset = float(input('Enter the torque of the sensor with the arm attached: '))
else:
    # GET TORQUE ONLY OF SENSOR (SHOULD BE AROUND 0.24)

    num_samples = 30

    while counter < num_samples + 1:
        torque_ser.reset_input_buffer()
        print(torque_ser.in_waiting)
        val = torque_ser.readline()
        val = (str(val, 'UTF-8').strip().strip('lbs-in'))
        if counter > 0: 
            if val != '' and val != '+' and val.count('.') != 2:
                val_float = float(val[:8])   
                val_list += val_float
                print(f'Torque Reading: {val_float}')
        counter += 1

    # tare the sensor
    torque_offset = val_list/num_samples
    print(torque_offset)
    print(type(torque_offset))
    counter = 0

    print('The average torque value of the sensor only has been recorded.')

    # GET TORQUE OF ONLY ARM + BOLTS (SHOULD BE AROUND 0.113)

    answer = input('Change the orientation of the sensor and click Y when done. ')

    arm_num_samples = 30

    while counter < num_samples + 1:
        torque_ser.reset_input_buffer()
        print(torque_ser.in_waiting)
        arm_val = torque_ser.readline()
        arm_val = (str(arm_val, 'UTF-8').strip().strip('lbs-in'))
        if counter > 0:
            arm_val_float = float(arm_val[:8])    
            arm_val_list += arm_val_float
            print(f'Torque Reading: {arm_val_float}')
        counter += 1

    # tare the sensor
    arm_torque_offset = arm_val_list/arm_num_samples
    print(arm_torque_offset)
    print(type(arm_torque_offset))
    counter = 0
    #Sensor has been tared

# Take mass of known weights
answer = input("Click Y: ")

new_time = start_time = datetime.datetime.now()
end_time = start_time + datetime.timedelta(seconds = 5)
true_val_list = []

while new_time < end_time:
    torque_ser.reset_input_buffer()
    val = torque_ser.readline()
    val = (str(val, 'UTF-8').strip().strip('lbs'))
    val = val[:-7]
    if counter > 0:    
        if val != '' and val != '+' and val.count('.') != 2:
            val_list += (float(val))
            true_val = (float(val))
            print(f'Torque Reading: {true_val}')
            # if ((end_time - new_time).seconds + (end_time - new_time).microseconds/1000000) < 2:
            if true_val < 0:
                true_val_list.append(true_val)
    counter += 1
    new_time = datetime.datetime.now()
print(len(true_val_list))
print(true_val_list)
actual_arm_torque = arm_torque_offset - torque_offset
recorded_torque = ((statistics.mean(true_val_list) - torque_offset) - actual_arm_torque) * (-0.9980242908389914 * 1.0159514656155124 * 1.0061498743216253 * 0.994759255032 * 0.9992285428459807) *(1.0044194447822277*1.0058888387503069*0.9963883760432045*0.992546236350996*0.9972841255742625) * 1.0051329185997395 * 0.9971789475175031
print(f'Average torque measured (without adjustments): {statistics.mean(true_val_list)}')
print(f'Adjusted Torque Recorded by Futek: {recorded_torque}')
# calculate calibration ratio
actual = float(input("Enter the actual torque (in lb-in): "))
cal_ratio = actual/recorded_torque
print(f'Calibration Ratio: {cal_ratio}')
