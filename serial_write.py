import ctypes
import serial
import datetime
import time

# Load the DLL file
# futek_dll = ctypes.CDLL(r"C:\Users\britt\OneDrive\Desktop\For_Futek\FUTEK_USB_DLL.dll")

ser = serial.Serial(port='COM26', baudrate=9600)
flist = []
tlist = []

new_time = start_time = datetime.datetime.now()
end_time = start_time + datetime.timedelta(seconds = 10)
counter = 0

while True:
# while new_time < end_time:
    ser.reset_input_buffer
    ser.reset_output_buffer

    fvalue = ser.readline()
    print(fvalue)
    counter +=1 
    new_time = datetime.datetime.now()
    # if new_time >= end_time:
    #     break


print(len(flist))
print(counter)    