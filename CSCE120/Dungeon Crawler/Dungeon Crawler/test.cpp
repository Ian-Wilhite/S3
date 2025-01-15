#include <iostream>
#include <fstream>
#include <string>
#include "helper.h"
#include "logic.h"
using std::cin, std::cout, std::endl, std::string, std::ifstream;

int row;
int col;

Player tom;


int main(){
    string filename;
    cin >> filename;
    char** map = loadLevel(filename,row, col, tom);

    //cout << row << endl;
    //cout << col << endl;

    for (int i = 0; i < row; ++i){
        for (int j = 0; j < col; ++j){
            cout << map[i][j];
        }
        cout << endl;
    }

    resizeMap(map,row,col);
    // for (int i = 0; i < row; ++i){
    //     for (int j = 0; j < col; ++j){
    //         cout << map[i][j];
    //     }
    //     cout << endl;
    // }
    //deleteMap(map, row);
    //cout << map;
    
    cout << row << endl;
    cout << col << endl;
}