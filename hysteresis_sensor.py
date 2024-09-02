import serial
import datetime
import statistics

def get_mass(ser, f_offset):
    force_list = []

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
response = input('Take mass reading? Enter y: ')
while response == 'y':
    answer = input("Click Y: ")

    new_time = start_time = datetime.datetime.now()
    end_time = start_time + datetime.timedelta(seconds = 5)
    true_val_list = []

    while new_time < end_time:

        val = force_ser.readline()
        val = (str(val, 'UTF-8').strip().strip('lbs'))
        val = val[:9]
        if counter > 0:    
            if val != '' and val != '-' and val != '+' and val.count('.') != 2 and val!='+    ' and val.count('l')==0 and val != '-    ':
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

    response = input("New reading? Click y: ")
