# Ian Wilhite 9/22/2024
# Meen 357 solo

import numpy as np
import matplotlib.pyplot as plt


#task 1: Strategy for Coding a Numerical Integration Routine
""" 
- area of a rectangle is length times width
- riemmien sum over a curve = sum( f(x) * dx)
"""

def simpint(x, fx):
    if(type(x) != np.ndarray or type(fx) != np.ndarray):
        raise Exception("x and fx must be np arrays")
    if(x.size != fx.size):
        raise Exception("np arrays must be same len")
    if(not (x.size == 3 or x.size == 4)):
        raise Exception("np arrays must have len 3 or 4")
    
    # simpsons 3/8th rule
    if(x.size == 3):
        sum = fx[0] + 4 * fx[1] + fx[2]
        return ((x[2] - x[0]) / 6 ) * sum
        
    else: # len == 4
        sum = fx[0] + 3 * fx[1] + 3 * fx[2] + fx[3]
        return ((x[3] - x[0]) / 8 ) * sum
    
def fx(x):
    return (x ** 2) * (np.e ** x)


#print(simpint(np.arange(0,4,1), np.array([fx(x) for x in np.arange(0,4,1)])))

xrange = np.arange(0, 4, 1)
yrange = np.array([fx(i) for i in xrange])

#print(type(xrange))
#print(type(yrange))

#print(simpint(xrange, yrange)) # 104.09750661796272

#1.5, 1, 0.75, 0.5, 0.375, 0.330, 0.3, 0.25}
hs = [3/x for x in range(2,15)] # possible vals of h (hs)
print(hs)
def findnumcom(m_1, m_2, N): #find linear combination of two variables
    """given a total sum and two components, finds the combination of two components that adds up to N

    Args:
        m_1 (int): multiple 1
        m_2 (int): multiple 2
        N (int): total that multiples should sum to
    Returns tuple (x, y) where x * m_1 + y * m_2 = N
    """
    x = 0
    while (x * m_1 <= N):
        remaining = N - x * m_1
        if (remaining % m_2 == 0): 
            y = int(remaining / m_2)
            return (x, y)
        
        x += 1
    return (-1, -1)


custom_combs = {}

for h in hs:
    numcom = findnumcom(3, 4, 3 / h)
    if(numcom[0] != -1):
        #print(f'{(h / 1.0):.3}: {numcom},')
        custom_combs[float(f'{(h / 1.0):.3}')] = numcom
        

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

given_combs = {
    #1.5: (-1, -1),
    1.0: (1, 0),
    0.75: (0, 1),
    0.5: (2, 0),
    0.38: (0, 2),
    0.33: (3, 0),
    0.3: (2, 1),
    0.25: (0, 3)
}

actual_value = 98.4276846159 #actual value of integral 0 to 3

given_areas = {
    1.5: 0.0,
    1.0: 0.0,
    0.75: 0.0,
    0.5: 0.0,
    0.38: 0.0,
    0.33: 0.0,
    0.3: 0.0,
    0.25: 0.0
}

given_areas[1.5] = (fx(3) - fx(0)) / 2 * 3

for comb in given_combs:
    xrange = np.arange(0, 3 + comb, comb)
    print(comb, xrange)
    yrange = [fx(x) for x in xrange]
    
    #integrate a num of points defined by comb
    area = 0 #area starts at 0 
    pt_index = 0 #starting at index = 0
    for i in range(given_combs[comb][0]):
        xsubrange = np.array(xrange[pt_index: pt_index + 4])
        ysubrange = np.array([fx(x) for x in xsubrange])
        print((xsubrange, ysubrange))
        area += simpint(xsubrange, ysubrange)
        print(area)
        pt_index += 3
    
    for i in range(given_combs[comb][1]):
        xsubrange = np.array(xrange[pt_index: pt_index + 4])
        ysubrange = np.array(yrange[pt_index: pt_index + 4])
        area += simpint(xsubrange, ysubrange)
        pt_index += 4
    
    given_areas[comb] = area
"""
custom_areas = {}

for comb in custom_combs:
    xrange = np.arange(0, 3 + comb, comb)
    yrange = [fx(x) for x in xrange]
    
    #integrate a num of points defined by comb
    area = 0 #area starts at 0 
    pt_index = 0 #starting at index = 0
    for i in range(custom_combs[comb][0]):
        xsubrange = np.array(xrange[pt_index: pt_index + 3])
        ysubrange = np.array(yrange[pt_index: pt_index + 3])
        area += simpint(xsubrange, ysubrange)
        pt_index += 3
    
    for i in range(custom_combs[comb][1]):
        xsubrange = np.array(xrange[pt_index: pt_index + 4])
        ysubrange = np.array(yrange[pt_index: pt_index + 4])
        area += simpint(xsubrange, ysubrange)
        pt_index += 4
    custom_areas[comb] = area

"""
print("given")
print(f'width; area; error')
for area in given_areas:
    print(f'{area}; {given_areas[area]:.3}; {((actual_value - given_areas[area]) / actual_value * 100):.3}')
"""
print("custom")
print(f'width; area; error')
for area in custom_areas:
    print(f'{area}; {custom_areas[area]:.3}; {((actual_value - custom_areas[area]) / actual_value * 100):.3}')
"""



plt.plot([area for area in given_areas], [given_areas[area] for area in given_areas])
plt.ylabel("area found")
plt.xlabel("interval width")
plt.plot([area for area in given_areas], [abs(actual_value - given_areas[area]) / actual_value * 100 for area in given_areas])
plt.show() 