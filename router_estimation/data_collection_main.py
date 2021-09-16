import json
import subprocess
import signal
from gps.gps import NmeaGps

CONFIG_NAME = "config.json"


def get_gps(config: dict):
    gps = NmeaGps(**config)
    if not gps.is_valid():
        raise RuntimeError("Gps not working")
    return gps


def get_config():
    # Opening JSON file

    with open(CONFIG_NAME) as nf:
        data = json.load(nf)
    return data


class DataCollector:
    def __init__(self, gps_obj: NmeaGps, executable: str, gps_data_path: str):
        self.__gps_data_path = gps_data_path
        self.__gps = gps_obj
        self.__collect_data = False
        self.__executable_path = executable
        self.__packet_collection_process = None
        signal.signal(signal.SIGINT, self.__signal_handler)

    def __signal_handler(self, signum, frame):
        print("stopping collection")
        self.__packet_collection_process.send_signal(signal.SIGTERM)
        self.__packet_collection_process.terminate()
        self.__collect_data = False

    def __run_packet_collection(self):
        self.__packet_collection_process = subprocess.Popen([self.__executable_path])
        if self.__packet_collection_process is None:
            raise RuntimeError("unable to start packet collecting")

    def collect_data(self):
        self.__collect_data = True
        self.__run_packet_collection()
        print("starting gps collection")
        with open(self.__gps_data_path, "a+") as nf:
            while self.__collect_data:
                self.__gps.update()
                location = self.__gps.get_location()
                nf.write("{},{},{}\n".format(location["latitude"], location["longitude"], location["time"]))


if __name__ == '__main__':
    config = get_config()
    gps = get_gps(config["gps"])
    if not gps.is_signal_acquired():
        print("unable to acquire gps signal")
        exit()
    data_collector = DataCollector(gps, config["packet_processing"]["executable_path"], config["gps"]["csv_path"])
    data_collector.collect_data()
