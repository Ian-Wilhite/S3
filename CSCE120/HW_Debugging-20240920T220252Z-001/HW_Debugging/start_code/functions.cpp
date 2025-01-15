#include <stdexcept>
#include <climits>

bool SumIsEven(int a, int b) {
  return ((a + b) % 2 == 0);
}

int Largest(int a, int b, int c) {
  if (a >= b && a >= c){
    return a;
  }
  if (b >= c && b >= a){
    return b;
  }
  return c;

}

unsigned int BoxesNeeded(int apples) {
  if (apples <= 0){
    return 0;
  } 
  int boxes = 1 + (apples - 1) / 20;
  return boxes;
}

bool SmarterSection(int A_correct, int A_total, int B_correct, int B_total) {
  if (A_correct > A_total || B_correct > B_total){
    throw std::invalid_argument("correct answers must be less than total");
  }
  if (A_correct & 0x80000000 || A_total & 0x80000000 || B_correct & 0x80000000 || B_total & 0x80000000){
    throw std::invalid_argument("must be positive");
  }
  return (A_correct * B_total > B_correct * A_total);
}

bool GoodDinner(int pizzas, bool is_weekend) {
  return !(pizzas < 10 || (pizzas > 20 && !is_weekend));
}
/*
long long SumBetween(long long low, long long high) {
  if (low > high){
    throw std::invalid_argument("low must be less than high");
  }
  if (low == high){
    return low;
  }
  if (low == -high){
    return 0;
  }
  if (low == LLONG_MIN || high == LLONG_MAX){
    return low;
    //throw std::overflow_error("abs(low && high) must be less than abs(llong_max)");
  }
  if (low < 0 && high > 0){
    value = (high - low + 1) * (low / 2 + high / 2);
    return value;
  }
  long long value = 0;
  
  for (long long i = low; i <= high; i++){
    if (i > 0) {
      if (value > LLONG_MAX - i){
        throw std::overflow_error("sum overflow");
      }
    } else {
      if (value < LLONG_MIN - i){
        throw std::overflow_error("sum overflow");
      }
    }

    value += i;
  }
  
  //value = (high - low + 1) * (low / 2 + high / 2);
  return value;
}
*/

/*
long long SumBetween(long long low, long long high) {
  if (low > high) {
    throw std::invalid_argument("low must be less than high");
  }
  if (low == LLONG_MIN && high == LLONG_MAX) {
    return -1;  // The sum from LLONG_MIN to LLONG_MAX is -1
  } 

  if ((low == -LLONG_MAX + 1 && high == LLONG_MAX) || (-low == high)) {
    return 0;
  }

  //long long sum = 0;

  
  long long n = high - low + 1;
  if (LLONG_MAX / n < ((low + high) / 2)){
    throw std::overflow_error("sum overflow");
  }
  long long sum = n * (low + high) / 2;
  
  return sum;
}
*/
long long SumBetween(long long low, long long high) {
    if (low > high) {
        throw std::invalid_argument("low must be less than or equal to high");
    }

    // Special case: Sum between LLONG_MIN and LLONG_MAX should return LLONG_MIN
    if (low == LLONG_MIN && high == LLONG_MAX) {
        return LLONG_MIN;
    }

    // Check for overflow when calculating sum with large ranges
    long long n = high - low + 1;
    long long sum = (n * (low + high)) / 2;

    // Check if overflow occurred
    if (low < 0 && high > 0 && sum < 0) {
        throw std::overflow_error("sum overflow");
    }
    if (low > 0 && sum < 0) {
        throw std::overflow_error("sum overflow");
    }

    return sum;
}




/*
long long Product(long long a, long long b) {

  if (a == 0 || b == 0){
    return 0;
  }
  if (a / b < 0){
    if (a < 0){
      a *= -1;
    } else {
      b *= -1;
    }
    if (LLONG_MAX / a < b || a >= 4643172349 || b >= 4643172349){
      throw std::overflow_error("result overflow");
    }
    return - a * b; 
  }
  if (a < 0){
    a *= -1; b *= -1;
  }
  if (LLONG_MAX / a < b || a >= 4643172349 || b >= 4643172349){
    throw std::overflow_error("result overflow");
  }
  return a * b;
}
*/
/*
long long Product(long long a, long long b) {
    if (a == 0 || b == 0) {
        return 0;
    }

    // Handle cases where multiplication with LLONG_MIN should not overflow
    if (a == 1) {
        return b;
    }
    if (b == 1) {
        return a;
    }

    // Handle overflow when multiplying by -1 and LLONG_MIN
    if (a == LLONG_MIN && b == -1) {
        throw std::overflow_error("result overflow");
    }
    if (b == LLONG_MIN && a == -1) {
        throw std::overflow_error("result overflow");
    }

    // Check for overflow based on division
    if (a > 0 && b > 0 && a > LLONG_MAX / b) {
        throw std::overflow_error("result overflow");
    }
    if (a < 0 && b < 0 && -a > LLONG_MAX / -b) {
        throw std::overflow_error("result overflow");
    }
    if (a > 0 && b < 0 && a > LLONG_MAX / -b) {
        throw std::overflow_error("result overflow");
    }
}   
*/
long long Product(long long a, long long b) {
    if (a == 0 || b == 0) {
        return 0;
    }

    // Handle special cases like multiplying by 1
    if (a == 1) {
        return b;
    }
    if (b == 1) {
        return a;
    }

    // Handle overflow when multiplying by LLONG_MIN
    if ((a == LLONG_MIN && b == -1) || (b == LLONG_MIN && a == -1)) {
        throw std::overflow_error("result overflow");
    }

    // Check for overflow before performing the multiplication
    if ((a > 0 && b > 0 && a > LLONG_MAX / b) ||
        (a < 0 && b < 0 && -a > LLONG_MAX / -b) ||
        (a > 0 && b < 0 && a > LLONG_MAX / -b) ||
        (a < 0 && b > 0 && -a > LLONG_MAX / b)) {
        throw std::overflow_error("result overflow");
    }

    return a * b;
}
