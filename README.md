# Router Location Estimation

This project is aimed at predicting a routers location based on RSSI values collected from its Beacon.
The motivation for this project was to experiment and see if RSSI values alone are enough to predict the routers location with reasonable accuracy.

for Usage scroll to bottom.

## Methodology

1. Collect Beacon data and gps data and store into Json and CSV (Json was chosen to accommodate ESSID with a ",")
2. Cross reference timestamps from GPS data and Packet Collection Data to match RSSI to coordinates
3. Translate RSSI to distance using Log-Distance Path Loss Model with value tuning to better represent Wifi signal in urban areas
4. Calculate coordinates using measured distances at varying coordinates (explained in detail later on)

## Project Status
The current state of the project is designed as a POC, meaning not aimed at deployment. There are still improvements to be made to the algorithm and ease of use.

### Languages

The project combines both c++ and python3.

The sniffer is written in c++ using the library libtins due to the importance of efficiency in packet capturing.

The rest of the project uses python3.9
To both read gps information and process the data does not require performance and python has many Libraries offering easy solutions to generating maps and working with data, making it the ideal choice.

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
- Experiment with data collection by drone to reduce signal interference and further improve results while taking into consideration spherical estimations rather than circular
- Attempt a machine learning approach for better distance estimation


## Prediction Algorithm

To predict the router's location we use a Weighted Least Squares approach.
We find the optimal coordinates by looking for coordinates that reduce error measured as follows:

    for distance_measured in distances:
	    error += weight*(distance - distance_from_optimal_coordinates)^2

As for weights, during data processing and experimenting, it was found that the stronger the RSSI the more accurate the estimated distance was. Therefore we produce weights for each measured distance according to the RSSI that was used to measure it.

Furthermore RSSI weaker than -80 dbm is not estimated well and therefore all packets that match this are thrown out.

### Vizualization:
<img width="366" alt="Screen Shot 2021-09-15 at 7 27 12 PM" src="https://user-images.githubusercontent.com/82959055/133539406-9978206a-2f91-4c79-bb18-47501b23485f.png">

The center of each point represents a location where a Beacon was received.
The radius of each circle represents the distance that was calculated based on that Beacon's RSSI value.
To find the router, we find the optimal point (cloud) whose sum of the distances from the point to the circles is the smallest.

## Results

An important factor in gathering data is the path on which the data was gathered.

This can be seen in the following examples:

We walked different paths to see how accurate the algorithm was based on the data gathering path.

Home icon - actual location

Cloud icon - estimate

Important: circles were made smaller in order to better see path that was taken

Path 1:

<img width="498" alt="Screen Shot 2021-09-15 at 7 21 00 PM" src="https://user-images.githubusercontent.com/82959055/133539744-afe820db-e900-448f-bd19-1c52a78bc441.png">

Path 2:

<img width="495" alt="Screen Shot 2021-09-15 at 7 35 41 PM" src="https://user-images.githubusercontent.com/82959055/133540128-1b62a25a-b23c-4ff5-96ec-ebf41a853138.png">

Path 3:

<img width="519" alt="Screen Shot 2021-09-15 at 7 39 03 PM" src="https://user-images.githubusercontent.com/82959055/133540453-2d5fcb9f-3361-492b-82f0-58422e4ade99.png">

Path 4:

<img width="366" alt="Screen Shot 2021-09-15 at 7 40 29 PM" src="https://user-images.githubusercontent.com/82959055/133540573-a02005d8-8817-44b0-8b2a-d6d2974404de.png">

Combined data:

<img width="481" alt="Screen Shot 2021-09-15 at 7 42 16 PM" src="https://user-images.githubusercontent.com/82959055/133540760-c75a9524-7070-4d57-b51f-0a3cc1fe2a3e.png">

As can be seen in order to get accurate estimations it is important to get a variety of paths rather than a single path. 
In path 2 and path 3, we did not pass close to the router and therefore the optimal location was on the wrong side of the street.
From the results we can conclude that the algorithm heavily depends on a variety of sampling locations and a lack of causes issues.
But with enough variety the Algorithm does a decent job at estimating the location, reaching errors of 2 to 10 meters.



## Usage

1. go into make_config.py and make changes according to setup used. Descriptions of configurations are provided in file.
2. run python make_config.py to create the configuration file.
3. run 'python setup.py install' to install python dependencies
4. install the following c++ libs:

	a. libtins
	
	b. jsoncpp
	
	c. libpcap
	
4. change directory to sniffer
5. run 'make' to produce executable
6. place executable in location chosen in config file
7. run 'python data_collection.py' to collect data
8. run 'python data2map.py' to produce a map with the estimation


