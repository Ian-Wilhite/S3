/******************************************************************************

File: main.cpp
Author: Prof. Lupoli & Andrew Nemec
Date: 2/16/2021
Section: 
E-mail: slupoli@tamu.edu
Description:
This file contains C++  code that will simulate data collected from a track 
event with 9 lanes. The code will sort the order, then display the results

Updates
Author: J. Michael Moore & Paul Taele
Author: J. Michael Moore

Input information format
<Time (double)> <Abbreviated Country (String)> <Uniform number (int)> <Lastname (String)>
32.7 USA 12 Moore
36.5 RUS 35 Polsley
45.8 ENG 73 Teale
52.34 CHN 14 Nemec
76.45 ITY 23 Lupoli     

*******************************************************************************/

#include <iostream>
#include <cstring>
#include "rank_functions.h"

using std::cin; using std::cout; using std::endl;

const int MAX_DRIVERS = 10;
const int MAX_NAME_LENGTH = 51; // Adjusted to accommodate longer names


int main()
{
    // TODO: create arrays needed
    double times[MAX_DRIVERS] = {}; 
    char cunt[MAX_DRIVERS][MAX_NAME_LENGTH] = {}; 
    unsigned int num[MAX_DRIVERS] = {}; 
    char names[MAX_DRIVERS][MAX_NAME_LENGTH] = {};

    // TODO: prep all arrays (using your prep functions)
	prep_double_array(times);
    prep_string_array(cunt);
    prep_unsigned_int_array(num);
    prep_string_array(names);
    get_driver_data(times, cunt, num, names);

    // TODO: Determine ranking, populate the rank array
    unsigned int rankary[MAX_DRIVERS];
    prep_unsigned_int_array(rankary);
    set_rankings(times, rankary);

    // TODO: Output results
    print_results(times, cunt, names, rankary);

    return 0;
}