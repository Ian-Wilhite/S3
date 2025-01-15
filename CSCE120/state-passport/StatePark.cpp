# include "Passport.h"

using std::string, std::vector;

StatePark::StatePark(std::string parkName, double entranceFee, double trailMiles) {
	this->parkName = parkName;
	this->entranceFee = entranceFee;
	this->trailMiles = trailMiles;
	this->camperLog = {};
}
	
string StatePark::getParkName() {
	return this->parkName;
}

double StatePark::getEntranceFee() {
	return this->entranceFee;
}

double StatePark::getTrailMiles() {
	return this->trailMiles;
}

void StatePark::addCamper(Passport* camper) {
	INFO(camper)

	camperLog.push_back(camper);
}

double StatePark::getRevenue() {
    double totalRevenue = 0;
    for (auto camper : camperLog) {
        totalRevenue += camper->checkJuniorPassport() ? entranceFee / 2 : entranceFee;
    }
    return totalRevenue;
}
