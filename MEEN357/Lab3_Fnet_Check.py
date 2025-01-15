#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 20 08:39:38 2022

@author: dallaire
"""

from subfunctions import *
from Lab3_DefineRover import *
import numpy as np

rover, planet = define_rover_1()
omega = np.array([0.00, 0.50, 1.00, 2.00, 3.00, 3.80])
terrain_angle = np.array([-5.0, 0.0, 5.0, 10.0, 20.0, 30.0]) # degrees!
Crr = 0.1
Fnet = F_net(omega, terrain_angle, rover, planet, Crr)
print('terrain_angle   Omega   F_net')
for i in range(len(Fnet)):
    print('{:3.4F}        {:3.4F}  {:3.4F}'.format(terrain_angle[i], omega[i], 
                                                   Fnet[i]))
    
    