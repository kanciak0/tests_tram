import os
import sys

import pytest
import logging

from common.Service import SerialService

# Configure logging with timestamps to milliseconds
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

@pytest.fixture(scope="module", autouse=True)
def radio_setup_n717(apn_service):
    apn_service.login_admin()
    apn_service.gsm_ver()
    expected_radio = apn_service.wait_for_message("717",timeout=5)
    if expected_radio is False:
        apn_service.set_active_radio(radio_id=2)
        apn_service.save()
        apn_service.reset()
        apn_service.wait_for_message("Modul radiowy poprawnie wykryty")
        apn_service.login_admin()
        apn_service.gsm_ver()
        expected_radio = apn_service.wait_for_message("N717")
        if expected_radio is False:
            pytest.fail("Nie przelaczono na poprawny modul radiowy")
    yield
    apn_service.save()
    apn_service.reset()
    apn_service.wait_for_message("Modul radiowy poprawnie wykryty i zainicjowany")

@pytest.fixture(scope='module')
def serial_service(request):
    """
    Fixture to initialize and provide the SerialService instance for the tests.
    """
    config_file = request.config.getoption("--serial-config")
    service = SerialService(config_file=config_file)
    yield service
    service.ser.close()


@pytest.mark.skip("Configuration not working")
def test_uplink1_rs485_customn717(serial_service):
    """
    Test to verify the uplink1 configuration with RS485 and custom settings.
    """
    logging.info("Starting test_uplink1_rs485_custom_n27")
    try:
        serial_service.login_admin()

        # Set the uplink1 configuration
        uplink = "rs485:7E1:1200,srv,tcp:8500,apap-bin"
        serial_service.write(f"set uplink1 {uplink}\n")

        serial_service.save()
        serial_service.reset()

        # Wait for the restart or configuration to take effect
        expected_message = "Modem restarted"
        result = serial_service.wait_for_message(expected_message)

        assert result, f"Expected message '{expected_message}' was not received."

        # Verify the configuration
        serial_service.write("print uplink\n")
        response = serial_service.wait_for_message(uplink)

        assert response, f"Uplink1 configuration mismatch or not set correctly. Expected: {uplink}"

        logging.info("Uplink1 configuration with RS485 and custom settings completed successfully.")
    except AssertionError as e:
        logging.error(f"Test failed: {e}")
        raise
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise


def test_uplink1_rs232_custom_speed_n717(serial_service):
    """
    Test to verify the uplink1 configuration with RS232 and custom initial speed.
    """
    logging.info("Starting test_uplink1_rs232_custom_speed_n717")
    try:
        serial_service.login_admin()

        # Set the uplink1 configuration
        uplink = "rs232:8e1:2400,srv,tcp:8500,apap-bin"
        serial_service.write(f"set uplink1 {uplink}\n")

        serial_service.save()
        serial_service.reset()

        serial_service.wait_for_message("Modul radiowy poprawnie wykryty i zainicjowany")
        serial_service.login_admin()

        serial_service.write("print uplink\n")
        response = serial_service.wait_for_message(uplink)

        assert response, f"Uplink1 configuration mismatch or not set correctly. Expected: {uplink}"

        logging.info("Uplink1 configuration with RS232 and custom speed completed successfully.")
    except AssertionError as e:
        logging.error(f"Test failed: {e}")
        raise
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise


def test_uplink1_rs232_custom_framing_n717(serial_service):
    """
    Test to verify the uplink1 configuration with RS232 and custom framing.
    """
    logging.info("Starting test_uplink1_rs232_custom_framing_n717")
    try:
        serial_service.login_admin()

        # Set the uplink1 configuration
        uplink = "rs232:8E1,srv,tcp:8500,apap-bin"
        serial_service.write(f"set uplink1 {uplink}\n")

        serial_service.save()
        serial_service.reset()

        serial_service.wait_for_message("Modul radiowy poprawnie wykryty i zainicjowany")
        serial_service.login_admin()

        serial_service.write("print uplink\n")
        response = serial_service.wait_for_message(uplink)

        assert response, "Uplink1 configuration mismatch or not set correctly."

        logging.info("Uplink1 configuration with RS232 and custom framing completed successfully.")
    except AssertionError as e:
        logging.error(f"Test failed: {e}")
        raise
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise
