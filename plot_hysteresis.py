# going to plot the hysteresis from loading and unloading the
# force sensor

import numpy as np
import matplotlib.pyplot as plt
import scipy

loading_data = [-0.000979161667560276, 0.7011855946234941, 1.6915295070343823, 5.616972847885771, 8.108198109690802, 8.549305315279245]

unloading_data = [8.106953002432796, 5.612746439604761, 1.687294930724289, 0.6973308232998933, -0.003723712307176581]

true_loading = [0, 0.70625, 1.7, 5.61875, 8.10625, 8.55]

true_unloading = [8.10625, 5.61875, 1.7, 0.70625, 0]

x1 = np.array(true_loading)
y1 = np.array(loading_data)
x2 = np.array(true_unloading)
y2 = np.array(unloading_data)

z1 = np.polyfit(x1, y1, 1) # gets the coefficients
print(f'Coefficients of Loading Polynomial: {z1}')
f1 = np.poly1d(z1) # gets the polynomial
ys1 = f1(x1)

z2 = np.polyfit(x2, y2, 1) # gets the coefficients
print(f'Coefficients of Unloading Polynomial: {z2}')
f2 = np.poly1d(z2) # gets the polynomial
ys2 = f2(x2)

# plotting the results
plt.plot(x1, ys1, color = 'green')
plt.scatter(x1, y1, color = 'green')

plt.plot(x2, ys2, color = 'blue')
plt.scatter(x2, y2, color = 'blue')

plt.show()
