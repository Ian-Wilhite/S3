
import numpy as np
from subfunctions import *
from Lab3_DefineRover import *
from scipy.optimize import root_scalar
import matplotlib.pyplot as plt

rover, planet = define_rover_1()

Crr = 0.2
slope_array_deg = np.linspace(-10, 35, 25)
omega_max = np.zeros(len(slope_array_deg), dtype=float)
omega_nl = rover['wheel_assembly']['motor']['speed_noload']

# Iterate over the slopes and calculate the maximum angular velocity for each
for ii in range(len(slope_array_deg)):
    # Define the net force function to find the root
    def F_net_at_omega(omega):
        return F_net(omega, float(slope_array_deg[ii]), rover, planet, Crr)

    # Find the root using the bisection method with a bracket from 0 to no-load speed
    sol = root_scalar(F_net_at_omega, method='bisect', bracket=[0, omega_nl])
    omega_max[ii] = sol.root

# Convert the angular velocity (rad/s) to linear velocity (m/s)
v_max = omega_max #* rover['wheel_assembly']['wheel']['radius']

# Plot v_max versus slope_array_deg
plt.plot(slope_array_deg, v_max)
plt.xlabel('Terrain Angle (degrees)')
plt.ylabel('Maximum Rover Velocity (m/s)')
plt.title('Rover Maximum Velocity vs Terrain Slope')
#plt.grid(True)
plt.show()