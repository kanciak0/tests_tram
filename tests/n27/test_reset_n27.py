import logging
import os
import random
import sys

import pytest

from common.Service import SerialService

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

@pytest.fixture(scope='module')
def serial_service(request):
    """
    Fixture to initialize and provide the SerialService instance for the tests.
    """
    config_file = request.config.getoption("--serial-config")
    service = SerialService(config_file=config_file)
    yield service
    service.ser.close()

def _generate_random_phone_number() -> str:
    """Generate a random 9-digit phone number."""
    return ''.join([str(random.randint(0, 9)) for _ in range(9)])

@pytest.mark.parametrize("reset_number", [1, 2, 3])
def test_set_reset_numbers(serial_service, reset_number):
    """
    Test to set random 9-digit phone numbers for reset numbers 1 to 3.

    :param serial_service: The serial_service instance used for interacting with the device.
    :param reset_number: The reset number to set (1, 2, or 3).
    """
    logging.info(f"Starting test_reset_numbers for reset_num {reset_number}")

    try:
        # Log in as admin before setting the reset number
        serial_service.login_admin()

        # Generate a random 9-digit phone number
        phone_number = _generate_random_phone_number()

        expected_message = f"reset_num{reset_number}={phone_number}"
        # Set the reset number with the generated phone number
        serial_service.reset_num(reset_number, phone_number)

        # Validate the setting (you can add custom validation here if needed)
        # For now, we assume the function works if no exception is raised
        logging.info(f"Successfully set reset_num {reset_number} to {phone_number}")
        serial_service.save()
        serial_service.reset()
        serial_service.wait_for_message("Modul radiowy poprawnie wykryty i zainicjowany")
        serial_service.login_admin()
        serial_service.write("print reset\n")


        # Check if the correct number is set by waiting for the confirmation message
        result = serial_service.wait_for_message(expected_message)


        assert result, f"Expected confirmation message '{expected_message}' not received."
        logging.info(f"Successfully verified reset_num {reset_number} is set to {phone_number}")

    except AssertionError as e:
        logging.error(f"Test failed: {e}")
        raise
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise


@pytest.mark.parametrize("autoreset_param", ["autoreset1", "autoreset2"])
def test_set_autoreset_times(serial_service, autoreset_param):
    """
    Test to set and verify autoreset1 and autoreset2 values.

    :param serial_service: The serial_service instance used for interacting with the device.
    :param autoreset_param: Either 'autoreset1' or 'autoreset2'.
    """
    logging.info(f"Starting test for {autoreset_param}")

    try:
        serial_service.login_admin()

        # Set the autoreset time to a random value (e.g., 'HH:MM')
        autoreset_time = f"{random.randint(0, 23):02}:{random.randint(0, 59):02}"

        expected_message = f"{autoreset_param}={autoreset_time}"
        serial_service.write(f"set {autoreset_param} {autoreset_time}\n")

        # Save and reset the device
        serial_service.save()
        serial_service.reset()
        serial_service.wait_for_message("Modul radiowy poprawnie wykryty i zainicjowany")
        serial_service.login_admin()

        # Verify that the autoreset time was set correctly
        serial_service.write("print auto\n")
        result = serial_service.wait_for_message(expected_message)

        assert result, f"Expected message '{expected_message}' not received."
        logging.info(f"Successfully verified {autoreset_param} is set to {autoreset_time}")

    except AssertionError as e:
        logging.error(f"Test failed: {e}")
        raise
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise
