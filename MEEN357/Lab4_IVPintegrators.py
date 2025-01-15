# Lab4_IVPintegrators.py

import numpy as np

def euler_integrate(func, x0, y0, x_end, h):
    """
    Perform Euler integration on an initial value problem.

    Parameters:
    - func: The function handle, dy/dx = f(x, y), to integrate.
    - x0: Initial x value.
    - y0: Initial y value.
    - x_end: Stopping point for x.
    - h: Step size.

    Returns:
    - x_vals: Array of x values at each step.
    - y_vals: Array of y values at each step.
    """
    # Initialize the lists to store x and y values
    x_vals = [x0]
    y_vals = [y0]
    
    # Perform Euler's method until x reaches the stopping point
    while x_vals[-1] < x_end:
        # Get the current x and y
        x_current = x_vals[-1]
        y_current = y_vals[-1]
        
        # Calculate the next y value using Euler's method
        y_next = y_current + h * func(x_current, y_current)
        
        # Update x for the next step
        x_next = x_current + h
        
        # Append the new values to the lists
        x_vals.append(x_next)
        y_vals.append(y_next)
    
    # Convert lists to numpy arrays for easy manipulation
    return np.array(x_vals), np.array(y_vals)
