import numpy as np
import matplotlib.pyplot as plt

# read date from time file into a string:
timing = []
timer = open('vib_torque_time_file.txt', 'r')
for line in timer:
    timing.append(float(line.strip()))

print(timing)
print(timing[0])
print(timing[len(timing)-1])

dt_list = []

# get the list of dt values
for num in range(1, len(timing)):
    dt_list.append(timing[num]-timing[num-1])
# print (dt_list)

# plot the list of dt values

x = np.arange(0, len(timing)-1)
y = np.array(dt_list)
# x = np.arange(0, 10)
# y = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
plt.title('DT PLOT')
plt.ylabel('dt values')
plt.plot(x, y, color = "green")
plt.show()