#include <iostream>
#include <fstream>
#include <string>
#include "logic.h"

using std::cout, std::endl, std::ifstream, std::string;

/**
 * TODO: Student implement this function
 * Load representation of the dungeon level from file into the 2D map.
 * Calls createMap to allocate the 2D array.
 * @param   fileName    File name of dungeon level.
 * @param   maxRow      Number of rows in the dungeon table (aka height).
 * @param   maxCol      Number of columns in the dungeon table (aka width).
 * @param   player      Player object by reference to set starting position.
 * @return  pointer to 2D dynamic array representation of dungeon map with player's location., or nullptr if loading fails for any reason
 * @updates  maxRow, maxCol, player
 */
char** loadLevel(const string& fileName, int& maxRow, int& maxCol, Player& player) {
    
    ifstream level(fileName);
    

    if (!level.is_open()){
        return nullptr;
    }

    if (level.eof()){
                return nullptr;
            }

    //reading the first line
    level >> maxRow;
    if (level.eof()){
                return nullptr;
            }
    level >> maxCol;
    if (level.eof()){
                return nullptr;
            }

    //checking if the map is in size
    if (maxRow < 1 || maxRow > 999999 || maxCol < 1 || maxCol > 999999){
        //cout << "MAX SIZE ERROR";
        return nullptr;
    }

    // reading the second line
    level >> player.row;
    if (level.eof()){
                return nullptr;
            }
    level >> player.col;
    if (level.eof()){
                return nullptr;
            }

    //checking if the player starts inside the map
    if (player.row > maxRow-1 || player.row < 0 || player.col > maxCol-1 || player.col < 0){
        return nullptr;
    }

    

    char** map = createMap(maxRow, maxCol);

    char valid[8] = {'-','o','@','$','+','M','!','?'};

    int doorcount = 0;
    
    for (int row = 0 ; row < maxRow; ++row){
        for (int col = 0; col < maxCol; ++col){

            if (level.eof()){
                deleteMap(map, maxRow);
                return nullptr;
            }
            
            else{

                level >> map[row][col];
                bool good = false;

                for (int i = 0; i < 8; ++i){
                    if (map[row][col] == valid[i]){
                        good = true;
                        if (map[row][col] == '?' || map[row][col] == '!'){
                            ++doorcount;
                        }
                        break;
                    }
                }

                if (!good){
                    deleteMap(map, maxRow);
                    return nullptr;
                }
            }
        }
    }

    char temp;
    level >> temp;

    if (!level.eof()){
        deleteMap(map, maxRow);
        return nullptr;
    }  

    if (doorcount == 0){
        deleteMap(map, maxRow);
        return nullptr;
    }

    if (map[player.row][player.col] != '-'){
        deleteMap(map, maxRow);
        return nullptr;
    }

    map[player.row][player.col] = 'o';

    return map;
}

/**
 * TODO: Student implement this function
 * Translate the character direction input by the user into row or column change.
 * That is, updates the nextRow or nextCol according to the player's movement direction.
 * @param   input       Character input by the user which translates to a direction.
 * @param   nextRow     Player's next row on the dungeon map (up/down).
 * @param   nextCol     Player's next column on dungeon map (left/right).
 * @updates  nextRow, nextCol
 */
void getDirection(char input, int& nextRow, int& nextCol) {
    if (input == 'W' || input == 'w'){
        nextRow -= 1;
        //nextCol = 0;
    }
    else if (input == 'A' || input == 'a'){
        //nextRow = 0;
        nextCol -= 1;
    }
    else if (input == 'S' || input == 's'){
        nextRow += 1;
        //nextCol = 0;
    }
    else if (input == 'D' || input == 'd'){
        //nextRow = 0;
        nextCol += 1;
    }
}

/**
 * TODO: [suggested] Student implement this function
 * Allocate the 2D map array.
 * Initialize each cell to TILE_OPEN.
 * @param   maxRow      Number of rows in the dungeon table (aka height).
 * @param   maxCol      Number of columns in the dungeon table (aka width).
 * @return  2D map array for the dungeon level, holds char type.
 */
char** createMap(int maxRow, int maxCol) {

    char* * map = new char*[maxRow];
    for (int i = 0; i < maxRow; ++i){
        map[i] = new char[maxCol];
    }

    for (int i = 0; i < maxRow; ++i){
        for (int j = 0; j < maxCol; ++j){
            map[i][j] = TILE_OPEN;
        }
    }

    return map;
}

/**
 * TODO: Student implement this function
 * Deallocates the 2D map array.
 * @param   map         Dungeon map.
 * @param   maxRow      Number of rows in the dungeon table (aka height).
 * @return None
 * @update map, maxRow
 */
void deleteMap(char**& map, int& maxRow) {

    if (map == nullptr){
        // delete map;
        maxRow = 0;
        
    }

    else {
        for (int i = 0; i < maxRow; ++i){
        delete[] map[i];
        }
        delete[] map;
        maxRow = 0;
        map = nullptr;
    }
    
    //cout << map;
}

/**
 * TODO: Student implement this function
 * Resize the 2D map by doubling both dimensions.
 * Copy the current map contents to the right, diagonal down, and below.
 * Do not duplicate the player, and remember to avoid memory leaks!
 * You can use the STATUS constants defined in logic.h to help!
 * @param   map         Dungeon map.
 * @param   maxRow      Number of rows in the dungeon table (aka height), to be doubled.
 * @param   maxCol      Number of columns in the dungeon table (aka width), to be doubled.
 * @return  pointer to a dynamically-allocated 2D array (map) that has twice as many columns and rows in size.
 * @update maxRow, maxCol
 */
char** resizeMap(char** map, int& maxRow, int& maxCol) {
    
    int tempRow = maxRow;

    if (map == nullptr || maxRow > 999999 || maxCol > 999999 || maxRow < 1 || maxCol < 1){
        //cout << "failed";
        return nullptr;
    }

    for (int i = 0; i < maxRow; ++i){
        if (map[i] == nullptr){
            return nullptr;
        }
    }


    //making the temp array
    char** temp = createMap(maxRow, maxCol);
    // cout << "made array" << endl;



    for (int i = 0; i < maxRow; ++i){
        for (int j = 0; j < maxCol; ++j){
            temp[i][j] = map[i][j];
        }
    }

    // for (int i = 0; i < maxRow; ++i){
    //     for (int j = 0; j < maxCol; ++j){
    //         cout << temp[i][j];
    //     }
    //     cout <<endl;
    // }

    // cout << "transfered" <<endl;


    deleteMap(map,maxRow);

    maxRow = tempRow;

    //cout << "deleted original" <<endl;

    char** newmap = createMap(maxRow*2, maxCol*2);

    // cout <<"created new array" << endl;
    /*
    A   B

    C   D
    */



    //array A
    for (int i = 0; i < maxRow; ++i){
        for (int j = 0; j < maxCol; ++j){
            newmap[i][j] = temp[i][j];
        }
    }

    // cout << "A done"<<endl;

    //array B
    for (int i = 0; i < maxRow; ++i){
        for (int j = maxCol; j < maxCol*2; ++j){
            if (temp[i][j-maxCol] == 'o'){
                newmap[i][j] = '-';
            }
            else{
                newmap[i][j] = temp[i][j-maxCol];
            }
            
        }
    }

    // cout << "B done"<<endl;

    //array C
    for (int i = maxRow; i < maxRow*2; ++i){
        for (int j = 0; j < (maxCol); ++j){
            if (temp[i-maxRow][j] == 'o'){
                newmap[i][j] = '-';
            }
            else{
                newmap[i][j] = temp[i-maxRow][j];
            }
            
        }
    }

    // cout << "C done"<<endl;

    //array D
    for (int i = maxRow; i < (maxRow*2); ++i){
        for (int j = maxCol; j < (maxCol*2); ++j){
            if (temp[i-maxRow][j-maxCol] == 'o'){
                newmap[i][j] = '-';
            }
            else{
                newmap[i][j] = temp[i-maxRow][j-maxCol];
            }
            
        }
    }

    // cout << "D done"<<endl;

    //cout << "appended modified arrays" << endl;

    deleteMap(temp, maxRow);

    maxRow = tempRow;

    // cout << "deleted temp array" <<endl;

    maxRow = maxRow*2;
    maxCol = maxCol*2;

    // for (int i = 0; i < maxRow; ++i){
    //     for (int j = 0; j < maxCol; ++j){
    //         cout << newmap[i][j];
    //     }
    //     cout <<endl;
    // }

    return newmap;
}

/**
 * TODO: Student implement this function
 * Checks if the player can move in the specified direction and performs the move if so.
 * Cannot move out of bounds or onto TILE_PILLAR or TILE_MONSTER.
 * Cannot move onto TILE_EXIT without at least one treasure. 
 * If TILE_TREASURE, increment treasure by 1.
 * Remember to update the map tile that the player moves onto and return the appropriate status.
 * You can use the STATUS constants defined in logic.h to help!
 * @param   map         Dungeon map.
 * @param   maxRow      Number of rows in the dungeon table (aka height).
 * @param   maxCol      Number of columns in the dungeon table (aka width).
 * @param   player      Player object to by reference to see current location.
 * @param   nextRow     Player's next row on the dungeon map (up/down).
 * @param   nextCol     Player's next column on dungeon map (left/right).
 * @return  Player's movement status after updating player's position.
 * @update map contents, player
 */
int doPlayerMove(char** map, int maxRow, int maxCol, Player& player, int nextRow, int nextCol) {
    if (nextRow > maxRow-1 || nextRow < 0 || nextCol > maxCol-1 || nextCol < 0){
        nextRow = player.row;
        nextCol = player.col;
        return STATUS_STAY;
    }
    else{
        //pillar logic
        if (map[nextRow][nextCol] == TILE_PILLAR || map[nextRow][nextCol] == TILE_MONSTER){
            nextRow = player.row;
            nextCol = player.col;
            return STATUS_STAY;
        }

        //treasure logic
        if (map[nextRow][nextCol] == TILE_TREASURE){
            ++player.treasure;
            map[player.row][player.col] = TILE_OPEN;
            player.col = nextCol;
            player.row = nextRow;
            map[player.row][player.col] = TILE_PLAYER;
            return STATUS_TREASURE;
        }

        //exit logic
        if (map[nextRow][nextCol] == TILE_EXIT){
            if (player.treasure <= 0){
                nextRow = player.row;
                nextCol = player.col;
                map[player.row][player.col] = TILE_PLAYER;
                return STATUS_STAY;
            }
            else{
                map[player.row][player.col] = TILE_OPEN;
                player.col = nextCol;
                player.row = nextRow;

                map[player.row][player.col] = TILE_PLAYER;
                return STATUS_ESCAPE;
            }
            
        }

        //amulet logic
        if (map[nextRow][nextCol] == TILE_AMULET){
            map[player.row][player.col] = TILE_OPEN;
            player.col = nextCol;
            player.row = nextRow;
            map[player.row][player.col] = TILE_PLAYER;
            return STATUS_AMULET;
        }

        //door logic
        if (map[nextRow][nextCol] == TILE_DOOR){
            map[player.row][player.col] = TILE_OPEN;
            player.col = nextCol;
            player.row = nextRow;
            map[player.row][player.col] = TILE_PLAYER;
            return STATUS_LEAVE;
        } 

        //open logic
        if (map[nextRow][nextCol] == TILE_OPEN){
            map[player.row][player.col] = TILE_OPEN;
            player.col = nextCol;
            player.row = nextRow;
            map[player.row][player.col] = TILE_PLAYER;
            return STATUS_MOVE;
        } 
    }
    return 0;
}

/**
 * TODO: Student implement this function
 * Update monster locations:
 * We check up, down, left, right from the current player position.
 * If we see an obstacle, there is no line of sight in that direction, and the monster does not move.
 * If we see a monster before an obstacle, the monster moves one tile toward the player.
 * We should update the map as the monster moves.
 * At the end, we check if a monster has moved onto the player's tile.
 * @param   map         Dungeon map.
 * @param   maxRow      Number of rows in the dungeon table (aka height).
 * @param   maxCol      Number of columns in the dungeon table (aka width).
 * @param   player      Player object by reference for current location.
 * @return  Boolean value indicating player status: true if monster reaches the player, false if not.
 * @update map contents
 */
bool doMonsterAttack(char** map, int maxRow, int maxCol, const Player& player) {


    //checking right
    for (int i = player.col+1; i < maxCol; ++i){
        if (map[player.row][i] == TILE_MONSTER){
            map[player.row][i] = TILE_OPEN;
            map[player.row][i - 1] = TILE_MONSTER;
            //break;
            
        }
        if ( map[player.row][i] == TILE_PILLAR){
            break;
        }
    }

    //checking left
    for (int i = player.col-1; i >= 0; --i){
        if (map[player.row][i] == TILE_MONSTER){
                if (map[player.row][i + 1] != TILE_MONSTER){
                    map[player.row][i + 1] = TILE_MONSTER;
                    map[player.row][i] = TILE_OPEN;
                }
                else{
                    break;
                }
                
                //break;
        }
        if ( map[player.row][i] == TILE_PILLAR){
            break;
        }
    }

    //checking up
    for (int i = player.row-1; i >= 0; --i){
        if (map[i][player.col] == TILE_MONSTER){
                if (map[i + 1][player.col] != TILE_MONSTER){
                    map[i + 1][player.col] = TILE_MONSTER;
                    map[i][player.col] = TILE_OPEN;
                }
                else{
                    break;
                }
                
                //break;
        }
        if ( map[i][player.col] == TILE_PILLAR){
            break;
        }
    }

    // checking down
    for (int i = player.row+1; i < maxRow; ++i){
        if (map[i][player.col] == TILE_MONSTER){
            if (map[i - 1][player.col] != TILE_MONSTER){
                map[i - 1][player.col] = TILE_MONSTER;
                map[i][player.col] = TILE_OPEN;
            }
            else{
                break;
            }
            
            //break;
        }
        if ( map[i][player.col] == TILE_PILLAR){
            break;
        }
    }

    if (map[player.row][player.col] == TILE_MONSTER){
        return true;
    }


    return false;
}
