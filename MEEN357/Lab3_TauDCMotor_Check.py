"""
Test your "tau_dcmotor" function
"""


from subfunctions import *
from Lab3_DefineRover import *
import numpy as np

rover, planet = define_rover_1()
omega = np.array([0.00, 0.50, 1.00, 2.00, 3.00, 3.80])
tau = tau_dcmotor(omega, rover['wheel_assembly']['motor'])
print('Omega     Tau')
for i in range(len(tau)):
    print('{:3.4F}    {:3.4F}'.format(omega[i], tau[i]))
    
   
    
   
    
   
    
   

# try this too
tau_dcmotor(np.array([[0, 0], [1, 2]]), rover['wheel_assembly']['motor'])