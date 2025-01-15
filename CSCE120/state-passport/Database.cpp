# include "Database.h"

using std::string, std::vector;

// TODO: implement constructor using member initializer list
Database::Database(){
	this->stateParkList = {};
	this->camperList = {};
}

Database::~Database() {
	for (unsigned int i = 0; i < stateParkList.size(); ++i) {
		delete stateParkList.at(i);
	}
	
	for (unsigned int i = 0; i < camperList.size(); ++i) {
		delete camperList.at(i);
	}
}

void Database::addStatePark(string parkName, double entranceFee, double trailMiles) {
	INFO(parkName)
	INFO(entranceFee)
	INFO(trailMiles)

	// TODO: implement function
	StatePark* park = new StatePark(parkName, entranceFee, trailMiles); 
	this->stateParkList.push_back(park);

	return;
}

void Database::addPassport(string camperName, bool isJuniorPassport) {
	INFO(camperName)
	INFO(isJuniorPassport)

	// TODO: implement function
	Passport* camper = new Passport(camperName, isJuniorPassport);
	this->camperList.push_back(camper);

	return;
}

void Database::addParkToPassport(std::string camperName, std::string parkName) {
    Passport* foundCamper = nullptr;
    StatePark* foundPark = nullptr;

    // Find camper
    for (Passport* camper : camperList) {
        if (camper->getCamperName() == camperName) {
            foundCamper = camper;
            break;
        }
    }

    // Find park
    for (StatePark* park : stateParkList) {
        if (park->getParkName() == parkName) {
            foundPark = park;
            break;
        }
    }

    // Add park to camper if both found
    if (foundCamper && foundPark) {
        foundCamper->addParkVisited(foundPark);
    }
}

vector<string> Database::getParksInRevenueRange(double lowerBound, double upperBound) {
	INFO(lowerBound)
	INFO(upperBound)

	// TODO: (optional) implement function
	
	return {};
}

vector<string> Database::getHikersAtLeastLevel(int level) {
	INFO(level)

	// TODO: (optional) implement function

	return {};
}
