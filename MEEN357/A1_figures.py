from math import *
from scipy.integrate import *
import matplotlib.pyplot as plt
import numpy as np

#   TASK 2


"""
The graph should contain five curves, defined by 𝑦 = erf (𝛼𝑥) for 0 ≤ 𝑥 ≤ 5 for 𝛼 =
0.05, 0.25, 0.5, 1, 1.5. That is, you should have one curve for each value of 𝛼.
o erf is a built-in function in the math and special Python packages.
• Your axes should be labeled “x” and “erf(𝛼x)”.
o Note: Use the 𝛼 symbol. Do not write out “alpha”.
• Use 100 samples of 𝑥 to ensure curves look smooth.
• Use different colors/styles for each curve according to the table below. This is to be
implemented directly in your code (i.e., no editing the graph manually)
"""

a_list = [0.05, 0.25, 0.5, 1, 1.5]

x = np.arange(0, 5 , 5 / 100)
#print(x)


y_a1 = []
for i in x:
    y_a1 += [erf(i * a_list[0])]
plt.plot(x, y_a1, 'b')

y_a2 = []
for i in x:
    y_a2 += [erf(i * a_list[1])]
plt.plot(x, y_a2, 'k--')

y_a3 = []
for i in x:
    y_a3 += [erf(i * a_list[2])]
plt.plot(x, y_a3, 'c:')

y_a4 = []
for i in x:
    y_a4 += [erf(i * a_list[3])]
plt.plot(x, y_a4, 'm-.')

y_a5 = []
for i in x:
    y_a5 += [erf(i * a_list[4])]
plt.plot(x, y_a5, 'g')


plt.xlabel("x")
plt.ylabel("erf(" + r'$\alpha$' + "x)")


lgd = [str(i) for i in a_list]
plt.legend(lgd, title = r'$\alpha$')
           
#plt.show()



#   TASK 2

fig = plt.figure()
ax1 = fig.add_subplot(211)
ax2 = fig.add_subplot(212)



x1 = np.arange(-5, 5 , 10 / 20)
y_1 = []
for i in x1:
    y_1 += [0.5 * i * i]
ax1.plot(x1, y_1)
ax1.set_title('Exhibit 1')
ax1.set_xlabel('x')
ax1.set_ylabel('y')



x2 = np.arange(0, 100 , 100 / 20)
y_2 = []
for i in x2:
    y_2 += [-i]
ax2.plot(x2, y_2)
ax2.set_title('Exhibit 2')
ax2.set_xlabel('work')
ax2.set_ylabel('play')

plt.tight_layout()
plt.show()



