import serial
import time
import configparser
import os


class SerialCommunicator:
    def __init__(self, config_file='config_file.txt', log_dir='logs', test_file_name=""):
        config = configparser.ConfigParser()
        config.read(config_file)

        if not config.has_section('serial'):
            raise configparser.NoSectionError('serial')

        self.port = config.get('serial', 'port')
        self.baudrate = config.getint('serial', 'baudrate')
        self.timeout = config.getfloat('serial', 'timeout')
        self.password = config.get('serial', 'password')

        self.ser = serial.Serial(self.port, baudrate=self.baudrate, timeout=self.timeout)

        self.test_file_name = test_file_name
        self.log_dir = log_dir
        self.log_file = self.create_log_file()

    def write(self, command):
        self.log_message(f"Sending command: {command}")
        self.ser.write(command.encode())
        time.sleep(0.1)

    def read(self):
        data = self.ser.read(self.ser.in_waiting or 1).decode('utf-8').strip()
        self.log_message(f"Received data: {data}")
        return data

    def send_command_and_wait(self, command, expected_message, timeout=30):
        self.write(command)
        return self.wait_for_message(expected_message, timeout)

    def wait_for_message(self, expected_message, timeout=45):
        start_time = time.time()
        buffer = ""

        while True:
            if time.time() - start_time > timeout:
                self.log_message("Timeout waiting for message.")
                return False

            if self.ser.in_waiting > 0:
                data = self.read()
                buffer += data
                self.log_message(f"Buffer updated: {buffer}")

                if expected_message in buffer:
                    return True

    def wait_for_one_of_expected_messages(self, expected_messages, timeout=45):
        start_time = time.time()
        buffer = ""

        while True:
            if time.time() - start_time > timeout:
                self.log_message("Timeout waiting for messages.")
                return False

            if self.ser.in_waiting > 0:
                data = self.read()
                buffer += data
                self.log_message(f"Buffer updated: {buffer}")

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
                self.log_message(f"Console output: {data}")

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
                self.log_message(f"Buffer updated: {buffer}")

                if expected_message in buffer:
                    return buffer

        self.log_message(f"Timeout: '{expected_message}' not received within {timeout} seconds.")
        return ""

    @staticmethod
    def get_value_from_response(response, start_index):
        return response[start_index:].strip()

    def check_lct(self):
        if not self.wait_for_message("LCT: OK"):
            self.log_message("LCT: ERROR")
            if self.wait_for_message("LCT: Blad"):
                self.log_message("Niedopuszczalna wartosc")
                return False
        else:
            return True

    def close(self):
        self.ser.close()
        if hasattr(self, 'log_file'):
            self.log_file.close()

    def create_log_file(self):
        # Ensure the log directory exists
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

        timestamp = time.strftime("%Y%m%d_%H%M%S")
        com_port = self.port

        log_filename = os.path.join(self.log_dir, f"serial_log{self.test_file_name}_{com_port}_{timestamp}.txt")
        return open(log_filename, 'a')

    def log_message(self, message):
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        milliseconds = int((time.time() % 1) * 1000)
        log_entry = f"{timestamp}.{milliseconds:03d} - {message}\n"
        self.log_file.write(log_entry)
        self.log_file.flush()  # Ensure the log entry is written to the file
