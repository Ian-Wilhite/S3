from subfunctions import *
from Lab3_DefineRover import define_rover_1

rover = define_rover_1()
effcy_tau = rover['wheel_assembly']['motor']['effcy_tau']
effcy = rover['wheel_assembly']['motor']['effcy']

# Create cubic spline interpolation function
effcy_fun = interp1d(effcy_tau, effcy, kind='cubic')

# Define torque values for interpolation
torque_values = np.linspace(effcy_tau.min(), effcy_tau.max(), 100)
interpolated_effcy = effcy_fun(torque_values)




