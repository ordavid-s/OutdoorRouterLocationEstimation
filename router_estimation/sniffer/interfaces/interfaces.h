#ifndef INTERFACES_H
#define INTERFACES_H

#include <iostream>
#include <pcap.h>
#include <tins/tins.h>


using namespace Tins;

/**
* Packet Capture Interface
*
* Implements an Interface objects to be used for packet capture.
* The Interface supports adding a callback function to apply to each packet.
* Interface validates name given name. Channel hopping and monitor mode should be done by user to guarantee success.
* The following functions are available:
* Interface:
*   Constructors:
*       Interface()                                 - takes no arguments, name must be set before using
*	    Interface(const std::string& iface_name)    - takes name as string
*   configurations:
*       setName		                                - Sets interface name, must be a valid interface
*       getName		                                - returns current name
*       enablePromiscuous		                    - enables promiscuous capture
*       disablePromiscuous		                    - disables promiscuous capture
*       setTimeout (not supported in all OS)	    - sets a timeout for how long to wait for packets before exiting
*       setFilter                                   - packet filter string for BPF
*
* WifiInterface:
*   configurations:
*       enableMonitor                               - enables monitor mode, may not be supported on all OS
*       disableMonitor                              - disables monitor mode, may not be supported on all OS
*
*
* capture                                           - captures packets, uses a template for functor that serves
 *                                                      as callback for packet processing.
*
* Errors:
*   InterfaceNameDoesNotExist                       - name trying to set is not a valid interface
*   InterfaceNameNotSet                             - attempting to capture without setting a name
*/


class Interface {
protected:
	std::string name;
	SnifferConfiguration config;
    pcap_t *handler;

    void set_handler();

public:
	// Constructors + Destructor
	Interface() = default;
	virtual ~Interface();
	explicit Interface(const std::string& iface_name);
	// Functions
	void setName(const std::string& iface_name);
	std::string getName();
    template <class callback_type>
    void capture(callback_type callback) {
        Sniffer sniffer(name, config);
        sniffer.sniff_loop(callback);
    }

	void enablePromiscuous();
	void disablePromiscuous();
	void setTimeout(int time);
	void setFilter(const std::string& filter_string);
	// Errors
	class InterfaceNameDoesNotExist;
	class InterfaceNameNotSet;
};

class WifiInterface: public Interface{
public:
	void enableMonitor();
	void disableMonitor();
};

#endif
