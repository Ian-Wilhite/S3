from subfunctions import *
import numpy as np
import scipy.interpolate as sc
import matplotlib.pyplot as plt
from define_experiment import *

# Load rover and experiment definitions
rover, planet = define_rover_1()
experiment, end_event = experiment1()

# Set end_event fields as required
end_event['max_distance'] = 1000
end_event['max_time'] = 2500
end_event['min_velocity'] = 0.01

# Simulate rover trajectory
simulate_rover(rover, planet, experiment, end_event)

# Extract telemetry data
time = np.array(rover['telemetry']['Time'])
position_data = np.array(rover['telemetry']['position'])
velocity_data = np.array(rover['telemetry']['velocity'])
power_data = np.array(rover['telemetry']['power'])

# Create interpolation functions for smooth plotting
time_smooth = np.linspace(0, time[-1], 100)
position_interp = sc.interp1d(time, position_data, kind='cubic', fill_value='extrapolate')(time_smooth)
velocity_interp = sc.interp1d(time, velocity_data, kind='cubic', fill_value='extrapolate')(time_smooth)
power_interp = sc.interp1d(time, power_data, kind='cubic', fill_value='extrapolate')(time_smooth)

# Plot the data in a 3x1 arrangement
plt.figure(figsize=(8, 12))

# Position vs Time
plt.subplot(3, 1, 1)
plt.plot(time_smooth, position_interp, label='Position', color='blue')
#plt.scatter(time, position_data, color='blue', label='Data points')
plt.title('Position vs Time')
plt.xlabel('Time [s]')
plt.ylabel('Position [m]')
plt.grid(True)

# Velocity vs Time
plt.subplot(3, 1, 2)
plt.plot(time_smooth, velocity_interp, label='Velocity', color='green')
#plt.scatter(time, velocity_data, color='green', label='Data points')
plt.title('Velocity vs Time')
plt.xlabel('Time [s]')
plt.ylabel('Velocity [m/s]')
plt.grid(True)

# Power vs Time
plt.subplot(3, 1, 3)
plt.plot(time_smooth, power_interp, label='Power', color='red')
#plt.scatter(time, power_data, color='red', label='Data points')
plt.title('Power vs Time')
plt.xlabel('Time [s]')
plt.ylabel('Power [W]')
plt.grid(True)

plt.subplots_adjust(wspace=0.1, hspace=0.1)  # wspace controls the width space, hspace controls the height space
#plt.tight_layout()
plt.show()

# Print the telemetry data summary
completion_time = rover['telemetry']['Time'][-1]
distance_traveled = rover['telemetry']['position'][-1]
max_velocity = np.max(rover['telemetry']['velocity'])
average_velocity = np.mean(rover['telemetry']['velocity'])
battery_energy = rover['telemetry']['battery_energy']
batt_energy_per_distance = battery_energy / distance_traveled

print("Telemetry Summary:")
print(f"Completion Time: {completion_time:.2f} s")
print(f"Distance Traveled: {distance_traveled:.2f} m")
print(f"Max Velocity: {max_velocity:.2f} m/s")
print(f"Average Velocity: {average_velocity:.2f} m/s")
print(f"Battery Energy: {battery_energy:.2f} J")
print(f"Battery Energy per Distance: {batt_energy_per_distance:.2f} J/m")
