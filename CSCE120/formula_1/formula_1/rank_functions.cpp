#include <iostream>
#include <iomanip>
#include <cstring>
#include "rank_functions.h"

using std::cin; using std::cout; using std::endl;

void prep_double_array(double ary[]){
    for (unsigned int i = 0; i < SIZE; ++i) {
        ary[i] = 0.0;
    }
}

void prep_unsigned_int_array(unsigned int ary[]) {
    for (unsigned int i = 0; i < SIZE; ++i) {
        ary[i] = 0;
    }
}

void prep_string_array(char ary[][STRING_SIZE]) {
    for (unsigned int i = 0; i < STRING_SIZE; ++i) {
        strcpy(ary[i], "N/A");
    }
}

//-------------------------------------------------------
// Name: trim
// PreCondition:  the cstring
// PostCondition: whitespace has been removed from beginning and end of string
//---------------------------------------------------------
void trim(char str[STRING_SIZE]) {
    // 1. Trim leading whitespace
    int start = 0;
    while (str[start] == ' ' || str[start] == '\t') {
        start++;
    }

    // 2. Trim trailing whitespace
    int end = strlen(str) - 1;
    while (end >= start && (str[end] == ' ' || str[end] == '\t')) {
        end--;
    }

    // 3. Shift the characters to the front
    int length = end - start + 1;
    for (int i = 0; i <= length; ++i) {
        str[i] = str[start + i];
    }

    // 4. Null-terminate the trimmed string
    str[length] = '\0';
}

bool get_driver_data(double timeArray[], char countryArray[][STRING_SIZE], 
                     unsigned int numberArray[], char lastnameArray[][STRING_SIZE]) {

    int i = 0;
    double time;
    char country[STRING_SIZE], lastname[STRING_SIZE], numberStr[STRING_SIZE];

    // Read data until we reach the end of input or arrays are full
    while (i < 9) {  // Assuming 9 entries based on your example
        // Read time
        if (!(std::cin >> time) || time <= 0) {  // Check for invalid time
            return false;
        }
        timeArray[i] = time;

        // Read country
        std::cin >> country;
        trim(country);  // Trim whitespace before validation
        if (strlen(country) != 3) return false;  // Must be exactly 3 characters
        for (int j = 0; j < 3; j++) {
            if (country[j] < 'A' || country[j] > 'Z') {
                return false;  // Only uppercase alphabetic characters
            }
        }
        strcpy(countryArray[i], country);

        // Read driver number as string, then validate
        std::cin >> numberStr;
        trim(numberStr);  // Trim whitespace before validation
        int len = strlen(numberStr);
        if (len < 1 || len > 2) return false;  // Must be 1 or 2 digits
        for (int j = 0; j < len; j++) {
            if (numberStr[j] < '0' || numberStr[j] > '9') {
                return false;  // Only digits are allowed
            }
        }
        numberArray[i] = static_cast<unsigned int>(std::stoi(numberStr));

        // Read last name
        std::cin >> lastname;
        trim(lastname);  // Trim whitespace before validation
        if (strlen(lastname) < 2) return false;  // Must be longer than 1 character
        for (long unsigned int j = 0; j < strlen(lastname); j++) {
            if (!( (lastname[j] >= 'A' && lastname[j] <= 'Z') || 
                   (lastname[j] >= 'a' && lastname[j] <= 'z') || 
                   lastname[j] == ' ')) {
                return false;  // Only alphabetic characters and spaces
            }
        }
        strcpy(lastnameArray[i], lastname);

        // Increment index for next driver
        i++;
    }

    return true;
}

void set_rankings(const double timeArray[], unsigned int rankArray[]) {
    // Create an array of indices to track the original positions of the times
    unsigned int indices[9];
    for (unsigned int i = 0; i < 9; ++i) {
        indices[i] = i;
    }

    // Bubble sort based on timeArray, sorting the indices in increasing order of times
    for (unsigned int i = 0; i < 9; ++i) {
        for (unsigned int j = i + 1; j < 9; ++j) {
            if (timeArray[indices[i]] > timeArray[indices[j]]) {
                // Swap indices
                unsigned int temp = indices[i];
                indices[i] = indices[j];
                indices[j] = temp;
            }
        }
    }

    // Assign ranks based on sorted indices
    for (unsigned int i = 0; i < 9; ++i) {
        rankArray[indices[i]] = i + 1;
    }
}

void print_results(const double timeArray[], const char countryArray[][STRING_SIZE],
                   const char lastnameArray[][STRING_SIZE], const unsigned int rankArray[]) {

    // Step 1: Create local copies of the input data
    double* localTimeArray = new double[SIZE];
    char (*localCountryArray)[STRING_SIZE] = new char[SIZE][STRING_SIZE];
    char (*localLastnameArray)[STRING_SIZE] = new char[SIZE][STRING_SIZE];
    unsigned int* localRankArray = new unsigned int[SIZE];

    // Copy data into local arrays
    for (unsigned int i = 0; i < SIZE; i++) {
        localTimeArray[i] = timeArray[i];
        std::strcpy(localCountryArray[i], countryArray[i]);
        std::strcpy(localLastnameArray[i], lastnameArray[i]);
        localRankArray[i] = rankArray[i];
    }

    // Step 2: Sort local arrays based on localTimeArray using Bubble Sort
    for (unsigned int i = 0; i < SIZE - 1; i++) {
        for (unsigned int j = 0; j < SIZE - i - 1; j++) {
            if (localTimeArray[j] > localTimeArray[j + 1]) {
                // Swap localTimeArray
                double tempTime = localTimeArray[j];
                localTimeArray[j] = localTimeArray[j + 1];
                localTimeArray[j + 1] = tempTime;

                // Swap localCountryArray
                char tempCountry[STRING_SIZE];
                std::strcpy(tempCountry, localCountryArray[j]);
                std::strcpy(localCountryArray[j], localCountryArray[j + 1]);
                std::strcpy(localCountryArray[j + 1], tempCountry);

                // Swap localLastnameArray
                char tempLastname[STRING_SIZE];
                std::strcpy(tempLastname, localLastnameArray[j]);
                std::strcpy(localLastnameArray[j], localLastnameArray[j + 1]);
                std::strcpy(localLastnameArray[j + 1], tempLastname);

                // Swap localRankArray
                unsigned int tempRank = localRankArray[j];
                localRankArray[j] = localRankArray[j + 1];
                localRankArray[j + 1] = tempRank;
            }
        }
    }

    // Step 3: Print results
    std::cout << "Final results!!" << std::endl;

    // Fastest time is the first element after sorting
    double fastestTime = localTimeArray[0];

    for (unsigned int i = 0; i < SIZE; i++) {
        double timeDiff = localTimeArray[i] - fastestTime;

        // Format rank and time correctly to avoid leading spaces
        std::cout << "[" << localRankArray[i] << "] "
                  << std::fixed << std::setprecision(2)
                  << std::setw(6) << std::right << localTimeArray[i] << " "
                  << std::left << std::setw(15) << localLastnameArray[i]
                  << "\t(" << localCountryArray[i] << ")  "
                  << "+" << std::fixed << std::setprecision(2) << timeDiff
                  << std::endl;
    }

    // Step 4: Delete dynamically allocated memory
    delete[] localTimeArray;
    delete[] localCountryArray;
    delete[] localLastnameArray;
    delete[] localRankArray;
}
