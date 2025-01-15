import numpy as np
import matplotlib.pyplot as plt

r_outer = 2
r_inner = r_outer / 2  
n = 10  
dr = (r_outer - r_inner) / (n - 1)  

# radii
r = np.linspace(r_inner, r_outer, n)

A = np.zeros((n, n))
b = np.zeros(n)

A[0, 0] = 1
A[-1, -1] = 1
b[-1] = 200 

# iterate diagonally
for i in range(1, n - 1):
    A[i, i - 1] = (1 - dr / (2 * r[i])) / dr**2
    A[i, i] = -2 / dr**2
    A[i, i + 1] = (1 + dr / (2 * r[i])) / dr**2


plt.plot(r, np.linalg.solve(A, b), 'bo-', label="Numerical Solution")
plt.plot(r, 200 * (1 - np.log(r / r_outer) / np.log(0.5)), 'r-', label="True Solution")
plt.xlabel("Radius (r)")
plt.ylabel("Temperature (T)")
plt.title("Temperature Profile in the Cylinder")
plt.legend()
plt.show()

