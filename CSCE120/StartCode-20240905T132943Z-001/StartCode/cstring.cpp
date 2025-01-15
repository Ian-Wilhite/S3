#include <iostream>
#include "cstring.h"

unsigned int length(char str[]) {
  // returns the length of the string including zero (0)
  unsigned i=0, len=0;

  while (str[i]){
    i++, len++;
  }

  return len;
}

unsigned int find(char str[], char character) {
  // returns 
  //  - the index of the first occurence of character in str
  //  - the size if the character is not found

  unsigned i=0, len=0;

  while (str[i]){
    if (str[i] == character){
      return i;
    }
    i++, len++;
    
  }

  return len;
}

bool equalStr(char str1[], char str2[]) {
  // returns true if they are equal and false if they are not
  
  unsigned int len1 = length(str1);
  unsigned int len2 = length(str2);
  

  if (len1 != len2){
    return false;
  }
  
  unsigned int i = 0;

  while (i < len1){
    if (str1[i] != str2[i]){
      return false;
    }
    i++;
  }
 
  
  return true;
}