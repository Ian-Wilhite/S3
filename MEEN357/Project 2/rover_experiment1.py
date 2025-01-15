
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from define_experiment import experiment1  # Ensure you have this file downloaded and in the same directory
from subfunctions import *  # Assuming this contains your simulate_rover function


experiment, planet = experiment1()  # Load experiment and planet dictionaries

end_event = {
    'max_distance': 1000,
    'max_time': 10000,
    'min_velocity': 0.01,
}


rover = {
    'telemetry': {}
}  # Initialize the rover dictionary (expand with other necessary parameters)

# Simulate the rover
rover = simulate_rover(rover, planet, experiment, end_event)


# Extract telemetry data
time_data = rover['telemetry']['time']  # Assuming time is stored in the telemetry
position_data = rover['telemetry']['position']  # Assuming position is stored in the telemetry
velocity_data = rover['telemetry']['velocity']  # Assuming velocity is stored in the telemetry
power_data = rover['telemetry']['power']  # Assuming power is stored in the telemetry

# Create a single figure with three subfigures (3x1 arrangement)
fig, axs = plt.subplots(3, 1, figsize=(10, 15))

# Position vs. Time
axs[0].plot(time_data, position_data, label='Position', color='blue')
axs[0].set_title('Position vs. Time')
axs[0].set_xlabel('Time (s)')
axs[0].set_ylabel('Position (m)')
axs[0].grid()
axs[0].legend()

# Velocity vs. Time
axs[1].plot(time_data, velocity_data, label='Velocity', color='orange')
axs[1].set_title('Velocity vs. Time')
axs[1].set_xlabel('Time (s)')
axs[1].set_ylabel('Velocity (m/s)')
axs[1].grid()
axs[1].legend()

# Power vs. Time
axs[2].plot(time_data, power_data, label='Power', color='green')
axs[2].set_title('Power vs. Time')
axs[2].set_xlabel('Time (s)')
axs[2].set_ylabel('Power (W)')
axs[2].grid()
axs[2].legend()

# Save the figure
plt.tight_layout()
plt.savefig('rover_simulation_results.png')
plt.show()


# Summary Table
telemetry_summary = {
    'Completion Time (s)': rover['telemetry']['completion_time'],
    'Distance Traveled (m)': rover['telemetry']['distance_traveled'],
    'Max Velocity (m/s)': rover['telemetry']['max_velocity'],
    'Average Velocity (m/s)': rover['telemetry']['average_velocity'],
    'Battery Energy (J)': rover['telemetry']['battery_energy'],
    'Energy per Distance (J/m)': rover['telemetry']['batt_energy_per_distance'],
}

# Print the summary table
print("Rover Telemetry Summary:")
for key, value in telemetry_summary.items():
    print(f"{key}: {value}")
