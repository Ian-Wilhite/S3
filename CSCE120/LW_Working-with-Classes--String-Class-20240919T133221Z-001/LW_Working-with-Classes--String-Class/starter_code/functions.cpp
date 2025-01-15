# include "functions.h"
// add any includes

using std::cout, std::cin, std::endl, std::string;

void deobfuscate() {
    /*
    Prompt the user to enter a collection of sentence words (i.e., words in the sentence), with the spaces removed (i.e., the obfuscated sentence) and with words that are less than ten (10) letters each.
    Prompt the user to enter a sequence of numbers that represent the length of each corresponding sentence word (i.e. the deobfuscated details).
    Output the deobfuscated sentence.

    Ex:
    Please enter obfuscated sentence: Thisisasentence
    Please enter deobfuscation details: 4218
    Deobfuscated sentence: This is a sentence

    */
    std::string user_word, new_word, word_lens;
    std::cout << "Please enter obfuscated sentence: ";
    std::cin >> user_word;
    std::cout << "Please enter deobfuscation details: ";
    std::cin >> word_lens;

    unsigned int chars_passed = 0;
    for(char curr_len : word_lens){
        // Convert character to integer
        int len = curr_len - '0'; // Convert char to int

        // Extract substd::string of length `len` starting from `current_index`
        std::string word = user_word.substr(chars_passed, len);
        new_word += word + " ";
        
        // Update the index to the next starting position
        chars_passed += len;
    }
    std::cout << "Deobfuscated sentence: " << new_word << std::endl;
}



void wordFilter() {
    // TODO
}

void passwordConverter() {
    /*
    Please enter your text input: password
    input: password
    output: p@ssw0rddr0wss@p
    
    Replace:
    With:
    'a'
    '@'
    'e'
    '3'
    'i'
    '!'
    'o'
    '0'
    'u'
    '^'

    */
    // TODO
    std::string user_password;
    std::cout << "Please enter your text input: ";
    std::cin >> user_password;
    std::cout << "input: " << user_password << std::endl;

    // pass to correct chars
    unsigned int pass_len = user_password.length();
    for(unsigned int i = 0; i < pass_len; i++){
        if (user_password.at(i) == 'a'){
            user_password[i] = '@';
        } else if (user_password.at(i) == 'e'){
            user_password[i] = '3';
        } else if (user_password.at(i) == 'i'){
            user_password[i] = '!';
        } else if (user_password.at(i) == 'o'){
            user_password[i] = '0';
        } else if (user_password.at(i) == 'u'){
            user_password[i] = '^';
        }
    }

    // pass to make palindrome
    for (int i = pass_len - 1; i >= 0; i--) {
        user_password += user_password.at(i);
    }

    std::cout << "output: " << user_password << std::endl;
}

void wordCalculator() {
   
}

void palindromeCounter() {
    
}