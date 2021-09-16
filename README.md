# Router Location Estimation

This project is aimed at predicting a routers location based on RSSI values collected from its Beacon.
The motivation for this project was to experiment and see if RSSI values alone are enough to predict the routers location with reasonable accuracy.


## Methodology

1. Collect Beacon data and gps data and store into Json and CSV (Json was chosen to accommodate ESSID with a ",")
2. Cross reference timestamps from GPS data and Packet Collection Data to match RSSI to coordinates
3. Translate RSSI to distance using Log-Distance Path Loss Model with value tuning to better represent Wifi signal in urban areas
4. Calculate coordinates using measured distances at varying coordinates (explained in detail later on)

## Project Status
The current state of the project is designed as a POC, meaning not aimed at deployment. There are still improvements to be made to the algorithm and ease of use.

### Supported Platforms

The project is supported on both macOS and Linux.
Currently there are no known bugs in either OS.

### Requirements

	- Wifi driver should be using RadioTap
	- GPS should be using NMEA to communicate its data
	- Wifi Adapter must be put in Monitor mode manually
	- Wifi Channel must be set manually
	- To convert data to a map, internet connection is required

### Future Development
- Estimation confidence level using the achieved error in optimization process
- Add Monitor mode and Channel hopping capability to the interface class
- Test on more routers and in different environments to better optimize distance estimation based on RSSI
- Experiment with data collection by drone to reduce signal interference and further improve results


## Prediction Algorithm

To predict the router's location we use a Weighted Least Squares approach.
We find the optimal coordinates by looking for coordinates that reduce error measured as follows:

    for distance_measured in distances:
	    error += weight*(distance - distance_from_optimal_coordinates)^2

As for weights, during data processing and experimenting, it was found that the stronger the RSSI the more accurate the estimated distance was. Therefore we produce weights for each measured distance according to the RSSI that was used to measure it.

Furthermore RSSI weaker than -80 dbm is not estimated well and therefore all packets that match this are thrown out.

