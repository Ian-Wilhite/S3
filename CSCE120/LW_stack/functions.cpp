#include "functions.h"
#include <iostream>  // Make sure to include the necessary headers
//#include <cstdlib>   // For exit and NULL
using std::cin, std::cout, std::endl, std::ostream, std::string;

#define INFO(X)  cout << "[INFO] ("<<__FUNCTION__<<":"<<__LINE__<<") " << #X << " = " << X << endl;
#define INFO_STRUCT(X) cout << "[INFO] ("<<__FUNCTION__<<":"<<__LINE__<<") " << #X << " count = " << X.count << endl;

/**
 * ----- REQUIRED -----
 * Pushes number to top of stack. If stack is full, then resize stack's array.
 * @param   stack   Target stack.
 * @param   number  Number to push to stack.
 */
void push(Stack& stack, int number) {
    // Check if resizing is needed
    if (stack.count == stack.capacity) {
        // Resize the stack array
        stack.capacity *= 2; // Double the capacity

        // Allocate new memory
        int* newNumbers = new int[stack.capacity]; // Use new instead of realloc

        // Copy old numbers to new array
        for (int i = 0; i < stack.count; ++i) {
            newNumbers[i] = stack.numbers[i];
        }

        // Free old memory
        delete[] stack.numbers;

        // Assign new array to stack
        stack.numbers = newNumbers;
    }
    // Add the new element and increment the count
    stack.numbers[stack.count++] = number;

    // INFO_STRUCT(stack);
    // INFO(number);
}

/**
 * ----- REQUIRED -----
 * Pops number from top of stack. If stack is empty, return INT32_MAX.
 * @param   stack   Target stack.
 * @return          Value of popped number.
 */
int pop(Stack& stack) {
    // Return INT32_MAX if stack is empty
    if (stack.count == 0) {
        return INT32_MAX;
    }
    return stack.numbers[--stack.count];
    // INFO_STRUCT(stack);
}

/**
 * ----- REQUIRED -----
 * Returns the number at top of stack without popping it. If stack is empty, return INT32_MAX.
 * @param   stack   Target stack.
 * @return          Number at top of stack.
 */
int peek(const Stack& stack) {
    // Return INT32_MAX if stack is empty
    if (stack.count == 0) {
        return INT32_MAX;
    }
    return stack.numbers[stack.count - 1];
    // INFO_STRUCT(stack);
}
