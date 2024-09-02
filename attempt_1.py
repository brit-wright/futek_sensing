"""This program reads the serial port for 
bits which correspond to voltage change.
These bits are converted to analog readings.
The analog readings will be used alongside a
conversion factor to obtain the thrust and torque
experienced by the sensor"""

#import the necessary libraries
import serial
import time # idk why but this might be useful
import datetime

# defining important functions

# function to read the port data/signals
def read_data(f_port, t_port):

    new_time = start_time = datetime.datetime.now()
    end_time = start_time + datetime.timedelta(seconds = 3)

    force_dict = {}
    torque_dict = {}

    while new_time < end_time: #want to use another condition like...while is_running = True
        # print(new_time)
        force_val = str(f_port.readline(), 'UTF-8')
        thrust_val = str(t_port.readline(), 'UTF-8')
        new_time = datetime.datetime.now()
        index_val = new_time - start_time
        force_dict[index_val] = force_val
        torque_dict[index_val] = thrust_val
    
    full_list = [force_dict, torque_dict]

    return full_list

# function to print the port data/signals to .csv

# function to convert to analog(?)
def convert_to_analog(digital):
    
    # noise-free resolution of USB 220 is based on the sampling rate chosen
    # dictionary made using spec sheet
    res_dict = {5:17.8, 10:17.2, 100:16.4, 300:15.4, 1200:14.6, 2400:14, 4800:13.6}
    resolution = 2**res_dict[4800] # can be altered 
    
    v_ref = 4.6 # not sure, this is the bridge excitation voltage
    analog_force_dict = {}
    analog_torque_dict = {}
    for entry in digital[0]:
        analog_ver = digital[0][entry]/(resolution - 1) * v_ref
        analog_force_dict[entry] = analog_ver
    for entry in digital[1]:
        analog_ver = digital[1][entry]/(resolution - 1) * v_ref
        analog_torque_dict[entry] = analog_ver
    full_analog_list = [analog_force_dict, analog_torque_dict]
    return full_analog_list
    
# function to convert the analog signals to force/torque
#WHAT IS THE CONVERSION FACTOR AHHHH
# Chat gpt says the formula is Load = Voltage Output/(Sensitivity*Excitation Voltage) * Load Capacity
# I think I should just calibrate it myself --> TEEHEE?
# https://youtu.be/nGUpzwEa4vg?si=tQSG3KgtDzQ0iX7R 

def convert_to_force(force_voltage_dict):
    force_factor = 0
    force_dict = {}
    for key_val in force_voltage_dict:
        force_val = force_factor * force_voltage_dict[key_val]
        force_dict[key_val] = force_val
    return force_dict

def convert_to_torque(torque_voltage_dict):
    torque_factor = 0
    torque_dict = {}
    for key_val in torque_voltage_dict:
        torque_val = torque_factor * torque_voltage_dict[key_val]
        torque_dict[key_val] = torque_val
    return torque_dict


# initialize the ports
force_port = serial.Serial(port = 'COM30', baudrate = 9600)
thrust_port = serial.Serial(port = 'COM31', baudrate = 9600)

time.sleep(2) #chatgpt says this waits for the connection to establish


data = read_data(force_port, thrust_port) # type [{force_dict}, {torque_dict}]

voltages = convert_to_analog(data) # type [{analog_force_dict}, {analog_torque_dict}]

force_list = convert_to_force(voltages[0]) # type {time: force}

torque_list = convert_to_torque(voltages[1]) # type {time: torque}