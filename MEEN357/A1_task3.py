from A1 import *
import matplotlib.pyplot as plt
# ----------------------------------------------------------------------
#  - - - - TASK 3 - - - - 

tv = 6.737947 * 10 ** -3 #the true value for all comparisons

# 3-1-a
def e_chapra(x, n):
    #find the value of e^x using chapra's method at x using a taylor approximation to n terms
    val = 0
    for i in range(n):
        val += (-1) ** (i) * x ** i / factorial(i)
        
    return val

def e_canale(x, n):
    #find the value of e^x using canale's method at x using a taylor approximation to n terms
    val = 1
    for i in range(n):
        val += x ** (i+1) / factorial(i+1)
        
    return 1/val

#3-1-b

e_chapra_list = []
e_canale_list = []

e_chapra_error = []
e_canale_error = []

for i in range(20):
    chapra = float(e_chapra(5,i))
    canale = float(e_canale(5,i))
    
    e_chapra_list += [chapra]
    e_canale_list += [canale]
    
    e_chapra_error += [tv - chapra]
    e_canale_error += [tv - canale]

e_cha_pererr = [] #percent error
e_can_pererr = []

for i in range(len(e_chapra_list)):
    e_cha_pererr += [abs(e_chapra_error[i] / tv) * 100]

for i in range(len(e_canale_list)):
    e_can_pererr += [abs(e_canale_error[i] / tv ) * 100]

lists = [e_chapra_list,
    e_canale_list,
    e_chapra_error,
    e_canale_error,
    e_can_pererr,
    e_cha_pererr]

"""for list in lists:
    for num in list:
        print(f'{num:.4}', end=' ')
    print('')#nextline char"""

#3-1-c
fig, axs = plt.subplots(1, 3)

# Step 3: Plot data on each subplot
axs[0].plot(range(len(e_chapra_list)), e_chapra_list, 'b')  
axs[0].plot(range(len(e_canale_list)), e_canale_list, 'g')  
axs[0].set_xlabel('i')
axs[0].set_ylabel('approximations / num terms')

axs[1].plot(range(len(e_chapra_error)), e_chapra_error, 'b')  
axs[1].plot(range(len(e_canale_error)), e_canale_error, 'g')  
axs[1].set_xlabel('i')
axs[1].set_ylabel('error / num terms')

axs[2].plot(range(len(e_cha_pererr)), e_cha_pererr, 'b')  
axs[2].plot(range(len(e_can_pererr)), e_can_pererr, 'g')  
axs[2].set_xlabel('x')
axs[2].set_ylabel('percent error / num terms')

fig.tight_layout()
plt.show()


for i in range (17, 21):
    print()