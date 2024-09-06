import os
import time

from common.communicator import SerialCommunicator

#TODO: SEPERATE CLASSES INTO DIFFERENT FILES
#TODO: Get everything from config


class SerialService(SerialCommunicator):
    def __init__(self, config_file='config_file.txt'):
        """
        Initialize the SerialService with the given configuration file.

        Args:
            config_file (str): Path to the configuration file.
        """
        super().__init__(config_file)

    def login_admin(self):
        if self.is_debug_mode():
            return False
        self.write('login\n')
        time.sleep(0.1)
        self.write(f'{self.password}\r\n')

        if self.wait_for_message("LCT: OK logged in"):
            print("Login: OK")
            return True
        else:
            print("Login: ERROR")
            return False

    def logout(self):
        self.write('logout\n')
        time.sleep(0.1)
        if self.wait_for_message("user >"):
            print("Logout: OK")
        else:
            print("Logout: ERROR")
            exit()

    def ver(self):
        self.write("ver\n")

    def verex(self):
        self.write("verex\n")

    def hwver(self):
        self.write("hwver\n")

    def urc_with_parameters(self, urc_value):
        self.write(f"urc {urc_value}\n")

    def config_info(self):
        self.write("config.info\n")

    def urc_without_parameters(self):
        self.write("urc\n")

    def board_serial_show(self):
        self.write("board.serial.show\n")

    def passwd(self):
        self.write('passwd\n')
        time.sleep(0.1)

    def defaults(self):
        self.write('defaults\n')
        time.sleep(0.1)

    def config_start(self):
        self.write("config.start\n")
        if self.wait_for_message("CONFIG: OK"):
            print("CONFIG: OK")
            return True
        else:
            print("CONFIG: ERROR")
            return False

    def gsm_ver(self):
        self.write("gsm.ver\n")

    def save(self):
        self.write('save\r\n')
        if self.wait_for_message("LCT: OK"):
            print("Zapis: OK")

    def reset(self):
        self.write('reset\r\n')
        if self.wait_for_message("Restart w ciagu 3 s"):
            print("Restart: PENDING")
        else:
            if self.wait_for_message("Wlaczanie modulu radiowego", timeout=180):
                print("Restart: OK")
            else:
                print("Restart: ERROR")
                exit()

    def set_active_radio(self, radio_id):
        """
        Set the active radio by specifying the radio ID.
        Radio ID can be 1 for radio N27 or 2 for radio N717.
        """
        if radio_id == 1:
            self.write('set active_radio 1\n')
        elif radio_id == 2:
            self.write('set active_radio 2\n')
        else:
            print(f"Invalid radio ID: {radio_id}. Valid IDs are 1 or 2.")
            return

    def rtc_print(self):
        self.write("rtc.print\n")

    def rtc_print2(self):
        self.write("rtc.print2\n")

    def rtc_print_utc(self):
        self.write("rtc.print.utc\n")

    def rtc_set_time(self, time_value):
        self.write(f"rtc.set.time {time_value}\n")

    def rtc_set_date(self, date_value):
        self.write(f"rtc.set.date {date_value}\n")

    def restart_disable(self, duration):
        self.write(f"restart.disable {duration}\n")

    def restore_configuration(self, config_file='backup_logs/backup_config.txt'):
        """
        Restore the configuration from the given file to the serial device.
        """
        with open(config_file, 'r') as file:
            config_lines = file.readlines()

        # Process each line in the configuration file
        for line in config_lines:
            # Strip leading and trailing whitespace
            line = line.strip()

            # Skip lines that are not in 'key=value' format or are empty
            if not line or '=' not in line:
                continue

            # Extract key and value from the line
            key, value = line.split('=', 1)

            # Remove leading and trailing spaces
            key = key.strip()
            value = value.strip()

            # Format the command based on the key
            command = None
            if key.startswith('apn_'):
                # Handle APN parameters
                if key == 'apn_name':
                    command = f"set apn_name {value}\n"
                    time.sleep(0.1)
                elif key == 'apn_login':
                    command = f"set apn_login {value}\n"
                    time.sleep(0.1)
                elif key == 'apn_passwd':
                    command = f"set apn_passwd {value}\n"
                    time.sleep(0.1)
                elif key == 'apn_auth':
                    command = f"set apn_auth {value}\n"
                    time.sleep(0.1)
                elif key == 'apn_tries':
                    command = f"set apn_tries {value}\n"
                    time.sleep(0.1)
            elif key.startswith('lwm2m_'):
                # Handle LWM2M parameters
                if key == 'lwm2m_uri':
                    command = f"set lwm2m_uri {value}\n"
                    time.sleep(0.1)
                elif key == 'lwm2m_client_port':
                    command = f"set lwm2m_client_port {value}\n"
                    time.sleep(0.1)
                elif key == 'lwm2m_coap_block_size':
                    command = f"set lwm2m_coap_block_size {value}\n"
                    time.sleep(0.1)
                elif key == 'lwm2m_lifetime':
                    command = f"set lwm2m_lifetime {value}\n"
                    time.sleep(0.1)
                elif key == 'lwm2m_bootstrap':
                    command = f"set lwm2m_bootstrap {value}\n"
                    time.sleep(0.1)
                elif key == 'lwm2m_reconnect':
                    command = f"set lwm2m_reconnect {value}\n"
                    time.sleep(0.1)
                elif key == 'lwm2m_psk_id':
                    command = f"set lwm2m_psk_id {value}\n"
                    time.sleep(0.1)
                elif key == 'lwm2m_psk_key':
                    command = f"set lwm2m_psk_key {value}\n"
                    time.sleep(0.1)
            elif key.startswith(('rtc_', 'timesync_', 'autoreset_')):
                # Handle RTC, time sync, and auto-reset parameters
                command = f"set {key} {value}\n"
            elif key.startswith(('allowed_ip', 'tcp_session_tout', 'icmp_server', 'test_server_ip',
                                 'test_server_ip2', 'test_failure_action', 'testing_interval',
                                 'lct_tcp_port', 'ntp_server_ip', 'ntp_backup_server_ip',
                                 'ntp_sync_interval', 'ntp_sync_time', 'uplink1')):
                # Handle IP, TCP, ICMP, test server, and other network-related parameters
                command = f"set {key} {value}\n"
                time.sleep(0.1)
            elif key.startswith(('avail_bands', 'conf_bands', 'pref_bands', 'pref_bands_cur',
                                 'test_ping_size', 'test_ping_count', 'test_ping_tout',
                                 'test_ping_ratio', 'test_ping_delay')):
                # Handle bands and test parameters
                command = f"set {key} {value}\n"
                time.sleep(0.1)
            elif key.startswith('cell_lock'):
                # Handle cell lock parameters
                command = f"set {key} {value}\n"
                time.sleep(0.1)
            elif key in ['active_radio', 'pin', 'puk', 'reset_num1', 'reset_num2', 'reset_num3',
                         'radio_mode', 'network_searching_tout', 'radio_mode_auto_delay',
                         'radio_mode_pref', 'radio_mode_rssi_low', 'timesync1', 'timesync2',
                         'time_synchronized']:
                # Handle additional parameters
                command = f"set {key} {value}\n"
                time.sleep(0.1)
            elif key.startswith('autoreset_'):
                # Handle autoreset parameters
                command = f"set {key} {value}\n"
            else:
                print(f"Unrecognized key: {key}")

            # Send the command if it's recognized
            if command:
                self.ser.write(command.encode())  # Encode the command to bytes

        # Optionally, send a command to save the configuration
        self.ser.write('save\n'.encode())  # Encode 'save' to bytes
        print("Configuration restored and saved.")
        self.ser.write('reset\n'.encode())
        time.sleep(20)
        os.remove(config_file)
        print(f"Configuration file {config_file} deleted.")

class GSMService(SerialService):
    def __init__(self, config_file='config_file.txt'):
        super().__init__(config_file)


    def gsm_regstate(self):
        self.write("gsm.regstate\n")

    def gsm_rssi(self):
        self.write("gsm.rssi\n")

    def gsm_rssiex(self):
        self.write("gsm.rssiex\n")

    def gsm_ids(self):
        self.write("gsm.ids\n")

    def gsm_band(self):
        self.write("gsm.band\n")

    def gsm_aux_ati(self):
        self.write("gsm.aux ati\n")

    def gsm_ctrl(self):
        self.write("gsm.ctrl\n")

    def gsm_state(self):
        self.write("gsm.state\n")

    def gsm_status(self):
        self.write("gsm.status\n")

    def gsm_cellinfo(self):
        self.write("gsm.cellinfo\n")

    def gsm_rat(self):
        self.write("gsm.rat\n")

    def gsm_signal(self):
        self.write("gsm.signal\n")

    def gsm_at_cops(self):
        self.write("gsm.aux at+cops?\n")

    def gsm_at_creg(self):
        self.write("gsm.aux at+creg?\n")


class APNService(SerialService):
    def __init__(self, config_file='config_file.txt'):
        super().__init__(config_file)

    def set_apn_name(self, apn_name):
        self.write(f"set apn_name {apn_name}\n")

    def set_apn_login(self, apn_login):
        self.write(f"set apn_login {apn_login}\n")

    def set_apn_passwd(self, apn_passwd):
        self.write(f"set apn_passwd {apn_passwd}\n")

    def set_apn_auth(self, apn_auth):
        self.write(f"set apn_auth {apn_auth}\n")

    def set_apn_tries(self, apn_tries):
        self.write(f"set apn_tries {apn_tries}\n")

    def print_apn(self):
        self.write("print apn\n")


class LWM2MService(SerialService):
    def __init__(self, config_file='config_file.txt'):
        super().__init__(config_file)

    def lwm2m_status(self):
        self.write('lwm2m.status\n')

    def set_lwm2m_uri(self,lwm2m_uri):
        self.write(f'set lwm2m_uri {lwm2m_uri}\n')
        time.sleep(0.1)

    def set_lwm2m_bootstrap(self, lwm2m_bootstrap):
        self.write(f'set lwm2m_bootstrap {lwm2m_bootstrap}\n')
        time.sleep(0.1)

    def set_lwm2m_lifetime(self, lwm2m_lifetime):
        self.write(f'set lwm2m_lifetime {lwm2m_lifetime}\n')
        time.sleep(0.1)

    def set_lwm2m_client_port(self,lwm2m_client_port):
        self.write(f'set lwm2m_client_port {lwm2m_client_port}\n')
        time.sleep(0.1)

    def set_lwm2m_psk_id(self,lwm2m_psk_id):
        self.write(f'set lwm2m_psk_id {lwm2m_psk_id}\n')
        time.sleep(0.1)

    def set_lwm2m_psk_key(self,lwm2m_psk_key):
        self.write(f'set lwm2m_psk_key {lwm2m_psk_key}\n')
        time.sleep(0.1)

    def lwm2m_reconnect(self):
        self.write("lwm2m.reconnect\n")


class MockService(SerialService):
    def __init__(self, config_file='config_file.txt'):
        super().__init__(config_file)

    def mock_set_radio_mode(self,radio_id):
        self.write(f"set radio_mode {radio_id}\n")

    def mock_set_active_radio(self,radio_id):
        self.write(f"set active_radio {radio_id}\n")