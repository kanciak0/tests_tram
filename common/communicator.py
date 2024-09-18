import configparser
import platform
import threading
import time
import serial
import os
from datetime import datetime


class SerialCommunicator:
    def __init__(self, config_file: str = 'config_file.txt', log_dir: str = 'logs') -> None:
        self.config_file = config_file
        config = configparser.ConfigParser()
        config.read(config_file)

        system = platform.system()
        if system == "Windows":
            config_section = 'serialWindows'
        elif system == "Linux":
            config_section = 'serialLinux'
        else:
            raise OSError(f"Unsupported platform: {system}")

        if not config.has_section(config_section):
            raise configparser.NoSectionError(config_section)

        self.port = config.get(config_section, 'port')
        self.baudrate = config.getint(config_section, 'baudrate')
        self.timeout = config.getfloat(config_section, 'timeout')
        self.password = config.get(config_section, 'password')

        self.pin = config.get(config_section, 'pin')
        self.apn_name = config.get(config_section, 'apn_name')

        self.ser = serial.Serial(self.port, baudrate=self.baudrate, timeout=self.timeout)

        self.log_dir = log_dir
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

        # Create a timestamp for the log file name
        timestamp = datetime.now().strftime('%Y%m%d_%H%M')
        # Determine the log file based on the COM port from the config
        self.log_file = os.path.join(self.log_dir, f'serial_log_{self.port.replace(":", "_")}_{timestamp}.txt')

        self.reading_thread = None
        self.stop_reading = threading.Event()

    def get_pin(self) -> str:
        """Fetches the PIN dynamically from the config file each time."""
        config = configparser.ConfigParser()
        config.read(self.config_file)
        return config.get('serialWindows' if platform.system() == 'Windows' else 'serialLinux', 'pin')

    def get_apn_name(self) -> str:
        config = configparser.ConfigParser()
        config.read(self.config_file)
        return config.get('serialWindows' if platform.system() == 'Windows' else 'serialLinux', 'apn_name')

    def write(self, command: str) -> None:
        self.ser.write(command.encode())
        time.sleep(0.1)

    def read(self) -> str:
        data = self.ser.read(self.ser.in_waiting or 1).decode('utf-8')
        self._log_data(data)
        return data

    def _log_data(self, data: str) -> None:
        """Log the data to a file with a timestamp, filtering out unwanted entries."""
        # Get the current timestamp with milliseconds
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]  # Slice to get milliseconds
        # Split data into lines and log each line with the timestamp
        log_entries = data.splitlines()
        with open(self.log_file, 'a') as f:
            for entry in log_entries:
                entry = entry.strip()
                if entry and not self._is_unwanted_entry(entry):
                    f.write(f"{timestamp} - {entry}\n")

    @staticmethod
    def _is_unwanted_entry(entry: str) -> bool:
        """Determine if the log entry should be ignored."""
        # Check if the entry is empty or starts with 'debug >'
        if entry == "" or entry.startswith("debug >"):
            return True
        return False

    def send_command_and_wait(self, command: str, expected_message: str, timeout: int = 30) -> bool:
        self.write(command)
        return self.wait_for_message(expected_message, timeout)

    def wait_for_message(self, expected_message: str, timeout: int = 45) -> bool:
        start_time = time.time()
        buffer = ""

        while True:
            if time.time() - start_time > timeout:
                return False

            if self.ser.in_waiting > 0:
                data = self.read()
                buffer += data

                if expected_message in buffer:
                    return True

    def wait_for_one_of_expected_messages(self, expected_messages: list[str], timeout: int = 45) -> bool:
        start_time = time.time()
        buffer = ""

        while True:
            if time.time() - start_time > timeout:
                return False

            if self.ser.in_waiting > 0:
                data = self.read()
                buffer += data

                for message in expected_messages:
                    if message in buffer:
                        return True

    def wait_for_all_expected_messages(self, expected_messages: list[str], timeout: int = 45) -> bool:
        """
        Waits for all the expected messages to be present in the buffer within the specified timeout.

        :param expected_messages: List of messages that should be present in the buffer.
        :param timeout: Time to wait for all messages to appear.
        :return: True if all expected messages are found, False otherwise.
        """
        start_time = time.time()
        buffer = ""
        expected_messages_set = set(expected_messages)
        received_messages_set = set()

        while True:
            if time.time() - start_time > timeout:
                return False

            if self.ser.in_waiting > 0:
                data = self.read()
                buffer += data

                # Check for each expected message in the buffer
                for message in expected_messages_set:
                    if message in buffer:
                        received_messages_set.add(message)
                        if received_messages_set == expected_messages_set:
                            return True

    def is_debug_mode(self) -> bool:
        self.ser.write(b'\n\r')
        if not self.wait_for_message("debug >", 3):
            return False
        else:
            return True

    def read_console_output(self, line_count: int = 5, timeout: int = 5) -> str:
        output = ""
        end_time = time.time() + timeout

        while time.time() < end_time:
            if self.ser.in_waiting > 0:
                data = self.ser.read(self.ser.in_waiting).decode('utf-8')
                output += data

                if output.count('\n') >= line_count:
                    break
            time.sleep(0.1)  # Small delay to avoid busy-waiting

        return output

    def wait_for_message_and_take_value(self, expected_message: str, timeout: int = 30) -> str:
        start_time = time.time()
        buffer = ""

        while time.time() - start_time < timeout:
            if self.ser.in_waiting > 0:
                data = self.read()
                buffer += data

                if expected_message in buffer:
                    return buffer
        return ""

    @staticmethod
    def get_value_from_response(response: str, start_index: int) -> str:
        return response[start_index:].strip()

    def check_lct(self) -> bool:
        if not self.wait_for_message("LCT: OK"):
            if self.wait_for_message("LCT: Blad"):
                return False
        else:
            return True

    @staticmethod
    def read_configuration_from_file(file_path: str) -> dict[str, str]:
        """
        Reads and parses the configuration data from the specified file.

        Args:
            file_path (str): Path to the backup configuration file.

        Returns:
            dict: Parsed configuration data.
        """
        config_data = {}

        with open(file_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                line = line.strip()
                if line and '=' in line:
                    key, value = line.split('=', 1)
                    config_data[key.strip()] = value.strip()

        return config_data
