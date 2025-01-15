import numpy as np
import matplotlib.pyplot as plt
from math import exp
from A4 import *

# Define the ODE
def func(t, y):
    return y * t **3 - 1.5*y

# Analytical solution
def actual(t):
    return np.exp((1/4)*t**4 - 1.5*t)



# Parameters
t0 = 0
y0 = 1  # Initial condition
tStop = 2



# Solve the problem using the methods
T_exact = np.linspace(t0, tStop, 100)
Y_exact = actual(T_exact)

# Euler's method with h = 0.5
T_euler_05, Y_euler_05 = euler_integrate(func, t0, y0, tStop, 0.5)

# Euler's method with h = 0.25
T_euler_025, Y_euler_025 = euler_integrate(func, t0, y0, tStop, 0.25)

# Midpoint method with h = 0.5
T_midpoint, Y_midpoint = midpoint_integrate(func, t0, y0, tStop, 0.5)

# Heun method with h = 0.5
T_heun, Y_heun = heun_integrate(func, t0, y0, tStop, 0.5)

# RK4 method with h = 0.5
T_RK4, Y_RK4 = RK4_integrate(func, t0, y0, tStop, 0.5)

# Plotting the results
plt.figure(figsize=(10, 6))
plt.plot(T_exact, Y_exact, label='Analytical solution', color='black', linewidth=2)

plt.plot(T_euler_05, Y_euler_05, label="Euler's method (h=0.5)", linestyle='--')
plt.plot(T_euler_025, Y_euler_025, label="Euler's method (h=0.25)", linestyle='--')
plt.plot(T_midpoint, Y_midpoint, label="Midpoint method (h=0.5)", linestyle=':')
plt.plot(T_heun, Y_heun, label="Heun's method (h=0.5)", linestyle='-.')
plt.plot(T_RK4, Y_RK4, label="RK4 method (h=0.5)", linestyle='-.')

# Labels and legend
plt.xlabel('t')
plt.ylabel('y(t)')
plt.title('Comparison of IVP Solvers')
plt.legend()
plt.grid(True)
plt.show()
