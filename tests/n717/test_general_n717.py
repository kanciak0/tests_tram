import logging
import os
import sys

import pytest
from common.Service import SerialService
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

@pytest.fixture(scope='module')
def serial_service(request):
    """
    Fixture to initialize and provide the SerialService instance for the tests.
    """
    config_file = request.config.getoption("--serial-config")
    service = SerialService(config_file=config_file)
    yield service


def test_ver_n717(serial_service):
    """
    Test to verify the version information of the TRAM device.
    """
    logging.info("Starting test_ver_n717")
    try:
        serial_service.ver()
        expected_message = "LCT: TRAM APATOR, version"
        result = serial_service.wait_for_message(expected_message)
        assert result, f"Expected version message '{expected_message}' was not received."
        logging.info("Version information test passed successfully.")
    except AssertionError as e:
        logging.error(f"Test failed: {e}")
        raise
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise


def test_hwver_n717(serial_service):
    """
    Test to verify the hardware version information of the TRAM device.
    """
    logging.info("Starting test_hwver_n717")
    try:
        serial_service.hwver()
        expected_message = "TRAM v"
        result = serial_service.wait_for_message(expected_message)
        assert result, f"Expected hardware version message '{expected_message}' was not received."
        logging.info("Hardware version test passed successfully.")
    except AssertionError as e:
        logging.error(f"Test failed: {e}")
        raise
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise


@pytest.mark.parametrize("urc_value, expected_message", [
    (1, "URC: 1"),
    (0, "URC: 0")
])
def test_urc_with_parameters_n717(serial_service, urc_value, expected_message):
    """
    Test to verify the URC (Unsolicited Result Code) response with parameters.
    """
    logging.info(f"Starting test_urc_with_parameters_n717 with URC value {urc_value}")
    try:
        serial_service.login_admin()
        serial_service.urc_with_parameters(urc_value)
        result = serial_service.wait_for_message(expected_message)
        assert result, f"Expected URC response message '{expected_message}' was not received."
        logging.info("URC with parameters test passed successfully.")
    except AssertionError as e:
        logging.error(f"Test failed: {e}")
        raise
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise


def test_config_info_n717(serial_service):
    """
    Test to retrieve and verify configuration information from the TRAM device.
    """
    logging.info("Starting test_config_info_n717")
    try:
        serial_service.login_admin()
        serial_service.config_info()
        expected_message = "config"
        result = serial_service.wait_for_message(expected_message)
        assert result, f"Expected configuration info message '{expected_message}' was not received."
        logging.info("Configuration info test passed successfully.")
    except AssertionError as e:
        logging.error(f"Test failed: {e}")
        raise
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise


def test_urc_without_parameters_n717(serial_service):
    """
    Test to verify the URC (Unsolicited Result Code) response without parameters.
    """
    logging.info("Starting test_urc_without_parameters_n717")
    try:
        serial_service.urc_without_parameters()
        expected_message = "URC: "
        result = serial_service.wait_for_message(expected_message)
        assert result, f"Expected URC response message '{expected_message}' was not received."
        logging.info("URC without parameters test passed successfully.")
    except AssertionError as e:
        logging.error(f"Test failed: {e}")
        raise
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise


def test_board_serial_show_n717(serial_service):
    """
    Test to display and verify the board serial number of the TRAM device.
    """
    logging.info("Starting test_board_serial_show_n717")
    try:
        serial_service.login_admin()
        serial_service.board_serial_show()
        expected_message = "BOARD SERIAL"
        result = serial_service.wait_for_message(expected_message)
        assert result, f"Expected board serial message '{expected_message}' was not received."
        logging.info("Board serial number test passed successfully.")
    except AssertionError as e:
        logging.error(f"Test failed: {e}")
        raise
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise
