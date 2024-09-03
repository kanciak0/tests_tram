import serial
import time
import configparser


class SerialCommunicator:
    def __init__(self, config_file='config_file.txt'):
        config = configparser.ConfigParser()
        config.read(config_file)

        # Ensure the section 'serial' exists
        if not config.has_section('serial'):
            raise configparser.NoSectionError('serial')

        self.port = config.get('serial', 'port')
        self.baudrate = config.getint('serial', 'baudrate')
        self.timeout = config.getfloat('serial', 'timeout')
        self.password = config.get('serial', 'password')

        self.ser = serial.Serial(self.port, baudrate=self.baudrate, timeout=self.timeout)


    def write(self, command):
        self.ser.write(command.encode())
        time.sleep(0.1)

    def read(self):
        return self.ser.read(self.ser.in_waiting or 1).decode('utf-8').strip()

    def send_command_and_wait(self, command, expected_message, timeout=30):
        self.write(command)
        return self.wait_for_message(expected_message, timeout)

    def wait_for_message(self, expected_message, timeout=45):
        start_time = time.time()
        buffer = ""

        while True:
            if time.time() - start_time > timeout:
                print("Timeout waiting for message.")
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
            # Check if the timeout has been exceeded
            if time.time() - start_time > timeout:
                print("Timeout waiting for messages.")
                return False

            # If data is available in the serial buffer, read it and add it to the buffer string
            if self.ser.in_waiting > 0:
                data = self.read()
                buffer += data

                # Check if any of the expected messages are present in the buffer
                for message in expected_messages:
                    if message in buffer:
                        return True

    def is_debug_mode(self):
        self.ser.write(b'\n\r')
        if not self.wait_for_message("debug >",3):
            return False
        else:
            return True

    def read_console_output(self, line_count=5, timeout=5):
        """
        Reads a specified number of lines from the console output.

        :param line_count: Number of lines to read from the console output.
        :param timeout: Time in seconds to wait for data to be available.
        :return: String containing the console output.
        """
        output = ""
        end_time = time.time() + timeout

        while time.time() < end_time:
            if self.ser.in_waiting > 0:
                # Read data from the serial port
                data = self.ser.read(self.ser.in_waiting).decode('utf-8')
                output += data

                # Check if we have enough lines
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

        print(f"Timeout: '{expected_message}' not received within {timeout} seconds.")
        return ""

    @staticmethod
    def get_value_from_response(response, start_index):
        return response[start_index:].strip()

    def check_lct(self):
        if not self.wait_for_message("LCT: OK"):
            print("LCT: ERROR")
            if self.wait_for_message("LCT: Blad"):
                print("Niedopuszczalna wartosc")
                return False
        else:
            return True

    def close(self):
        self.ser.close()
