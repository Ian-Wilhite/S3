import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from define_experiment import experiment1
# by Jacob Hargreaves - 10/20/24 for MEEN 357 rover project 2 w/ David Guess & Ian Wilhite

# Load the experiment data
experiment, _ = experiment1()

# Extract the terrain data
alpha_dist = experiment['alpha_dist']
alpha_deg = experiment['alpha_deg']

# Create the interpolation function
alpha_fun = interp1d(alpha_dist, alpha_deg, kind='cubic', fill_value='extrapolate')

# Create 100 evenly spaced points for evaluation
x_eval = np.linspace(alpha_dist.min(), alpha_dist.max(), 100)
y_eval = alpha_fun(x_eval)

# Create the plot
plt.figure(figsize=(10, 6))
plt.plot(x_eval, y_eval, '-', label='Interpolated Terrain')
plt.plot(alpha_dist, alpha_deg, '*', label='Data Points')
plt.xlabel('Position (m)')
plt.ylabel('Terrain Angle (degrees)')
plt.title('Terrain Profile')
plt.legend()
plt.grid(True)
plt.show()