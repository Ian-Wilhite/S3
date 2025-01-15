#include <iostream>
#include <fstream>
#include <sstream>
#include <stdexcept>
#include "Game.h"
#include "Card.h"
#include "Player.h"

using std::string;
using std::vector;
using std::ifstream;
using std::runtime_error;
using std::invalid_argument;
using std::cout;

Game::Game() : players({}), suits({}), ranks({}), deck({}), drawPile({}), discardPile({}) {}

// Load deck data from a file, initializing suits, ranks, deck, and drawPile
void Game::loadDeckFromFile(string filename) {
    ifstream file(filename);
    if (!file.is_open()) {
        throw runtime_error("Could not open file: " + filename);
    }

    string line;

    // First line: read suits
    if (!std::getline(file, line)) {
        throw runtime_error("File format error: missing suits line.");
    }
    std::istringstream suitsStream(line);
    string suit;
    while (suitsStream >> suit) {
        suits.push_back(suit);
    }

    // Second line: read ranks
    if (!std::getline(file, line)) {
        throw runtime_error("File format error: missing ranks line.");
    }
    std::istringstream ranksStream(line);
    string rank;
    while (ranksStream >> rank) {
        ranks.push_back(rank);
    }

    // Remaining lines: read each card's rank and suit, adding to deck and drawPile
    while (std::getline(file, line)) {
        std::istringstream cardStream(line);
        string cardRank, cardSuit;
        
        // Try to read rank and suit
        if (!(cardStream >> cardRank >> cardSuit)) {
            throw runtime_error("File format error: invalid card line.");
        }

        // Check for extra data
        string extraData;
        if (cardStream >> extraData) {
            throw runtime_error("File format error: extra data found in card line.");
        }
        
        // Validate rank
        bool validRank = false;
        for (const auto& r : ranks) {
            if (r == cardRank) {
                validRank = true;
                break;
            }
        }
        if (!validRank) {
            throw runtime_error("Invalid card rank: " + cardRank);
        }

        // Validate suit
        bool validSuit = false;
        for (const auto& s : suits) {
            if (s == cardSuit) {
                validSuit = true;
                break;
            }
        }
        if (!validSuit) {
            throw runtime_error("Invalid card suit: " + cardSuit);
        }

        // If rank and suit are valid, create the card and add to the deck
        try {
            Card* card = new Card(cardRank, cardSuit);
            deck.push_back(card);
            drawPile.insert(drawPile.begin(), card);  // Reverse order for efficient drawing
        } catch (const invalid_argument&) {
            throw runtime_error("Invalid card arguments: " + cardRank + " " + cardSuit);
        }
    }
}

// Add a new player to the game (either human or AI)
void Game::addPlayer(bool isAI) {
    Player* player = new Player(isAI);
    players.push_back(player);
}

// Move the top card of the draw pile to the specified player's hand
void Game::drawCard(Player* p) {
    if (drawPile.empty()) {
        if (discardPile.size() < 2) {
            throw runtime_error("Cannot draw a card: no cards left.");
        }
        cout << "Draw pile empty, flipping the discard pile.\n";
        
        // Flip the discard pile to create a new draw pile
        Card* topDiscard = discardPile.back();
        discardPile.pop_back();
        
        while (!discardPile.empty()) {
            drawPile.push_back(discardPile.back());
            discardPile.pop_back();
        }
        discardPile.push_back(topDiscard);
    }
    Card* drawnCard = drawPile.back();
    drawPile.pop_back();
    p->addToHand(drawnCard);
}

// Deal the specified number of cards to each player, and set up the discard pile
Card* Game::deal(int numCards) {
    if (drawPile.empty()) {
        throw runtime_error("Cannot deal: draw pile is empty.");
    }

    // Set the initial discard pile
    Card* initialDiscard = drawPile.back();
    drawPile.pop_back();
    discardPile.push_back(initialDiscard);

    // Deal numCards to each player
    for (int i = 0; i < numCards; ++i) {
        for (Player* player : players) {
            drawCard(player);
        }
    }
    return initialDiscard;
}

// Determine and return the most played suit
string Game::mostPlayedSuit() {
    vector<string> suitNames;
    vector<int> suitCounts;

    // Count timesPlayed for each suit
    for (Card* card : deck) {
        string suit = card->getSuit();
        int index = -1;

        // Check if suit already exists in suitNames vector
        for (size_t i = 0; i < suitNames.size(); ++i) {
            if (suitNames[i] == suit) {
                index = i;
                break;
            }
        }

        // Update count if suit is found, otherwise add new entry
        if (index != -1) {
            suitCounts[index] += card->getTimesPlayed();
        } else {
            suitNames.push_back(suit);
            suitCounts.push_back(card->getTimesPlayed());
        }
    }

    // Find the suit with the maximum play count
    int maxCount = 0;
    string mostPlayed;
    for (size_t i = 0; i < suitNames.size(); ++i) {
        if (suitCounts[i] > maxCount) {
            maxCount = suitCounts[i];
            mostPlayed = suitNames[i];
        }
    }
    return mostPlayed;
}

int Game::runGame() {
    int currentPlayerIndex = 0;
    string currentRank = discardPile.back()->getRank();
    string currentSuit = discardPile.back()->getSuit();

    while (true) {
        Player* currentPlayer = players[currentPlayerIndex];
        cout << "Player " << currentPlayerIndex << "'s turn!\n";

        Card* playedCard = currentPlayer->playCard(suits, currentRank, currentSuit);
        if (playedCard) {
            cout << "Player " << currentPlayerIndex << " plays " << playedCard->getRank() 
                 << " " << playedCard->getSuit();

            // If the card is an 8, allow the player to change the suit
            if (playedCard->getRank() == "8") {
                string newSuit;
                
                // For an AI player, we might want to auto-select a suit, but for now we prompt
                cout << " and changes the suit to ";
                while (true) {
                    cout << "\nChoose a new suit: ";
                    std::cin >> newSuit;

                    // Validate the new suit
                    bool validSuit = false;
                    for (const auto& suitOption : suits) {
                        if (suitOption == newSuit) {
                            validSuit = true;
                            break;
                        }
                    }
                    if (validSuit) {
                        currentSuit = newSuit;
                        cout << currentSuit << ".\n";
                        break;
                    } else {
                        cout << "That's not a suit in this deck. Try again.\n";
                    }
                }
            
            } else {
                cout << ".\n";
                currentRank = playedCard->getRank();
                currentSuit = playedCard->getSuit();
            }

            discardPile.push_back(playedCard);
        } else {
            cout << "Player " << currentPlayerIndex << " draws a card.\n";
            
            // Check if draw pile is empty, and flip the discard pile if needed
            if (drawPile.empty()) {
                if (discardPile.size() < 2) {
                    cout << "Player " << currentPlayerIndex << " cannot draw a card.\n";
                    return -1;  // Tie if no cards left
                }

                cout << "Draw pile empty, flipping the discard pile.\n";
                Card* topDiscard = discardPile.back();
                discardPile.pop_back();

                while (!discardPile.empty()) {
                    drawPile.push_back(discardPile.back());
                    discardPile.pop_back();
                }
                discardPile.push_back(topDiscard);
            }
            drawCard(currentPlayer);
        }

        // Check if current player has won
        if (currentPlayer->getHandSize() == 0) {
            return currentPlayerIndex;
        }

        // Move to the next player
        currentPlayerIndex = (currentPlayerIndex + 1) % players.size();
    }
}


// Destructor to clean up dynamically allocated memory for deck and players
Game::~Game() {
    for (Card* card : deck) {
        delete card;
    }
    for (Player* player : players) {
        delete player;
    }
}
