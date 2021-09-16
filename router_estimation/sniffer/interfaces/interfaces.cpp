#include "interfaces.h"
#include <iostream>
#include <pcap.h>
#include "packet_processing.h"

using namespace Tins;

static bool doesInterfaceExist(const std::string& iface);

// Errors
class Interface::InterfaceNameDoesNotExist: public std::exception{
	std::string err_message;
public:
	explicit InterfaceNameDoesNotExist(const std::string& name):
		err_message("Invalid Interface: " + name){}
	const char* what() const noexcept override{
		return err_message.c_str();
	}
};

class Interface::InterfaceNameNotSet: public std::exception{
	std::string err_message = "Interface name not set";
public:
	const char* what() const noexcept override{
		return err_message.c_str();
	}
};
// constructors
Interface::Interface(const std::string& iface_name):
	name(iface_name){
		if(!doesInterfaceExist(iface_name)){
			throw Interface::InterfaceNameDoesNotExist(name);
		}
//        set_handler();
}

// get, set name
void Interface::setName(const std::string& iface_name){
	if(!doesInterfaceExist(iface_name)){
		throw Interface::InterfaceNameDoesNotExist(iface_name);
	}
	this->name.assign(iface_name);
//	set_handler();
}

Interface::~Interface() {
    if (handler != NULL) {
        pcap_close(handler);
    }
}

std::string Interface::getName(){
	return name;
}

void Interface::setTimeout(int time){
    config.set_timeout(time);
}

// enables promiscuous

void Interface::enablePromiscuous(){
	config.set_promisc_mode(true);
}

void Interface::disablePromiscuous(){
	config.set_promisc_mode(false);
}

// set filter
void Interface::setFilter(const std::string& filter_string){
	config.set_filter(filter_string);
}

void Interface::set_handler() {
    char errbuf[PCAP_ERRBUF_SIZE+1];
    handler=pcap_create(name.c_str(), errbuf);
}


bool doesInterfaceExist(const std::string& iface){
	pcap_if_t *interfaces, *d;
	char error[PCAP_ERRBUF_SIZE+1];
	if(pcap_findalldevs(&interfaces, error) == -1){
	    if(interfaces != nullptr) {
            pcap_freealldevs(interfaces);
        }
		return false;
	}
	for(d = interfaces; d != nullptr; d = d->next){
		if(iface == d->name ){
		    if(interfaces != nullptr) {
                pcap_freealldevs(interfaces);
            }
			return true;
		}
	}
	return false;
}


// Wifi Interface

void WifiInterface::enableMonitor(){
    config.set_rfmon(true);
}

void WifiInterface::disableMonitor(){
    config.set_rfmon(false);
}
