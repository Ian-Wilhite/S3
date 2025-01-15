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
    std::ifstream mapFile(fileName);
    if (!mapFile.is_open()) {
        return nullptr; // File couldn't be opened
    }

    mapFile >> maxRow >> maxCol >> player.row >> player.col;

    // Check for invalid dimensions or player position
    if (maxRow <= 0 || maxCol <= 0 || player.row < 0 || player.col < 0 ||
        player.row >= maxRow || player.col >= maxCol || maxRow * maxCol > INT32_MAX) {
        return nullptr; // Invalid input
    }

    // Dynamically allocate 2D array
    char** map = new char*[maxRow];
    for (int i = 0; i < maxRow; ++i) {
        map[i] = new char[maxCol];
    }

   // Read in the map from the file
    for (int i = 0; i < maxRow; ++i) {
        for (int j = 0; j < maxCol; ++j) {
            if (!(mapFile >> map[i][j])) {
                // Clean up allocated memory on failure
                deleteMap(map, maxRow);
                return nullptr; // Invalid map data
            }

            // If the tile is the player's starting position, mark it with TILE_PLAYER
            if (i == player.row && j == player.col) {
                map[i][j] = TILE_PLAYER;
            }
            // If the tile is a door, place TILE_DOOR
            else if (map[i][j] == 'D') { // Assuming 'D' represents doors in the map file
                map[i][j] = TILE_DOOR;
            }
        }
    }

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
    switch (input) {
        case MOVE_UP:
            nextRow -= 1;
            break;
        case MOVE_DOWN:
            nextRow += 1;
            break;
        case MOVE_LEFT:
            nextCol -= 1;
            break;
        case MOVE_RIGHT:
            nextCol += 1;
            break;
        default:
            // Invalid input: no movement
            break;
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
    // Validate input dimensions
    if (maxRow <= 0 || maxCol <= 0) {
        return nullptr; // Invalid dimensions
    }

    // Dynamically allocate 2D array
    char** map = new char*[maxRow];
    for (int i = 0; i < maxRow; ++i) {
        map[i] = new char[maxCol];
        for (int j = 0; j < maxCol; ++j) {
            map[i][j] = TILE_OPEN; // Initialize all tiles to TILE_OPEN
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
    if (map == nullptr) {
        maxRow = 0;
        return; // Map is already nullptr
    }

    // Deallocate each row
    for (int i = 0; i < maxRow; ++i) {
        delete[] map[i];
    }

    // Deallocate the array of row pointers
    delete[] map;

    // Set map to nullptr and maxRow to 0 to avoid dangling pointers
    map = nullptr;
    maxRow = 0;
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
    // Validate input
    if (map == nullptr || maxRow <= 0 || maxCol <= 0) {
        return nullptr; // Invalid map or dimensions
    }

    int newMaxRow = maxRow * 2;
    int newMaxCol = maxCol * 2;

    // Dynamically allocate new larger map
    char** newMap = new char*[newMaxRow];
    for (int i = 0; i < newMaxRow; ++i) {
        newMap[i] = new char[newMaxCol];
    }

    // Copy contents into each quadrant
    for (int i = 0; i < maxRow; ++i) {
        for (int j = 0; j < maxCol; ++j) {
            newMap[i][j] = map[i][j]; // Quadrant A
            newMap[i][j + maxCol] = (map[i][j] == TILE_PLAYER) ? TILE_OPEN : map[i][j]; // Quadrant B
            newMap[i + maxRow][j] = (map[i][j] == TILE_PLAYER) ? TILE_OPEN : map[i][j]; // Quadrant C
            newMap[i + maxRow][j + maxCol] = (map[i][j] == TILE_PLAYER) ? TILE_OPEN : map[i][j]; // Quadrant D
        }
    }

    // Deallocate the old map to avoid memory leaks
    deleteMap(map, maxRow);

    // Update maxRow and maxCol to reflect the new map size
    maxRow = newMaxRow;
    maxCol = newMaxCol;

    return newMap;
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
    // Check for out-of-bounds movement
    if (nextRow < 0 || nextRow >= maxRow || nextCol < 0 || nextCol >= maxCol) {
        return STATUS_STAY; // Out of bounds
    }

    char nextTile = map[nextRow][nextCol];

    // Check for impassable tiles
    if (nextTile == TILE_PILLAR || nextTile == TILE_MONSTER) {
        return STATUS_STAY; // Can't move onto pillars or monsters
    }

    // Check for treasure
    if (nextTile == TILE_TREASURE) {
        player.treasure++;
        map[player.row][player.col] = TILE_OPEN; // Clear previous player position
        player.row = nextRow;
        player.col = nextCol;
        map[nextRow][nextCol] = TILE_PLAYER; // Update player position
        return STATUS_TREASURE;
    }

    // Check for exit
    if (nextTile == TILE_EXIT) {
        if (player.treasure > 0) {
            map[player.row][player.col] = TILE_OPEN; // Clear previous player position
            player.row = nextRow;
            player.col = nextCol;
            map[nextRow][nextCol] = TILE_PLAYER;
            return STATUS_ESCAPE; // Player escapes
        } else {
            return STATUS_STAY; // Can't exit without treasure
        }
    }

    // Check for amulet
    if (nextTile == TILE_AMULET) {
        map[player.row][player.col] = TILE_OPEN; // Clear previous player position
        player.row = nextRow;
        player.col = nextCol;
        map[nextRow][nextCol] = TILE_PLAYER;
        return STATUS_AMULET;
    }

    // Check for door to next level
    if (nextTile == TILE_DOOR) {
        map[player.row][player.col] = TILE_OPEN; // Clear previous player position
        player.row = nextRow;
        player.col = nextCol;
        map[nextRow][nextCol] = TILE_PLAYER;
        return STATUS_LEAVE; // Move to the next level
    }

    // Regular open move
    if (nextTile == TILE_OPEN) {
        map[player.row][player.col] = TILE_OPEN; // Clear previous player position
        player.row = nextRow;
        player.col = nextCol;
        map[nextRow][nextCol] = TILE_PLAYER;
        return STATUS_MOVE; // Successful move
    }

    return STATUS_STAY; // Default return if no conditions are met
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
    bool monsterReachedPlayer = false;

    // Check each direction (up, down, left, right) for monsters moving toward the player

    // Check up (above player)
    for (int i = player.row - 1; i >= 0; --i) {
        if (map[i][player.col] == TILE_PILLAR) break; // Obstacle blocks line of sight
        if (map[i][player.col] == TILE_MONSTER) {
            map[i][player.col] = TILE_OPEN; // Monster moves down
            map[i + 1][player.col] = TILE_MONSTER;
            if (i + 1 == player.row) monsterReachedPlayer = true; // Monster reached player
            break;
        }
    }

    // Check down (below player)
    for (int i = player.row + 1; i < maxRow; ++i) {
        if (map[i][player.col] == TILE_PILLAR) break; // Obstacle blocks line of sight
        if (map[i][player.col] == TILE_MONSTER) {
            map[i][player.col] = TILE_OPEN; // Monster moves up
            map[i - 1][player.col] = TILE_MONSTER;
            if (i - 1 == player.row) monsterReachedPlayer = true; // Monster reached player
            break;
        }
    }

    // Check left (left of player)
    for (int j = player.col - 1; j >= 0; --j) {
        if (map[player.row][j] == TILE_PILLAR) break; // Obstacle blocks line of sight
        if (map[player.row][j] == TILE_MONSTER) {
            map[player.row][j] = TILE_OPEN; // Monster moves right
            map[player.row][j + 1] = TILE_MONSTER;
            if (j + 1 == player.col) monsterReachedPlayer = true; // Monster reached player
            break;
        }
    }

    // Check right (right of player)
    for (int j = player.col + 1; j < maxCol; ++j) {
        if (map[player.row][j] == TILE_PILLAR) break; // Obstacle blocks line of sight
        if (map[player.row][j] == TILE_MONSTER) {
            map[player.row][j] = TILE_OPEN; // Monster moves left
            map[player.row][j - 1] = TILE_MONSTER;
            if (j - 1 == player.col) monsterReachedPlayer = true; // Monster reached player
            break;
        }
    }

    return monsterReachedPlayer; // Return true if a monster reached the player
}

