#ifndef MYSTRING_H
#define MYSTRING_H

#include <iostream>

class MyString {
private:
    char* str;
    size_t len;

public:
    // Default constructor
    MyString() : str(nullptr), len(0) {}

    // Parameterized constructor for const char* type
    MyString(const char* s) {
        // Calculate the length of the C-style string s
        len = 0;
        while (s[len] != '\0') {
            len++;
        }

        // Allocate memory for the string and copy characters from s
        str = new char[len + 1];
        for (size_t i = 0; i < len; i++) {
            str[i] = s[i];
        }
        str[len] = '\0';  // Null-terminate the new string
    }


    // Copy constructor
    MyString(const MyString& other) {
        len = other.len;
        str = new char[len + 1];
        
        for (size_t i = 0; i < len; i++) {
            str[i] = other.str[i];
        }
        str[len] = '\0';  // Null-terminate the new string
        //std::strcpy(str, other.str);
    }

    // Destructor
    ~MyString() {
        delete[] str;
    }

    // Size function
    size_t size() const {
        return len;
    }
    size_t length() const {
        return len;
    }

    // // at() function
    // char at(size_t index) const {
    //     return (index < len) ? str[index] : '\0';
    // }

    // // front() function
    // char front() const {
    //     return (len > 0) ? str[0] : '\0';
    // }

    // // empty() function
    // bool empty() const {
    //     return len == 0;
    // }

    // clear() function
    void clear() {
        delete[] str;
        str = nullptr;
        len = 0;
    }

    // data() function to get a const char* for ifstream
    const char* data() const {
        return str;
    }


    // Copy assignment operator
    MyString& operator=(const MyString& other) {
        if (this == &other) return *this; // self-assignment check
        delete[] str;
        len = other.len;
        str = new char[len + 1];
        // std::strcpy(str, other.str);

        str = new char[len + 1];
        for (size_t i = 0; i < len; i++) {
            str[i] = other.str[i];
        }
        str[len] = '\0';  // Null-terminate the new string


        return *this;
    }

    // find() function
    int find(const MyString& substring, size_t start = 0) const {
        // Check if starting index is out of bounds or substring is too long
        if (start >= len || substring.len > len - start) return -1;

        // Loop through each character in str starting from the specified index
        for (size_t i = start; i <= len - substring.len; i++) {
            size_t j = 0;

            // Check if substring matches str starting from position i
            while (j < substring.len && str[i + j] == substring.str[j]) {
                j++;
            }

            // If we've matched the entire substring, return the starting index
            if (j == substring.len) {
                return i;
            }
        }

        return -1; // Return -1 if the substring is not found
    }



    // Output stream operator<<
    friend std::ostream& operator<<(std::ostream& os, const MyString& myStr) {
        os << myStr.str;
        return os;
    }
};

#endif
