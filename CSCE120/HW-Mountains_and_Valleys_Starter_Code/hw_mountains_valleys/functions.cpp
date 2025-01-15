#include "functions.h"
# include <iostream>
using std::cout, std::endl, std::cin;

// Function to validate the range [a, b]
bool is_valid_range(int a, int b) {
    return (a >= 10 && b < 10000 && a <= b);
}

char classify_mv_range_type(int number) {
    if (number < 10) return 'N'; // Single-digit numbers are neither mountain nor valley

    if (number < 100){
        if (number / 10 < number % 10) {
           return 'M'; // Mountain pattern starts
        } else if (number / 10 > number % 10) {
            return 'V'; // Valley pattern starts
        } else {
            return 'N'; 
        }
    }

    // Extract the last two digits
    int last_digit = number % 10;
    number /= 10;
    int middle_digit = number % 10;

    // Loop through the remaining digits
    while (number >= 10) {
        number /= 10;
        int first_digit = number % 10; // Extract the next digit

        // Check if this triplet forms a mountain or valley
        if (!(first_digit < middle_digit && middle_digit > last_digit) && // Not a mountain
            !(first_digit > middle_digit && middle_digit < last_digit)) { // Not a valley
            return 'N'; // Break in the pattern
        }

        // Slide the window: Update digits for the next iteration
        last_digit = middle_digit;
        middle_digit = first_digit;
    }

    // Determine the pattern based on the first triplet
    if (middle_digit < last_digit) {
        return 'M'; // Mountain pattern starts
    } else {
        return 'V'; // Valley pattern starts
    }
}




// Function to count and display the number of mountain and valley numbers in a range
void count_valid_mv_numbers(int a, int b) {
    int mountain_count = 0;
    int valley_count = 0;

    for (int i = a; i <= b; ++i) {
        char type = classify_mv_range_type(i);
        if (type == 'M') {
            ++mountain_count;
        } else if (type == 'V') {
            ++valley_count;
        }
    }

    // Output in the required format
    std::cout << "There are " << mountain_count << " mountain ranges and "
              << valley_count << " valley ranges between " << a << " and " << b << "." << std::endl;
}

