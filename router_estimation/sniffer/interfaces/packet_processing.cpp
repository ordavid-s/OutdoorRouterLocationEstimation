//
// Created by Or Shafran on 9/9/21.
//

#include <iostream>
#include <fstream>
#include <tins/tins.h>
#include <chrono>
#include <json/json.h>
#include "packet_processing.h"

using std::string;
using std::runtime_error;

using namespace Tins;
using namespace std::chrono;

static void writeToCsv(const string& ssid, const string& addr, int signal, int freq, long long time,
                string filename){
    Json::Value packet_json;
    packet_json["addr"] = addr;
    packet_json["ssid"] = ssid;
    packet_json["signal"] = signal;
    packet_json["frequency"] = freq;
    packet_json["timestamp"] = (int)time;
    Json::StreamWriterBuilder builder;
    std::unique_ptr<Json::StreamWriter> writer(
            builder.newStreamWriter());
    std::ofstream myfile;
    myfile.open (filename, std::ios_base::app);
    writer->write(packet_json, &myfile);
    myfile << std::endl;
    myfile.close();
}

bool BeaconToCsv::continue_sniff_loop = true;


BeaconToCsv::BeaconToCsv(const string& file_name):
        filename(file_name){}



bool BeaconToCsv::operator()(PDU& pdu) {
    // Get the Dot11 layer
    const Dot11Beacon& beacon = pdu.rfind_pdu<Dot11Beacon>();
    const RadioTap& radiotap = pdu.rfind_pdu<RadioTap>();
    // All beacons must have from_ds == to_ds == 0
    if (!beacon.from_ds() && !beacon.to_ds()) {
        string addr = beacon.addr2().to_string();
        string ssid;
        try {
            /* If no ssid option is set, then Dot11::ssid will throw
             * a std::runtime_error.
             */
            ssid = beacon.ssid();
        }
        catch (runtime_error&) {
            ssid = ""; // no ssid leave empty name
        }
        int db_signal = int(radiotap.dbm_signal());
        int channel_freq =  int(radiotap.channel_freq());
        long long ms  =  duration_cast<milliseconds>(system_clock::now().time_since_epoch()).count();
        long long seconds =   ms/1000; // milliseconds in a second
        writeToCsv(ssid, addr, db_signal, channel_freq, seconds, filename);
    }
    return BeaconToCsv::continue_sniff_loop;
}

void BeaconToCsv::stop_sniffing(int signum){
    std::cout << "caught sig int" << std::endl;
    BeaconToCsv::continue_sniff_loop = false;
}