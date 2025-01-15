#include <iostream>
#include "functions.h"

using std::cout, std::cin, std::endl;

int main() {
	// TODO(student): print prompt for input
	
	bool isvalid = false;
	int a, b;
	while(!isvalid){
		cout << "Enter numbers 10 <= a <= b < 10000: ";
		cin >> a >> b;
		
        if (is_valid_range(a, b)) {
            isvalid = true;  
        } else {
            cout << "Invalid Input" << endl;
        }
	}


	// TODO(student): compute and display solution
	
	//There are 0 mountain ranges and 0 valley ranges between 9998 and 9999
	count_valid_mv_numbers(a,b);

	return 0;
}