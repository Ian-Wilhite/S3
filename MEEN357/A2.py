from math import *

def bisection(func, lb, ub, err_max=1e-5, iter_max=100):
    # Validate input
    if func(lb) * func(ub) > 0:
        return None, None, 0, -1  # Invalid bracket, no root found
    
    if lb > ub:
        raise Exception("Lower bound must be less than upper bound.")
    
    if not isinstance(iter_max, int) or iter_max <= 0:
        raise Exception("Maximum iterations must be a positive integer.")
    
    if not isinstance(err_max, (int, float)) or err_max <= 0:
        raise Exception("Error tolerance must be a positive number.")
    
    # Initialize values
    num_iter = 0
    root = lb
    err = float('inf')
    
    while num_iter < iter_max and err > err_max:
        root = (lb + ub) / 2.0  # Midpoint
        f_root = func(root)
        f_lb = func(lb)
        num_iter += 1

        # Check if root is found
        if f_root == 0 or abs(ub - lb) / abs(root) < err_max:
            return root, 0, num_iter, 1  # Root found, exit flag = 1
        
        # Update bounds
        if f_lb * f_root < 0:
            ub = root
        else:
            lb = root
        
        # Compute error and increment iteration
        err = abs(ub - lb) / abs(root)
        
    
    if num_iter == iter_max:
        return root, err, num_iter, 0  # Max iterations reached
    return root, err, num_iter, 1  # Root found successfully

"""
Secant Rootfinding pseudocode:

def secant(vals):
    init vars
    validate input
    
    while (rel_err < tol && num_it < max_it){
        find val at ub and lb
        
        update relative err
        move bounds
        num_it++
        
    }
    return root, error, iterations, and exit


"""

def secant(func, x0, err_max=1e-5, iter_max=100):
    # Initial guess for second point close to x0
    x1 = x0 + 1e-4
    
    # Validate input
    if not isinstance(iter_max, int) or iter_max <= 0:
        raise Exception("Maximum iterations must be a positive integer.")
    
    if not isinstance(err_max, (int, float)) or err_max <= 0:
        raise Exception("Error tolerance must be a positive number.")
    
    # Initialize values
    num_iter = 0
    err = float('inf')
    f_x0 = func(x0)
    f_x1 = func(x1)
    
    if f_x0 == 0:
        return x0, 0, 0, -1
    
    while num_iter < iter_max and err > err_max:
        # Check if function evaluation is valid
        if f_x0 == f_x1:
            return None, None, num_iter, -2  # Avoid division by zero
        
        # Secant formula to find next approximation
        x_new = x1 - f_x1 * (x1 - x0) / (f_x1 - f_x0)
        
        # Compute relative error
        err = abs((x_new - x1) / x_new) if x_new != 0 else float('inf')
        
        # Update guesses
        x0, x1 = x1, x_new
        f_x0, f_x1 = f_x1, func(x1)
        
        # Increment iteration count
        num_iter += 1
    
    if num_iter == iter_max:
        return x1, err, num_iter, 0  # Max iterations reached
    return x1, err, num_iter, 1  # Root found successfully


def falsepos(func, lb, ub, err_max=1e-5, iter_max=100):
    
    # Validate the initial bounds (ensure they bracket the root)
    f_lb = func(lb)
    f_ub = func(ub)
    
    if f_lb * f_ub > 0:
        return None, None, 0, -1  # Invalid bracket, no root found
    
    # Initialize variables
    num_iter = 0
    root = lb
    err = float('inf')  # Initialize with a large error value
    
    while num_iter < iter_max and err > err_max:
        # Compute the false position (new root estimate)
        root = ub - f_ub * (ub - lb) / (f_ub - f_lb)
        f_root = func(root)
        
        # Check if root is found or within error tolerance
        if f_root == 0 or abs(f_root) < err_max:
            return root, 0, num_iter, 1  # Root found
        
        # Update bounds and the function values
        if f_lb * f_root < 0:
            ub = root
            f_ub = f_root
        else:
            lb = root
            f_lb = f_root
        
        # Calculate relative approximation error
        err = abs(ub - lb) / abs(root)
        num_iter += 1
    
    if num_iter == iter_max:
        return root, err, num_iter, 0  # Max iterations reached
    
    return root, err, num_iter, 1  # Root found successfully


#Task 5

#a) y = x * sin (x) + 3 * cos(x) - x
def t5_a(x): #task 5a
    return x * sin (x) + 3 * cos(x) - x

print("Task 5: function A")
print(secant(t5_a, 0))
print(secant(t5_a, 6))
print(bisection(t5_a, 0, 6))

# 

#b) y = x * (sin(x) - x * cos(x))

def t5_b(x): #task 5a
    return x * (sin(x) - x * cos(x))

print("Task 5: function B")
print(secant(t5_b, 0))
print(secant(t5_b, 6))
print(bisection(t5_b, 0, 6))

# the point (0,0) cannot be used for secant method because it has no slope
# the bisection method is substantially more effective at garunteeing a solution in the range

#c) y = (x ** 3 - 2 * x ** 2 + 5 * x - 25) / 40
def t5_c(x): #task 5a
    return (x ** 3 - 2 * x ** 2 + 5 * x - 25) / 40


print("Task 5: function C")
print(secant(t5_c, 0))
print(secant(t5_c, 6))
print(bisection(t5_c, 0, 6))

#this function is very clean and has no oscillation or difficult features. This is a good function to take advatage of the secant method's speed


#Task 6
# false - the newton-raphson method, although known for speed and computational efficiency, is not garunteed to converge. between oscillating loops and the chance of finding a root outside the range, the newton-raphson method is not garunteed to converge
# plus, the newton-raphson method requires a derivative, so even if it is continuous, it may not be differentiable and would not allow the method to function