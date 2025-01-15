from subfunctions import *
from Lab3_DefineRover import define_rover_1
import numpy as np

omega = np.linspace(-10, 10, 20)
rover1, planet = define_rover_1()
terrain_angle = 5#degrees
Crr = 0.2 

f_roll = F_rolling(omega, terrain_angle, rover1, planet, Crr)
print(f_roll)


