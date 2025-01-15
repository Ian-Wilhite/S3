#include <iostream>
#include <sstream>
#include "Player.h"

using std::vector;
using std::string;
using std::size_t;
using std::cout;
using std::cin;

Player::Player(bool isAI) : isAI(isAI) {
    // Initialize as either AI or human player based on isAI flag
}

// Add a card to the player's hand
void Player::addToHand(Card* c) {
    hand.push_back(c);
}

// Get the number of cards in the player's hand
size_t Player::getHandSize() {
    return hand.size();
}

// Return a string representation of the player's hand
string Player::getHandString() {
    std::ostringstream oss;
    for (size_t i = 0; i < hand.size(); ++i) {
        oss << hand[i]->getRank() << " " << hand[i]->getSuit();
        if (i < hand.size() - 1) {
            oss << ", ";
        }
    }
    return oss.str();
}

Card* Player::playCard(const vector<string>& suits, string& currentRank, string& currentSuit) {
    if (isAI) {
        // AI player: play the first playable card, or draw if none available
        for (size_t i = 0; i < hand.size(); ++i) {
            if (hand[i]->canBePlayed(currentRank, currentSuit)) {
                currentRank = hand[i]->getRank();
                currentSuit = hand[i]->getSuit();
                hand[i]->play();
                Card* playedCard = hand[i];
                
                // Remove the card from hand
                hand.erase(hand.begin() + i);
                return playedCard;
            }
        }
        return nullptr;  // Draw a card if no valid card found
    } else {
        // Human player: prompt for input until a valid play is made
        string rank, suit;
        cout << "Your hand contains: " << getHandString() << "\n";
        cout << "The next card played must be a " << currentRank << " or " << currentSuit << "\n";
        cout << "What would you like to play? (enter \"draw card\" to draw a card)\n";
        while (true) {
            std::getline(cin, rank);
            
            if (rank.empty()) {
                continue;  // Re-prompt the user
            }

            if (rank == "draw card") {
                return nullptr;
            }

            std::istringstream iss(rank);
            iss >> rank >> suit;

            bool cardFound = false;
            for (size_t i = 0; i < hand.size(); ++i) {
                if (hand[i]->getRank() == rank && hand[i]->getSuit() == suit) {
                    cardFound = true;
                    if (hand[i]->canBePlayed(currentRank, currentSuit)) {
                        currentRank = hand[i]->getRank();
                        currentSuit = hand[i]->getSuit();
                        hand[i]->play();
                        Card* playedCard = hand[i];
                        
                        // Remove the card from hand
                        hand.erase(hand.begin() + i);
                        
                        if (rank == "8") {
                            // Prompt player to choose a suit after playing an 8
                            string newSuit;
                            cout << "What suit would you like to declare?\n";
                            while (true) {
                                cin >> newSuit;

                                // Manually check if newSuit is in suits
                                bool validSuit = false;
                                for (const auto& suitOption : suits) {
                                    if (suitOption == newSuit) {
                                        validSuit = true;
                                        break;
                                    }
                                }

                                if (validSuit) {
                                    currentSuit = newSuit;
                                    break;
                                } else {
                                    cout << "That's not a suit in this deck. Try again.\n";
                                }
                            }
                        }
                        return playedCard;
                    } else {
                        cout << "You can't play that card. Try again.\n";
                    }
                }
            }
            if (!cardFound) {
                cout << "That's not a card you have. Try again.\n";
            }
        }
    }
}