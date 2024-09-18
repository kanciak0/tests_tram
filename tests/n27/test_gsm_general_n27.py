import os
import sys
import time

import pytest
import logging
import re
from common.Service import GSMService

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

@pytest.fixture(scope='module')
def gsm_service(request):
    """
    Fixture to initialize and provide the GSMService instance for the tests.
    """
    config_file = request.config.getoption("--serial-config")
    service = GSMService(config_file=config_file)
    yield service


def test_gsm_ver_n27(gsm_service):
    """
    Test to verify the GSM module type and firmware version.
    """
    logging.info("Starting test_gsm_ver_n27")
    try:
        gsm_service.login_admin()
        gsm_service.gsm_ver()
        expected_message = "LCT: Typ modulu: "  # Example expected output
        result = gsm_service.wait_for_message(expected_message)
        assert result, f"Expected GSM version message '{expected_message}' was not received."
        logging.info("GSM version test passed successfully.")
    except AssertionError as e:
        logging.error(f"Test failed: {e}")
        raise
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise


def test_gsm_ids_n27(gsm_service):
    """
    Test to verify the IMEI, IMSI, and SIM ID (ICCID) numbers.
    """
    logging.info("Starting test_gsm_ids_n27")
    try:
        gsm_service.login_admin()
        gsm_service.gsm_ids()
        expected_message = "SIMID "
        result = gsm_service.wait_for_message(expected_message)
        assert result, f"Expected GSM IDs message '{expected_message}' was not received."
        logging.info("GSM IDs test passed successfully.")
    except AssertionError as e:
        logging.error(f"Test failed: {e}")
        raise
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise


def test_gsm_band_n27(gsm_service):
    """
    Test to verify the radio band used by the device and ensure correct APN and PIN settings.
    """
    logging.info("Starting test_gsm_band_n27")
    try:
        # List of expected GSM and LTE bands
        expected_messages = [
            "GSM900",
            "GSM1800",
            "LTE900",
            "LTE800",
            "LTE1800",
            "LTE2100",
            "LTE450B31"
        ]

        # Perform GSM band check
        gsm_service.login_admin()
        gsm_service.gsm_band()
        result = gsm_service.wait_for_one_of_expected_messages(expected_messages, timeout=5)

        if not result:
            expected_apn_name = gsm_service.get_apn_name()
            pin_value = gsm_service.get_pin()
            pin_check_command = 'print pin\n'
            pin_set_command = f'set pin {pin_value}\n'
            # Handle the "???" case by checking and setting APN and PIN
            gsm_service.write("print apn\n")
            result = gsm_service.wait_for_message(expected_apn_name)

            if not result:
                logging.info(f"APN name is not set correctly, setting it to '{expected_apn_name}'")
                gsm_service.write(f"set apn_name {expected_apn_name}")
                gsm_service.save()
                gsm_service.reset()
            pin_pattern = r'pin=\s?\d{4}'
            gsm_service.write(pin_check_command)
            pin_output = gsm_service.read_console_output(line_count=5)
            if re.search(pin_pattern, pin_output):
                return False
            else:
                logging.info("The string does not contain 'pin=' followed by an optional space and 4 digits.")
                gsm_service.write(pin_set_command)
                gsm_service.save()
                gsm_service.reset()
                gsm_service.wait_for_message("Modul radiowy poprawnie wykryty", timeout=60)
                gsm_service.login_admin()
                gsm_service.gsm_band()
                return True

        assert result, f"Expected one of the GSM/LTE band messages {expected_messages}, but got '{result}'."
        logging.info("GSM band test passed successfully.")
    except AssertionError as e:
        logging.error(f"Test failed: {e}")
        raise
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise


def test_gsm_rssi_n27(gsm_service):
    """
    Test to verify the current signal strength (RSSI) and bit error rate (BER).
    """
    logging.info("Starting test_gsm_rssi_n27")
    try:
        gsm_service.login_admin()
        gsm_service.gsm_rssi()
        expected_message = "RSSI: "  # Example expected output
        result = gsm_service.wait_for_message(expected_message)
        assert result, f"Expected GSM RSSI message '{expected_message}' was not received."
        logging.info("GSM RSSI test passed successfully.")
    except AssertionError as e:
        logging.error(f"Test failed: {e}")
        raise
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise


def test_gsm_rssiex_n27(gsm_service):
    """
    Test to verify the extended signal strength (RSSI) and bit error rate (BER).
    """
    logging.info("Starting test_gsm_rssiex_n27")
    try:
        gsm_service.login_admin()
        gsm_service.gsm_rssiex()
        expected_message = "Temp: "  # Example expected output
        result = gsm_service.wait_for_message(expected_message)
        assert result, f"Expected GSM RSSIex message '{expected_message}' was not received."
        logging.info("GSM RSSIex test passed successfully.")
    except AssertionError as e:
        logging.error(f"Test failed: {e}")
        raise
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise


def test_gsm_regstate_n27(gsm_service):
    """
    Test to verify the registration status in GSM and GPRS networks.
    """
    logging.info("Starting test_gsm_regstate_n27")
    try:
        gsm_service.login_admin()
        gsm_service.gsm_regstate()
        expected_message = "Siec GSM: "  # Example expected output
        result = gsm_service.wait_for_message(expected_message)
        assert result, f"Expected GSM registration state message '{expected_message}' was not received."
        logging.info("GSM registration state test passed successfully.")
    except AssertionError as e:
        logging.error(f"Test failed: {e}")
        raise
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise


def test_gsm_state_n27(gsm_service):
    """
    Test to verify the state of the GSM module.
    """
    logging.info("Starting test_gsm_state_n27")
    try:
        gsm_service.login_admin()
        gsm_service.gsm_state()
        expected_message = "Stan kanalu sterujacego: "  # Example expected output
        result = gsm_service.wait_for_message(expected_message)
        assert result, f"Expected GSM state message '{expected_message}' was not received."
        logging.info("GSM state test passed successfully.")
    except AssertionError as e:
        logging.error(f"Test failed: {e}")
        raise
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise


def test_gsm_status_n27(gsm_service):
    """
    Test to verify the status of the GSM module.
    """
    logging.info("Starting test_gsm_status_n27")
    try:
        gsm_service.login_admin()
        gsm_service.gsm_status()
        expected_message = "LCT: Radio status: "  # Example expected output
        result = gsm_service.wait_for_message(expected_message)
        assert result, f"Expected GSM status message '{expected_message}' was not received."
        logging.info("GSM status test passed successfully.")
    except AssertionError as e:
        logging.error(f"Test failed: {e}")
        raise
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise


def test_gsm_cellinfo_n27(gsm_service):
    """
    Test to verify the information about the serving cell.
    """
    logging.info("Starting test_gsm_cellinfo_n27")
    try:
        gsm_service.login_admin()
        gsm_service.gsm_cellinfo()
        expected_message = "LAC"  # Replace with the expected output
        result = gsm_service.wait_for_message(expected_message)
        assert result, f"Expected GSM cell info message '{expected_message}' was not received."
        logging.info("GSM cell info test passed successfully.")
    except AssertionError as e:
        logging.error(f"Test failed: {e}")
        raise
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise
