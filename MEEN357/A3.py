# Ian Wilhite 9/22/2024
# Meen 357 solo

import numpy as np
import matplotlib.pyplot as plt
#import math

actual_value = 98.4276846159
#task 1: Strategy for Coding a Numerical Integration Routine
""" 
- area of a rectangle is length times width
- riemmien sum over a curve = sum( f(x) * dx)
"""

def simpint(x, fx):
    if(type(x) != np.ndarray or type(fx) != np.ndarray):
        raise TypeError("x and fx must be np arrays")
    if x.size != fx.size:
        raise ValueError(f"x and fx must have the same length. Got lengths {x.size} and {fx.size}")
    if not (x.size == 3 or x.size == 4):
        raise ValueError(f"x and fx must have a length of 3 or 4 for Simpson's rule. Got length {x.size}")
    
    # simpsons 3/8th rule
    if(x.size == 3):
        sum = fx[0] + 4 * fx[1] + fx[2]
        return ((x[2] - x[0]) / 6 ) * sum
        
    else: # len == 4
        sum = fx[0] + 3 * fx[1] + 3 * fx[2] + fx[3]
        return ((x[3] - x[0]) / 8 ) * sum
    
def fx(x):
    return (x ** 2) * (np.e ** x)

def fx_4th(x, c):
    return c * x ** 4

step_sizes = [1.5, 1.0, 0.75, 0.5, 0.38, 0.33, 0.3, 0.25]
numsteps = []

for step in step_sizes:
    numsteps += [round(3 / step)]

simps_onethird_steps = []
simps_threeeighths_steps = []

for num in numsteps:
    if num % 2 == 0:
        simps_onethird_steps += [num]
        
    if num % 3 == 0:
        simps_threeeighths_steps += [num]

"""
1.5   (-1, -1) # two points means trapezoidal
1.0   (1, 0.0)
0.75   (0, 1.0)
0.5   (2, 0.0)
0.38   (0, 2.0)
0.33   (3, 0.0)
0.3   (2, 1.0)
0.25   (0, 3.0)

"""
simps_onethird_areas = []

for steps in simps_onethird_steps:
    step_size = 3 / steps
    x_vals = np.arange(0, 3 + step_size, step_size)
    area = 0
    ptr = 0
    while ptr + 2 < len(x_vals):  # Ensure enough points for Simpson's 1/3 rule
        area += simpint(x_vals[ptr:ptr + 3], fx(x_vals[ptr:ptr + 3]))
        ptr += 2
    simps_onethird_areas.append(area)
        
    
simps_threeeighths_areas = []

for steps in simps_threeeighths_steps:
    step_size = 3 / steps
    x_vals = np.arange(0, 3 + step_size, step_size)
    area = 0
    ptr = 0
    while ptr + 3 < len(x_vals):  # Ensure enough points for Simpson's 3/8 rule
        area += simpint(x_vals[ptr:ptr + 4], fx(x_vals[ptr:ptr + 4]))
        ptr += 3
    simps_threeeighths_areas.append(area)
    

print(simps_onethird_steps)
print(simps_threeeighths_steps)
    
print(simps_onethird_areas)
print(simps_threeeighths_areas)

for i in range(len(simps_onethird_areas)):
    print(f'({simps_onethird_steps[i]}, {simps_onethird_areas[i]})')

for i in range(len(simps_threeeighths_areas)):
    print(f'({simps_threeeighths_steps[i]}, {simps_threeeighths_areas[i]})')

fig, axs = plt.subplots(1, 2) 



# -------------------------------------------------------------------------------------
#2 - a

axs[0].plot([3/step for step in simps_onethird_steps], simps_onethird_areas)
axs[0].plot([3/step for step in simps_threeeighths_steps], simps_threeeighths_areas)
axs[0].axhline(y=actual_value)
axs[0].set_ylabel("integral approximation")
axs[0].set_xlabel("step size")
axs[0].legend(["Simposon's 1/3", "Simposon's 3/8"], loc="upper left")


# -------------------------------------------------------------------------------------
#2 - b


percent_error_onethird = [abs(actual_value - area) / actual_value * 100 for area in simps_onethird_areas]
percent_error_threeeighths = [abs(actual_value - area) / actual_value * 100 for area in simps_threeeighths_areas]

print(percent_error_onethird)
print(percent_error_threeeighths)

for i in range(len(percent_error_onethird)):
    print(f'({3/simps_onethird_steps[i]}, {percent_error_onethird[i]})')

for i in range(len(percent_error_threeeighths)):
    print(f'({3/simps_threeeighths_steps[i]}, {percent_error_threeeighths[i]})')
    
axs[1].plot([3/step for step in simps_onethird_steps], percent_error_onethird)
axs[1].plot([3/step for step in simps_threeeighths_steps], percent_error_threeeighths)
axs[1].axhline(y=0)
axs[1].set_ylabel("true percent relative error")
axs[1].set_xlabel("step size")
axs[1].legend(["Simposon's 1/3", "Simposon's 3/8"], loc="upper left")



plt.show() 