import serial
import datetime
import time

fser = serial.Serial(port='COM27', baudrate=9600, timeout=1)
tser = serial.Serial(port='COM26', baudrate=9600, timeout=1)
flist = []
tlist = []
tser.reset_input_buffer()
tser.reset_output_buffer()

new_time = start_time = datetime.datetime.now()
end_time = start_time + datetime.timedelta(seconds = 10)
counter = 0

while new_time < end_time:
# while True:
    # fvalue = fser.readline().decode('utf-8')
    fvalue = fser.readline().decode('utf-8')
    # flist.append(fvalue)
    flist.append(fvalue)
    counter +=1 
    new_time = datetime.datetime.now()
    print(fvalue)

print(len(flist))
print(len(tlist))
print(counter)
    