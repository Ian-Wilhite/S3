from random import *
import numpy as np
from math import *
from decimal import Decimal

def sort_ascending(unsorted_list):
    if len(unsorted_list) > 1:
        
        middle_index = len(unsorted_list) // 2
        
        left_half = sort_ascending(unsorted_list[:middle_index])
        right_half = sort_ascending(unsorted_list[middle_index:])
        
        
        # Merging the sorted halves
        i = j = 0
        
        arr = []
        while i < len(left_half) and j < len(right_half):
            if left_half[i] < right_half[j]:
                arr += [left_half[i]]
                i += 1
            else:
                arr += [right_half[j]]
                j += 1
            
        
        # Checking if any element was left
        while i < len(left_half):
            arr += [left_half[i]]
            i += 1
        
        while j < len(right_half):
            arr += [right_half[j]]
            j += 1
            
        unsorted_list = arr
        
    return unsorted_list


def A1_task1(N):
    arr = []
    for i in range(N):
        arr += [int(random() * 100 // 1 + 1)] #generates random number 1-100 

    return sort_ascending(arr)

sorted_list = A1_task1(10)
print (sorted_list)

# ----------------------------------------------------------------------
#  - - - - TASK 2 - - - - 

def A1_task2():

    A = np.array([
        [1, 2, 3, 4],
        [2, 4, 6, 8],
        [3, 6, 9, 12],
        [4, 8, 12, 16]
    ])

    C = np.flip(np.flip(A, 0), 1) #C is A flipped along a diagnal, or being flipped both horizontally and vertically

    #print(A)
    #print(C)

    b = [[-4, 3, -2, 1]]
    d = [[-1, 2, -3, 4]]
    print(b)
    b = np.transpose(b)
    d = np.transpose(d)

    #print(b)


    print('task 2-2 ')
    x = np.matmul((A + np.transpose(A)), b) - np.matmul(C, d)

    print('task 2-3')
    A_new = A[:,[0,1,3,2]]
    

    print('task 2-4')
    C_new = C[[2,1,0,3],:]
    

    print("A_new", A_new)
    print("C_new", C_new)

   # print('task 2-5')
    x_new = np.matmul((A_new + np.transpose(A_new)), b) - np.matmul(C_new, d)
    print(x_new)


    #print('task 2-6')
    M = A + np.transpose(A_new)
    print("M", M)
    M_max = M.max()
    print(M_max)
    M_min = M.min()
    print(M_min)
    
    return x, x_new, M_max, M_min

A1_task2()
