# futek_sensing
This repository is for interfacing with the Futek MBA500 (Thrust/Torque Biaxial Sensor) over USB220. This repository was specifically developed to characterize the thrust and torque of a ds-51-axi hds thruster but this code is suitable for general sensing applications. All code is written in Python

# useful libraries
I recommend having the following Python modules installed: pyserial, datetime, csv, time, statistics. These allow for serial communication with the sensor, timed tests, storing results as .csv and computing standard deviation (if needed).

# thrust/torque calibration
calibratesensor.py contains instructions for calibrating the force sensor. In this code, the sensor is first tared (with no mass on the sensor). Next, the user is instructed to place the object of known weight (to be used for calibration) on the sensor. The sensor will output an average of the force readings taken for 5 seconds. The user will input the actual weight of the object and then the program will calculate the calibration factor. It is recommended for the user to (in line 76) multiply that calibration factor by the true value formula (as shown in the script). The experiment will then be repeated and the new calibration factors calculated will be multiplied by previous factors. Repeat this until desired accuracy is achieved.

check_torque_calibration.py contains similar instructions for calibrating the torque sensor. For this experiment, it is recommended to use a setup similar to the one shown in torque_calibration_setup.jpg. The arm is 3D-printed with a high infill (70%). The method for torque calibration is similar to force calibration. Note that the sensor must be tared with the torque arm attached.

# force hysteresis testing
The force hysteresis test can be done to assess the repeatability of readings and to further assess the success of force calibration. In this experiment, multiple objects of known weight will be stacked and unstacked (in reverse order). This test is done in hysteresis.py where each new reading involves a new object being stacked or unstacked. The user will note the forces recorded by the sensor for each new reading.

Then in the plot_hysteresis.py script, the user will plot the sensor data for loading and unloaded against the true data for loading and unloaded. This plot can be used to assess how closely the loading and unloading plots match. Furthermore, this code also fits the loading and unloading data to polynomials such that a y-intercept and gradient for each line can be calculated and compared to one another to further evaluate hysteresis. plot_hysteresis.py contains results from a hysteresis experiment I conducted. I recommend running the code to better understand the script.

# torque vibration testing
optim_check_torque_oscillation.py can be used to conduct vibration tests. The purpose of this experiment is to test how good the sensor is at tracking vibrations. For this experiment, I used the same setup as shown in torque_calibration_setup.jpg. A string is tied to an object of known weight and during the test, the object is constantly dropped on the arm and the arm is allowed to vibrate. At the end of the test, the plot should resemble an exponentially decaying sine wave. [include picture of the vibration graph]

# thruster test
ver4_pyserial_serial_port_comm.py can be used to conduct the thrust test. Other versions of the code ver2 and ver3 are less efficient. [explain experiment setup]
