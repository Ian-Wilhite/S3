#include<iostream>
#include<fstream>
#include<string>
#include "Card.h"
#include "Player.h"
#include "Game.h"

using std::string;

bool loadDeck(Game& g) {
    string filename;
    std::cout << "Choose a file to load the deck from:" << std::endl;
    std::cin >> filename;
    try {
        g.loadDeckFromFile(filename);
    }
    catch (std::runtime_error const&) {
        std::cout << "The file was invalid. Aborting." << std::endl;
        return false;
    }
    return true;
}

int getPlayerCount() {
    std::cout << "Enter number of players:" << std::endl;
    int numPlayers;
    while (true) {
        if ((!(std::cin >> numPlayers)) || numPlayers <= 0) {
            if (std::cin.fail()) {
                // Clear the fail flag
                std::cin.clear();
                // Remove the non-integer data from the stream
                string garbage;
                std::cin >> garbage;
            }
            std::cout << "Please enter a positive number" << std::endl;
        }
        else {
            // break out of the loop once we've read a valid number
            break;
        }
    }
    return numPlayers;
}

void setupPlayers(Game& g, int numPlayers) {
    for (int i = 0; i < numPlayers; ++i) {
        char playerType;
        while (true) {
            std::cout << "Is player " << i << " an AI? (y/n): ";
            std::cin >> playerType;
            if (playerType == 'y' || playerType == 'Y') {
                g.addPlayer(true);  // AI player
                break;
            }
            else if (playerType == 'n' || playerType == 'N') {
                g.addPlayer(false); // Human player
                break;
            }
            else {
                std::cout << "Please enter y or n." << std::endl;
            }
        }
    }
}

void setupGame(Game& g) {
    int cardsToDeal;
    while (true) {
        std::cout << "How many cards should each player start with?" << std::endl;
        if (std::cin >> cardsToDeal && cardsToDeal > 0) {
            break;
        }
        else {
            std::cin.clear();  // Clear the fail flag
            std::cin.ignore(10000, '\n');  // Ignore any invalid input
            std::cout << "Please enter a positive number" << std::endl;
        }
    }
    
    g.deal(cardsToDeal);
    
}

int main() {
    Game g;
    
    if (!loadDeck(g)) {
        return 1;
    }
    
    int numPlayers = getPlayerCount();
    setupPlayers(g, numPlayers);
    setupGame(g);
    
    int winner = g.runGame();
    if (winner != -1) {
        std::cout << "Player " << winner << " wins!" << std::endl;`
    }
    else {
        std::cout << "The game is a draw!" << std::endl;
    }
    
    std::cout << "The most played suit was " << g.mostPlayedSuit() << std::endl;
    
    return 0;
}
