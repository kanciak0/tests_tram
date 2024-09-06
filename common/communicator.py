import configparser
import threading
import time
import serial
import os
from datetime import datetime


class SerialCommunicator:
    def __init__(self, config_file='config_file.txt', log_dir='logs'):
        config = configparser.ConfigParser()
        config.read(config_file)

        if not config.has_section('serial'):
            raise configparser.NoSectionError('serial')

        self.port = config.get('serial', 'port')
        self.baudrate = config.getint('serial', 'baudrate')
        self.timeout = config.getfloat('serial', 'timeout')
        self.password = config.get('serial', 'password')

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

    def write(self, command):
        self.ser.write(command.encode())
        time.sleep(0.1)

    def read(self):
        data = self.ser.read(self.ser.in_waiting or 1).decode('utf-8')
        self._log_data(data)
        return data

    def _log_data(self, data):
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


    def _is_unwanted_entry(self, entry):
        """Determine if the log entry should be ignored."""
        # Check if the entry is empty or starts with 'debug >'
        if entry == "" or entry.startswith("debug >"):
            return True
        return False

    def send_command_and_wait(self, command, expected_message, timeout=30):
        self.write(command)
        return self.wait_for_message(expected_message, timeout)

    def wait_for_message(self, expected_message, timeout=45):
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

    def wait_for_one_of_expected_messages(self, expected_messages, timeout=45):
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

    def is_debug_mode(self):
        self.ser.write(b'\n\r')
        if not self.wait_for_message("debug >", 3):
            return False
        else:
            return True

    def read_console_output(self, line_count=5, timeout=5):
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

    def wait_for_message_and_take_value(self, expected_message, timeout=30):
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
    def get_value_from_response(response, start_index):
        return response[start_index:].strip()

    def check_lct(self):
        if not self.wait_for_message("LCT: OK"):
            if self.wait_for_message("LCT: Blad"):
                return False
        else:
            return True

    def read_configuration_from_file(self, file_path):
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


