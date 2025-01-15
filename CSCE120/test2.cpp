#include <stdexcept>

long long combineDigitPairs(long long number){
    if (number < 0){
        throw std::invalid_argument("number cannot be negative");
    }
    
    long long sum = 0;
    while (number >= 10){
        int hund = number % 100;
        sum += (hund / 10) * (hund % 10);
        number /= 10;
    }
}