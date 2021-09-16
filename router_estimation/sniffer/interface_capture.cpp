//
// Created by Or Shafran on 9/9/21.
//
#include <fstream>
#include <iostream>
#include <csignal>
#include "json/json.h"
#include "interfaces/interfaces.h"
#include "interfaces/packet_processing.h"

#define CONFIG_PATH "./config.json"

void getConfig(std::string config_path, Json::Value& root );

int main () {
    // register signal SIGINT and signal handler
    Json::Value root;
    getConfig(CONFIG_PATH, root);
    std::string interface_name = root["interface"]["interface_name"].asString();
    std::string filter = root["interface"]["filter"].asString();
    std::string json_path = root["packet_processing"]["json_path"].asString();
    WifiInterface iface;
    iface.setName(interface_name);
    iface.setFilter(filter);
    iface.enableMonitor();
    BeaconToCsv packet_callback(json_path);
    signal(SIGINT, packet_callback.stop_sniffing);
    std::cout << "Capturing..." << std::endl;
    iface.capture<BeaconToCsv>(packet_callback);
}

void getConfig(std::string config_path, Json::Value& root ){
    Json::Reader reader;
    std::ifstream test(config_path, std::ifstream::binary);
    bool parsing_successful = reader.parse( test, root, false );
    if (!parsing_successful){
        std::cout  << reader.getFormatedErrorMessages() << std::endl;
    }
}
