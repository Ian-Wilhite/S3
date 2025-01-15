"""import numpy as np
import matplotlib.pyplot as plt

# Define the system of equations
def ode_system(x, Y):
    y, z = Y  # Unpack the vector Y = [y, z]
    dy_dx = z
    dz_dx = -0.5 * z - 7 * y
    return np.array([dy_dx, dz_dx])

# Implement the RK4 method for systems
def RK4_system(ode_system, x0, Y0, xStop, h):
    X = np.arange(x0, xStop + h, h)
    Y = np.zeros((len(X), len(Y0)))
    Y[0, :] = Y0
    
    for i in range(1, len(X)):
        x = X[i-1]
        Y_i = Y[i-1, :]
        
        k1 = h * ode_system(x, Y_i)
        k2 = h * ode_system(x + h/2, Y_i + k1/2)
        k3 = h * ode_system(x + h/2, Y_i + k2/2)
        k4 = h * ode_system(x + h, Y_i + k3)
        
        Y[i, :] = Y_i + (k1 + 2*k2 + 2*k3 + k4) / 6
        
    return X, Y

# Initial conditions and parameters
x0 = 0
y0 = 4  # Initial condition for y(0)
z0 = 0  # Initial condition for y'(0)
xStop = 5
h = 0.5
Y0 = np.array([y0, z0])

# Solve the system using RK4
X, Y = RK4_system(ode_system, x0, Y0, xStop, h)

# Extract solutions for y and z
Y_solution = Y[:, 0]
Z_solution = Y[:, 1]

# Plot the results
plt.figure(figsize=(10, 6))

# Plot y(x)
plt.subplot(2, 1, 1)
plt.plot(X, Y_solution, label='y(x)', color='b')
plt.xlabel('x')
plt.ylabel('y(x)')
plt.title('Solution of y(x) and y\'(x) using RK4')
plt.grid(True)
plt.legend()

# Plot z(x) = y'(x)
plt.subplot(2, 1, 2)
plt.plot(X, Z_solution, label="y'(x)", color='r')
plt.xlabel('x')
plt.ylabel("y'(x)")
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()

"""
import numpy as np
import matplotlib.pyplot as plt
from A4_task3 import actual  # Ensure this imports the correct analytical solution

# Define the ODE system function here (modify to match your specific ODEs)
def ode_system(x, Y):
    y, z = Y  # Unpack the vector Y = [y, z]
    dy_dx = z
    dz_dx = -0.5 * z - 7 * y  # Modify according to your ODE system
    return np.array([dy_dx, dz_dx])

# Implement the RK4 method for systems
def RK4_system(ode_system, x0, Y0, xStop, h):
    X = np.arange(x0, xStop + h, h)
    Y = np.zeros((len(X), len(Y0)))
    Y[0, :] = Y0
    
    for i in range(1, len(X)):
        x = X[i-1]
        Y_i = Y[i-1, :]
        
        k1 = h * ode_system(x, Y_i)
        k2 = h * ode_system(x + h/2, Y_i + k1/2)
        k3 = h * ode_system(x + h/2, Y_i + k2/2)
        k4 = h * ode_system(x + h, Y_i + k3)
        
        Y[i, :] = Y_i + (k1 + 2*k2 + 2*k3 + k4) / 6
        
    return X, Y

# Parameters for analysis
x_final = 2  # x-value at which you want to evaluate the solution
h_values = [0.5**p for p in range(0, 8)]  # Different step sizes
y0 = [4, 0]  # Initial conditions (modify to your specific initial conditions)

# Store errors
errors = []

# Run RK4 integration for each step size h
for h in h_values:
    t_values = np.arange(0, x_final + h, h)  # Time points for integration
    Y_rk4 = RK4_system(ode_system, 0, y0, x_final, h)[1]  # Get Y values from the RK4 method
    
    # Calculate the true solution using the 'actual' function
    Y_true = actual(x_final)  # Ensure this returns both state variables at x = 2
    
    # Compute the error as the percent relative error
    error = np.abs((Y_rk4[-1] - Y_true) / Y_true) * 100  # True percent relative error
    errors.append(error)

# Convert to numpy arrays for easier plotting
h_values = np.array(h_values)
errors = np.array(errors)

# Plot the results in a log-log scale
plt.loglog(h_values, errors[:, 0], label="State Variable 1")
plt.loglog(h_values, errors[:, 1], label="State Variable 2")
plt.xlabel("h (Step Size)")
plt.ylabel("True Percent Relative Error")
plt.title("Convergence Analysis")
plt.legend()
plt.grid(True, which="both", ls="--")
plt.show()
