import pynmea2
import io
import serial
import time


class NmeaGps:
    def __init__(self, **kwargs):
        print(kwargs["serial_file"])
        serial_port = serial.Serial(kwargs["serial_file"],
                                    baudrate=kwargs["baud_rate"],
                                     bytesize=kwargs["bit_rate"],
                                    timeout=kwargs["timeout"],
                                    parity=serial.PARITY_EVEN)
        self.__gps_line_type = kwargs["gps_line_type"]
        self.serial_output = io.TextIOWrapper(io.BufferedRWPair(serial_port, serial_port))
        # keys to retrieve
        self.__longitude_key = "longitude"
        self.__latitude_key = "latitude"
        self.__time_key = "time"

    # holds current values
        self.__latitude = None
        self.__longitude = None
        self.__last_update = None

    # checks that the data is streaming and valid
    def is_valid(self) -> bool:
        try:
            line = self.serial_output.readline()
            pynmea2.parse(line)
        
        except serial.SerialException as e:
            return False

        except pynmea2.ParseError as e:
            return False
        
        return True

    # checks whether satellites are acquired and current location is received
    def is_signal_acquired(self) -> bool:
        while True:
            try:
                line = self.serial_output.readline()
                if self.__gps_line_type in line:
                    print(line)
                    msg = pynmea2.parse(line)
                    if msg.lat == "":
                        return False
                    else:
                        return True

            except serial.SerialException as e:
                raise RuntimeError("Gps serial error")

            except pynmea2.ParseError as e:
                raise RuntimeError("Gps parse error")

    # update current location
    def update(self):
        while True:
            try:
                line = self.serial_output.readline()
                if self.__gps_line_type in line:
                    msg = pynmea2.parse(line)
                    self.__latitude = msg.latitude
                    self.__longitude = msg.longitude
                    self.__last_update = time.time()
                    return

            except serial.SerialException as e:
                raise RuntimeError("Gps serial error")

            except pynmea2.ParseError as e:
                raise RuntimeError("Gps parse error")

    # returns location as a dictionary along with time location was saved
    def get_location(self) -> dict:
        return {
                self.__latitude_key: self.__latitude,
                self.__longitude_key: self.__longitude,
                self.__time_key: self.__last_update
                }
