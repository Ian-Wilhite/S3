import numpy as np
import matplotlib.pyplot as plt
from subfunctions import tau_dcmotor  #import the function from subfunctions
from Lab3_DefineRover import define_rover_1  #import the define_rover_1 function

#get rover and planet information
rover, planet = define_rover_1()
motor = rover['wheel_assembly']['motor']  #extract motor data from the rover dict

#define a range of motor shaft torques and speeds for the analysis
speed_values = np.linspace(0, motor['speed_noload'], 100)  #use motor's no-load speed as the range

#use the tau_dcmotor function to compute motor shaft torque and power
motor_torque = np.array([tau_dcmotor(speed, motor) for speed in speed_values])

#assuming motor power = torque * speed (adjust if you have a different model)
motor_power = speed_values * motor_torque

#plotting the three graphs in a 3x1 array
plt.figure(figsize=(8, 12))

#1. motor shaft speed vs. motor shaft torque
plt.subplot(3, 1, 1)
plt.plot(motor_torque, speed_values, label='Speed vs Torque', color='b')
plt.xlabel('Motor Shaft Torque [Nm]')
plt.ylabel('Motor Shaft Speed [rad/s]')
plt.title('Motor Shaft Speed vs Torque')
plt.grid(True)

#2. motor power vs. motor shaft torque
plt.subplot(3, 1, 2)
plt.plot(motor_torque, motor_power, label='Power vs Torque', color='g')
plt.xlabel('Motor Shaft Torque [Nm]')
plt.ylabel('Motor Power [W]')
plt.title('Motor Power vs Torque')
plt.grid(True)

#3. motor power vs. motor shaft speed
plt.subplot(3, 1, 3)
plt.plot(speed_values, motor_power, label='Power vs Speed', color='r')
plt.xlabel('Motor Shaft Speed [rad/s]')
plt.ylabel('Motor Power [W]')
plt.title('Motor Power vs Speed')
plt.grid(True)

#adjust layout and save the figure
#plt.tight_layout()
plt.savefig('motor_performance_plots.png')
plt.show()

