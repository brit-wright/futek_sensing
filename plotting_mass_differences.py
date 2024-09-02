#it's plottin time 
import numpy as np
import matplotlib.pyplot as plt
import scipy

actual_masses = [0.4375, 0.70625, 0.99375, 1.14375, 1.43125, 1.69375, 2.4875, 3.1875, 3.48125, 3.91875, 4.18125, 4.9125, 4.625, 5.61875, 6.40625, 7.1125, 8.10625]
futek_masses = [0.43889229299422305, 0.6932093930692513, 0.986528272111796, 1.1416561552251034, 1.4341343926355092, 1.687429205555969, 2.4881550264275947, 3.1933527562993156, 3.487365078029037, 3.9203285449600993, 4.173360683713612, 4.90710843348128, 4.626626735814732, 5.623471534285906, 6.416062501540573, 7.110614556804874, 8.106659831541593]

x = np.array(actual_masses)
y = np.array(futek_masses)

# s = UnivariateSpline(x, y, s = -5)
# xs = np.linspace(0, 9, 100)
# ys = s(xs)

# plt.scatter(x, y, color='green')
# plt.plot(xs, ys)
# plt.show()

# # do a least squares curve fit on line

# # scipy.optimize.curve_fit


# # Perform least squares fit (polynomial of degree 1 for linear fit)
# coefficients = np.polyfit(x, y, 1)
# polynomial = np.poly1d(coefficients)

# # Generate y values from the fit line
# y_fit = polynomial(x)

# # Plot the data points
# plt.plot(x, y, 'o', label='Data points')

# # Plot the least squares fit line
# plt.plot(x, y_fit, '-', label='Least squares fit')

# # Add labels and title
# plt.xlabel('X values')
# plt.ylabel('Y values')
# plt.title('Least Squares Fit of Y against X')

# calculate the polynomial
z = np.polyfit(x, y, 1)
print(z)
f = np.poly1d(z)
ys = f(x)
plt.plot(x, ys)
plt.scatter(x, y)

plt.show()