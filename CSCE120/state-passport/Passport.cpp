# include "Passport.h"

using std::string, std::vector;

// TODO: implement constructor using member initializer list
Passport::Passport(string camperName, bool isJuniorCamper){
	this->camperName = camperName;
	this-> isJuniorPassport = isJuniorCamper;
	this->parksVisited = {};
}

string Passport::getCamperName() {
	// TODO: implement getter

	return this->camperName;
}

bool Passport::checkJuniorPassport() {
	
	return this->isJuniorPassport;
}

void Passport::addParkVisited(StatePark* park) {
	INFO(park)
	// TODO: implement function
	this->parksVisited.push_back(park);
    park->addCamper(this);  
	return;
}

double Passport::getMilesHiked() {
    double miles = 0;
    for (auto park : parksVisited) {
        miles += isJuniorPassport ? park->getTrailMiles() * 2 : park->getTrailMiles();
    }
    return miles;
}

int Passport::getHikerLevel() {
    return static_cast<int>(getMilesHiked() / 100);
}
