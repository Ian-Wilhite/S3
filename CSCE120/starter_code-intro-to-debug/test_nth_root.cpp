#include <iostream>
#include <cmath>
#include "./nth_root.h"  // Assuming nth_root is defined in a separate header

// Function declaration (you might have this in nth_root.h)
double nth_root(double x, double n);

// Main test code
int main() {
    try {
        // Call the function with various values of n and x
        std::cout << "nth_root(0, 0) = " << nth_root(0, 0) << std::endl;  // Might raise an error
        std::cout << "nth_root(2, 0.5) = " << nth_root(2, 0.5) << std::endl;
        std::cout << "nth_root(2, -1) = " << nth_root(2, -1) << std::endl;
        std::cout << "nth_root(-5, 2) = " << nth_root(-5, 2) << std::endl;  // Should raise an error
        std::cout << "nth_root(-7, 1) = " << nth_root(-7, 1) << std::endl;
        std::cout << "nth_root(1, -1) = " << nth_root(1, -1) << std::endl;
        std::cout << "nth_root(2, 1) = " << nth_root(2, 0) << std::endl;
        std::cout << "nth_root(-1, -1) = " << nth_root(-1, -1) << std::endl;
        std::cout << "nth_root(10, -1) = " << nth_root(10, -1) << std::endl;
        std::cout << "nth_root(10, 10) = " << nth_root(10, 10) << std::endl;
        std::cout << "nth_root(1, 0) = " << nth_root(1, 0) << std::endl;
        std::cout << "nth_root(-3, -3) = " << nth_root(-3, -3) << std::endl;
        std::cout << "nth_root(3, 3) = " << nth_root(3, 3) << std::endl;
        std::cout << "nth_root(1, -2) = " << nth_root(1, -2) << std::endl;
        std::cout << "nth_root(-3, 3) = " << nth_root(-3, 3) << std::endl;
        std::cout << "nth_root(3, -3) = " << nth_root(3, -3) << std::endl;
        std::cout << "nth_root(-1, 0) = " << nth_root(-1, 0) << std::endl;


        // Try more tests inside loops
        for (int i = 1; i <= 5; ++i) {
            for (double j = 0.5; j <= 3.0; j += 0.5) {
                std::cout << "nth_root(" << i << ", " << j << ") = " << nth_root(i, j) << std::endl;
            }
        }

    } catch (const std::exception &e) {
        std::cerr << "Error: " << e.what() << std::endl;
    }

    // TRY HARDER: Compare actual value to expected value
    {
        double actual = nth_root(2, 1);
        double expected = 2.0;
        if (std::fabs(actual - expected) > 0.00005) {
            std::cout << "[FAIL] (n=2, x=1)" << std::endl;
            std::cout << "  expected nth_root(2, 1) to be " << expected << std::endl;
            std::cout << "  got " << actual << std::endl;
        } else {
            std::cout << "[PASS] (n=2, x=1)" << std::endl;
        }
    }

    {
        double actual = nth_root(2, 4);
        double expected = 2.0;  // square root of 4 is 2
        if (std::fabs(actual - expected) > 0.00005) {
            std::cout << "[FAIL] (n=2, x=4)" << std::endl;
            std::cout << "  expected nth_root(2, 4) to be " << expected << std::endl;
            std::cout << "  got " << actual << std::endl;
        } else {
            std::cout << "[PASS] (n=2, x=4)" << std::endl;
        }
    }

    return 0;
}
