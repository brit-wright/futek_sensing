import serial

ser = serial.Serial(port='COM27', baudrate=9600)

while True:
    value = ser.readline()
    torque_to_string = str(value, 'UTF-8')[:-7]
    print(torque_to_string)

    