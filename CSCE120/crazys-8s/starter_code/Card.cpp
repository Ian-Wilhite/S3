#include <cctype>
#include <stdexcept>
#include "Card.h"
using std::string;

// Constructor to initialize a Card with rank and suit, and checks for invalid arguments
Card::Card(string rank, string suit) : rank(rank), suit(suit), timesPlayed(0) {
    if (rank.empty() || suit.empty()) {
        throw std::invalid_argument("Rank and suit cannot be empty.");
    }
    for (char c : rank) {
        if (!std::isalnum(c)) {
            throw std::invalid_argument("Rank contains non-alphanumeric characters.");
        }
    }
    for (char c : suit) {
        if (!std::isalnum(c)) {
            throw std::invalid_argument("Suit contains non-alphanumeric characters.");
        }
    }
}

// Getter for rank
string Card::getRank() {
    return rank;
}

// Getter for suit
string Card::getSuit() {
    return suit;
}

// Getter for timesPlayed
int Card::getTimesPlayed() {
    return timesPlayed;
}

// Check if this card can be played based on the current rank and suit
bool Card::canBePlayed(string currentRank, string currentSuit) {
    return (rank == "8" || rank == currentRank || suit == currentSuit);
}

// Increment the play count for the card
void Card::play() {
    timesPlayed++;
}
