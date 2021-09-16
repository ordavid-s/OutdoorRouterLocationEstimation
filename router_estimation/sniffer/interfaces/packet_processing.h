//
// Created by Or Shafran on 9/8/21.
//
#include <iostream>
#include <tins/tins.h>
#include <json/json.h>

using std::string;
using std::runtime_error;

using namespace Tins;
using namespace std::chrono;

#ifndef INTERFACES_PACKET_PROCESSING_H
#define INTERFACES_PACKET_PROCESSING_H

/**
* Packet Processing
*
* Implements a functor used to process beacon packets and write them to a json file.
* The following functions are available:
*   BeaconToCsv(const string& file_name)    - constructor that takes in the path to write json to
*   stop_sniffing(int signum)               - function called to stop capture
*/

class BeaconToCsv {
    string filename;
    static bool continue_sniff_loop;
public:
    BeaconToCsv(const string& file_name);
    bool operator()(PDU &pdu);
    // meant to be used to catch sig int
    static void stop_sniffing(int signum);

};


#endif //INTERFACES_PACKET_PROCESSING_H
