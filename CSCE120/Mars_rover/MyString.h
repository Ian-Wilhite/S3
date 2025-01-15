#ifndef MYSTRING_H
#define MYSTRING_H

#include <iostream>

class MyString {
private:
    char* str;
    size_t len;

    // Helper function to calculate string length
    size_t stringLength(const char* s) const {
        size_t length = 0;
        while (s[length] != '\0') {
            length++;
        }
        return length;
    }

    // Helper function to copy a string
    void stringCopy(char* dest, const char* src) {
        size_t i = 0;
        while (src[i] != '\0') {
            dest[i] = src[i];
            i++;
        }
        dest[i] = '\0';
    }

public:
    // Default constructor
    MyString() : str(new char[1]{'\0'}), len(0) {}

    // Parameterized constructor for const char* type
    MyString(const char* s) {
        len = stringLength(s);
        str = new char[len + 1];
        stringCopy(str, s);
    }
    

    // Copy constructor
    MyString(const MyString& other) {
        len = other.len;
        str = new char[len + 1];
        stringCopy(str, other.str);
    }

    // Destructor
    ~MyString() {
        delete[] str;
    }

    // capacity() function
    size_t capacity() const {
        return len + 1; // Capacity includes space for the null terminator
    }


    // Size function
    size_t size() const {
        return len;
    }
    size_t length() const {
        return len;
    }

    // at() function
    char at(size_t index) const {
        if (len <= index){
            throw std::out_of_range("out of range bozo");
        }
        return (index < len) ? str[index] : '\0';
    }

    // front() function
    char front() const {
        return (len > 0) ? str[0] : '\0';
    }

    // empty() function
    bool empty() const {
        return len == 0;
    }

    // clear() function
    void clear() {
        delete[] str;
        str = nullptr;
        len = 0;
    }

    // data() function to get a const char* for ifstream
    const char* data() const {
        return str ? str : ""; // Ensure str is never nullptr
    }
    
    MyString operator+(const MyString& other) const {
        size_t newLen = len + other.len;
        char* newStr = new char[newLen + 1];

        for (size_t i = 0; i < len; i++) {
            newStr[i] = str[i];
        }
        for (size_t i = 0; i < other.len; i++) {
            newStr[len + i] = other.str[i];
        }
        newStr[newLen] = '\0';

        return MyString(newStr);
    }
    
    // Copy assignment operator
    MyString& operator=(const MyString& other) {
        if (this == &other) return *this; // self-assignment check
        delete[] str;
        len = other.len;
        str = new char[len + 1];
        stringCopy(str, other.str);
        return *this;
    }

    // Equality operator== to compare two MyString objects
    bool operator==(const MyString& other) const {
        // If lengths are different, they can't be equal
        if (len != other.len) return false;

        // Compare each character in the two strings
        for (size_t i = 0; i < len; i++) {
            if (str[i] != other.str[i]) {
                return false;
            }
        }
        return true; // All characters are equal
    }

    // operator+= for appending another MyString
    MyString& operator+=(const MyString& other) {
        // Calculate the new length and allocate memory for the concatenated string
        size_t newLen = len + other.len;
        char* newStr = new char[newLen + 1];

        // Copy the original string to the new string
        for (size_t i = 0; i < len; i++) {
            newStr[i] = str[i];
        }

        // Append the other string to the new string
        for (size_t i = 0; i < other.len; i++) {
            newStr[len + i] = other.str[i];
        }

        newStr[newLen] = '\0'; // Null-terminate the concatenated string

        // Delete the old string and update the object with the new one
        delete[] str;
        str = newStr;
        len = newLen;

        return *this;
    }

    int find(const MyString& substring, size_t start = 0) const {
        // Ensure the starting position is within bounds
        if (start >= len) return -1;

        // Ensure the substring is not longer than the remaining part of the string
        if (substring.len > len - start) return -1;

        for (size_t i = start; i <= len - substring.len; i++) {
            size_t j = 0;
            while (j < substring.len && str[i + j] == substring.str[j]) {
                j++;
            }
            if (j == substring.len) return i; // Found the substring
        }
        return -1; // Substring not found
    }

    // Output stream operator<<
    friend std::ostream& operator<<(std::ostream& os, const MyString& myStr) {
        os << (myStr.str ? myStr.str : "");
        return os;
    }
};

#endif
