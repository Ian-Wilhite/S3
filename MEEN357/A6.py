import numpy as np
import numpy.linalg as la
import matplotlib.pyplot as plt

def QuadraticSpline(x, fx):
    
    #calculate the number of segments & constants
    nsegs = len(x)-1
    nknts = len(x)
    
    # create empty arr A and vec B of len 3 * the number of segments
    # vec B must have 3 constants to define each quadratic section, and
    # Arr A must have the same dimension as B to create a valid system to solve
    
    A = np.zeros((nsegs*3, nsegs*3))
    b = np.zeros((nsegs*3, 1))
    
    # fill in system for quadratic spline segments
    for i in range(1, nknts-1):
        #set up matrix ax^2 + bx + c
        A[2*i-2, 3*(i-1)] = x[i]**2
        A[2*i-2, 3*(i-1)+1] = x[i]
        A[2*i-2, 3*(i-1)+2] = 1
        A[2*i-1, 3*(i-1)+3] = x[i]**2
        A[2*i-1, 3*(i-1)+4] = x[i]
        A[2*i-1, 3*(i-1)+5] = 1
        
        b[2*i-2] = fx[i]
        b[2*i-1] = fx[i]
        
    #boundary condition for first
    A[2*nsegs-2, 0] = x[0]**2
    A[2*nsegs-2, 1] = x[0]
    A[2*nsegs-2, 2] = 1
    b[2*nsegs-2] = fx[0]
    
    #boundary conditions for last
    A[2*nsegs-2+1, -3] = x[-1]**2
    A[2*nsegs-2+1, -2] = x[-1]
    A[2*nsegs-2+1, -1] = 1
    b[2*nsegs-2+1] = fx[-1]
    
    #iterate through constants
    for i in range(1, nknts-1):
        A[(2*nsegs-2)+2 + (i-1), 3*(i-1)] = 2*x[i]
        A[(2*nsegs-2)+2 + (i-1), 3*(i-1)+1] = 1
        A[(2*nsegs-2)+2 + (i-1), 3*(i-1)+3] = -2*x[i]
        A[(2*nsegs-2)+2 + (i-1), 3*(i-1)+4] = -1
        b[(2*nsegs-2)+2 + (i-1)] = 0
  
    #set the inital conditions for the slope at the beginning and end
    A[(2*nsegs-2)+ 2 + nsegs-1, 0] = 1
    b[(2*nsegs-2) + 2 + nsegs-1] = 0
        
        
    # use np linalg to solve the matrix
    coeffs = la.solve(A, b)
    
    return coeffs #return

def QuadraticSplineInterp(x, xnew, coeffs):
    """
    Evaluates the quadratic spline at new points xnew using given coefficients.

    Parameters:
    x : numpy array
        Original knot locations.
    xnew : numpy array
        Locations where the spline is to be evaluated.
    coeffs : numpy array
        Coefficients of the quadratic splines.

    Returns:
    fapprox : numpy array
        Interpolated values at xnew.
    """
    nsegs = len(x) - 1
    fapprox = np.zeros_like(xnew)

    # Loop through each segment and apply the corresponding coefficients
    for i in range(nsegs):
        idx = np.where((xnew >= x[i]) & (xnew <= x[i + 1]))[0]  # Select indices where xnew is between x[i] and x[i+1]
        if len(idx) > 0:
            a, b, c = coeffs[3 * i:3 * (i + 1)].flatten()  # Extract coefficients for the segment
            fapprox[idx] = a * xnew[idx]**2 + b * xnew[idx] + c  # Apply the quadratic formula to these xnew values

    return fapprox

def BackSubstitutionSolver(U, b):
    # Check if U is square
    if U.shape[0] != U.shape[1]:
        raise ValueError("Matrix U must be square. Current shape: {}".format(U.shape))

    # Ensure b is a column vector
    if b.ndim != 2 or b.shape[1] != 1:
        raise ValueError("b must be a column vector. Current shape: {}".format(b.shape))
        
    # Ensure U and b have the same number of rows
    if U.shape[0] != b.shape[0]:
        raise ValueError("Dimensions of U and b are incompatible. U has {} rows, but b has {} rows.".format(U.shape[0], b.shape[0]))

    n = U.shape[0]
    x = np.zeros((n, 1), dtype=np.float64)

    # Perform back substitution
    for i in range(n - 1, -1, -1):
        x[i] = (b[i] - np.dot(U[i, i + 1:], x[i + 1:].flatten())) / U[i, i]

    return x.flatten()  # Return as 1D array for compatibility

def CramerRule(A, b):
    # Check if A is a square matrix
    if A.shape[0] != A.shape[1]:
        raise ValueError(f"Matrix A must be square. Current shape: {A.shape}")

    # Ensure b is a column vector
    if b.ndim != 2 or b.shape[1] != 1:
        raise ValueError(f"b must be a column vector. Current shape: {b.shape}")

    det_A = la.det(A)
    if np.isclose(det_A, 0):
        raise ValueError(f"Matrix A is singular (det(A) = 0).")

    n = A.shape[0]
    x = np.zeros(n)

    # Solve using Cramer's Rule
    for i in range(n):
        A_temp = A.copy()
        A_temp[:, i] = b.flatten()  # Replace the i-th column of A with b
        x[i] = la.det(A_temp) / det_A  # Compute the determinant of the modified matrix and divide by det(A)

    return x

def LinRegress(xd, yd, n):
    # Ensure the lengths of xd and yd match
    if len(xd) != len(yd):
        raise ValueError("xd and yd must have the same length. xd length: {}, yd length: {}".format(len(xd), len(yd)))
    if len(xd) < n + 1:
        raise ValueError("Not enough data points to fit a polynomial of degree n.")

    xd = np.array(xd)
    yd = np.array(yd)

    A = np.vander(xd, N=n + 1, increasing=True)
    coeffs = la.solve(A.T @ A, A.T @ yd)

    return coeffs

def compute_r2(xd, yd, coeffs):
    """
    Computes the R^2 value for the given fit.

    Parameters:
    xd : numpy array
        Independent variable data points.
    yd : numpy array
        Dependent variable data points.
    coeffs : numpy array
        Coefficients of the polynomial fit.

    Returns:
    r2 : float
        R^2 value.
    """
    yd_pred = np.polyval(coeffs[::-1], xd)
    ss_tot = np.sum((yd - np.mean(yd))**2)
    ss_res = np.sum((yd - yd_pred)**2)
    return 1 - (ss_res / ss_tot)


# # --- task1
# print(f' - - - - - task1 - - - - -')

# x = np.array([3.0, 4.5, 7.0, 9.0])
# fx = np.array([2.5, 1.0, 2.5, 0.5])
# xnew = np.linspace(3.0, 9.0, 100)

# coeffs = QuadraticSpline(x, fx)
# fapprox = QuadraticSplineInterp(x, xnew, coeffs)

# plt.plot(x, fx, 'r*', label="Data Points")
# plt.plot(xnew, fapprox, 'b-', label="Quadratic Spline")
# plt.xlabel("x")
# plt.ylabel("f(x)")
# plt.legend()
# plt.title("Quadratic Spline Interpolation")
# plt.show()



# # --- task2
# print(f' - - - - - task2 - - - - -')

# # Given data
# xd = [0., 1., 2., 3., 4., 5., 6., 7., 8., 9.]
# yd = [38.824, 31.382, 106.615, 84.958, 136.192, 221.649, 
#       239.815, 326.167, 433.752, 527.402]

# # Fit a 6th order polynomial
# coeffs_6th = LinRegress(xd, yd, 6)

# # Fit a cubic polynomial
# coeffs_cubic = LinRegress(xd, yd, 3)

# # Fit a linear polynomial
# coeffs_linear = LinRegress(xd, yd, 1)

# # Print coefficients
# print(f'6th order polynomial coefficients: {coeffs_6th}')
# print(f'Cubic polynomial coefficients: {coeffs_cubic}')
# print(f'Linear polynomial coefficients: {coeffs_linear}')



# # --- task3
# print(f' - - - - - task3 - - - - -')

# # Define the matrix and vector
# A = np.array([[2, -1, 0],
#               [-1, 2, -1],
#               [0, -1, 2]], dtype=np.float64)
# b = np.array([1, 0, 1], dtype=np.float64)

# # Solve using Cramer's Rule
# x_cramer = CramerRule(A, b)

# # Solve using numpy's built-in solver
# x_np = la.solve(A, b)

# # Print results
# print("Solution using CramerRule:", x_cramer)
# print("Solution using np.linalg.solve:", x_np)



# # --- task4
# print(f' - - - - - task4 - - - - -')

# # Create a fine grid for plotting
# x_plot = np.linspace(min(xd), max(xd), 100)

# # Evaluate polynomials on the grid
# y_6th = np.polyval(coeffs_6th[::-1], x_plot)
# y_cubic = np.polyval(coeffs_cubic[::-1], x_plot)
# y_linear = np.polyval(coeffs_linear[::-1], x_plot)

# # Plot the results
# plt.figure(figsize=(10, 6))
# plt.scatter(xd, yd, color='red', label="Data Points")
# plt.plot(x_plot, y_6th, label="6th Order Fit")
# plt.plot(x_plot, y_cubic, label="Cubic Fit")
# plt.plot(x_plot, y_linear, label="Linear Fit")
# plt.xlabel("x")
# plt.ylabel("y")
# plt.title("Linear Regression Fits")
# plt.legend()
# plt.show()

