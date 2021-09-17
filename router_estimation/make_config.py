import json

"""
Creates a configuration file in the proper format
"""


CONFIG_PATH = "./config.json"

CONFIG = {
    # GPS configurations
    "gps": {
        # baud rate, depends on gps, 9600 usually works
        "baud_rate": 9600,
        # how long to wait for gps to send data
        "timeout": 1,
        # bit rate of gps messages, 5 should work
        "bit_rate": 5,
        # gps data that contains the coordinates (NMEA protocol)
        "gps_line_type": "GPGGA",
        # keys used to save gps data
        "longitude_key": "longitude",
        "latitude_key": "latitude",
        "time_key": "time",
        # where to save the data
        "csv_path": "gps_data.csv",
        # serial file that gps saves data to
        # in MACOS usually "/dev/tty.usbmodem*"
        # in linux usually "/dev/ttyACM0
        "serial_file": "/dev/tty.usbmodem144201"
    },
    # Interface configuration
    "interface": {
        # BPF filter to use
        "filter": "wlan type mgt subtype beacon",
        # name of interface to capture on
        "interface_name": "en0",
        # how long to wait for packets before exiting, not supported on all OS
        "timeout": 3000
    },
    # packet processing configurations
    "packet_processing": {
        # path to save packet data
        "json_path": "../packet_data.json",
        # path of cpp executable to capture data
        "executable_path": "./capture"
    },
    # Configurations for map creation
    "maps": {
        # path to gps data
        "gps_path": "./data/combined/gps_data.csv",
        # path to packets data
        "packets_path": "./data/combined/packet_data.json",
        # icon to display on map, for more possibilities check folium website
        "icon_to_display": "cloud",
        # path to save map to
        "map_save_path": "./map.html",
        # initial latitude and longitude used for map
        "init_lat": 37.34103951865338,
        "init_long": -122.02313614757549,
        # initial zoom on map
        "init_zoom": 18,
        # name of network to locate
        "ssid": "Kfitz",
        # whether to show predicted distances, used to understand algorithm
        "show_rssi_circles": False,
    },
    # data processing configuration
    "data_processing": {
        # number of packets to average before estimating distance
        "num_packets_to_average": 80,
        # filter out all packets that are received at a weaker signal
        "min_usable_rssi": -90,
        # minimum rows to make guess
        "min_rows_to_make_guess": 30
    }
}

if __name__ == '__main__':
    with open(CONFIG_PATH, 'w') as fp:
        json.dump(CONFIG, fp, indent=4, sort_keys=True)
