import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate

effcy_tau = np.array([0,10,20,40,70,165])
effcy = np.array([0,0.60,0.75,0.73,0.50,0.05])

plt.plot(effcy_tau, effcy,  'k*', label='data points') #plots given data points
effcy_fun = interpolate.interp1d(effcy_tau, effcy, kind = 'cubic') #interpolation function to calculate efficiency

x = np.linspace(min(effcy_tau),max(effcy_tau),100) #creates 100 evenly spaced points between the min and max torque of data points
y = []
for i in range (len(x)): #evaluates the efficiency at all 100 points
    y.append(effcy_fun(i))

plt.plot(x,y, label='evaluated data') #plots 100 evaluated points as a line
plt.xlabel('motor torque [Nm]')
plt.ylabel('efficiency')
plt.legend(loc="upper right")
plt.show()

