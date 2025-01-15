#include <iostream>
#include <string>
#include <sstream>
#include "functions.h"  // Assume this contains your stack functions

using std::cin, std::cout, std::endl, std::string, std::istringstream;

int power(int base, int exp) {
    int result = 1;  // Initialize result to 1

    // Handle negative exponents
    if (exp < 0) {
        return 0;  // Typically you can return an error or handle as needed
    }

    for (int i = 0; i < exp; ++i) {
        result *= base;  // Multiply result by base
    }

    return result;  // Return the final result
}

int main() {
    // Prompt user input
    cout << "Type RPN expression (end with '=')." << endl;
    cout << "> ";

    Stack rpnStack;  // Create the stack

    string rpn_input;
    getline(cin, rpn_input);  // Read the entire line of input

    istringstream iss(rpn_input);  // Create a string stream to parse the input
    string token;

    while (iss >> token) {  // Read tokens separated by whitespace
        if (token == "=") {
            break;  // End processing on '='
        } else if (token == "+") {
            int right = pop(rpnStack);
            int left = pop(rpnStack);
            push(rpnStack, left + right);  // Push the result of addition
        } else if (token == "-") {
            int right = pop(rpnStack);
            int left = pop(rpnStack);
            push(rpnStack, left - right);  // Push the result of subtraction
        } else if (token == "*") {
            int right = pop(rpnStack);
            int left = pop(rpnStack);
            push(rpnStack, left * right);  // Push the result of multiplication
        } else if (token == "/") {
            int right = pop(rpnStack);
            int left = pop(rpnStack);
            if (right != 0) {
                push(rpnStack, left / right);  // Push the result of division
            } else {
                cout << "Error: Division by zero!" << endl;  // Handle division by zero
                return 1;  // Exit with an error code
            }
        } else if (token == "^") {
            int right = pop(rpnStack);
            int left = pop(rpnStack);
            push(rpnStack, power(left, right));  // Push the result of exponenitation
        } else {  // Assume the token is a number
            int num = std::stoi(token);  // Convert string token to integer
            push(rpnStack, num);  // Push the number onto the stack
        }
    }

    // Output the final answer
    if (rpnStack.count > 0) {
        cout << "Ans: " << peek(rpnStack) << endl;  // Print the result
    } else {
        cout << "> No result." << endl;  // Handle case where stack is empty
    }

    // Cleanup
    delete[] rpnStack.numbers;  // Free allocated memory for the stack

    return 0;
}

