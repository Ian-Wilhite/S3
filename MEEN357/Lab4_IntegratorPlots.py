import numpy as np
import matplotlib.pyplot as plt
from Lab4_IVPintegrators import *


def dfdx(x, y):
    return ((y * (x ** 3)) -( 1.5 * y))

h_vals = [0.5, 0.25, 0.125, 0.06125]
for h in h_vals:
    xvals, yvals = euler_integrate(dfdx, 0, 1, 2, h)
    #xvals, yvals = euler_integrate(dfdx, 0, 1, 2)
    print(xvals)
    print(yvals)

    plt.plot(xvals, yvals, label=f'h = {h}')


def sol_func(x):
    return np.e ** (1 / 4 * (x ** 4) - 1.5 * x)

sol_x_vals = np.arange(0, 2, 0.01)
sol_y_vals = sol_func(sol_x_vals)

plt.plot(sol_x_vals, sol_y_vals, label="actual solution")

#plt.legend("h = 0.5", "h = 0.25", "h = 0.125", "h = 0.06125", "actual solution")
plt.legend()
plt.show()