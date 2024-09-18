import os
import sys

import pytest
import logging
from common.Service import APNService

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S %F')

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

@pytest.fixture(scope='module')
def apn_service(request):
    """
    Fixture to initialize and provide the SerialService instance for the tests.
    """
    config_file = request.config.getoption("--serial-config")
    apn_service = APNService(config_file=config_file)
    yield apn_service
    apn_service.ser.close()

# @pytest.fixture(scope='module')
# def gsm_service():
#     gsm_service = GSMService(config_file='config.txt')
#     yield gsm_service
#     gsm_service.close()



logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

# Global fixture that runs once at the start of the session


@pytest.fixture(scope='module', autouse=True)
def backup_log_configuration(apn_service, request):
    """
    This fixture captures and backs up the configuration to a file at the beginning of the session.
    """
    # Set up logging
    log_dir = 'backup_logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Create a backup file
    backup_file_path = os.path.join(log_dir, 'backup_config.txt')

    # Get configuration from the APN service
    try:
        # Log in as admin
        apn_service.login_admin()

        # Write command to get the configuration
        apn_service.write('print\n')

        # Capture the output with 76 lines as expected
        configuration_data = apn_service.read_console_output(line_count=72)

        # Process the configuration data
        processed_data = process_configuration_data(configuration_data)

        # Log the processed configuration data to the backup file
        with open(backup_file_path, 'w') as backup_file:
            backup_file.write(
                "-------------------------- Saved current configuration -----------------------------------\n")
            backup_file.write(processed_data)

        # Log success to the console
        logging.info(f"Configuration saved to backup file: {backup_file_path}")

    except Exception as e:
        logging.error(f"Failed to save configuration: {e}")
        raise  # Re-raise the exception to ensure pytest reports the failure


def process_configuration_data(data):
    """
    Processes the configuration data by removing whitespaces and 'LCT:' prefixes.
    """
    lines = data.splitlines()
    processed_lines = []

    for line in lines:
        # Remove leading and trailing whitespaces
        line = line.strip()

        # Remove 'LCT:' prefix
        if line.startswith('LCT:'):
            line = line[4:].strip()

        # Add the processed line to the list
        processed_lines.append(line)

    return '\n'.join(processed_lines)


@pytest.fixture(scope="module", autouse=True)
def radio_setup_n27(apn_service):
    """
    Fixture to ensure the radio module N27 is active and properly initialized.
    """
    apn_service.login_admin()
    apn_service.gsm_ver()
    expected_radio = apn_service.wait_for_message("N27",timeout=5)
    if expected_radio is False:
        apn_service.set_active_radio(radio_id=1)
        apn_service.save()
        apn_service.reset()
        apn_service.wait_for_message("Modul radiowy poprawnie wykryty i zainicjowany")
        apn_service.login_admin()
        apn_service.gsm_ver()
        expected_radio = apn_service.wait_for_message("N27")
        if expected_radio is False:
            pytest.fail("Nie przelaczono na poprawny modul radiowy")
    yield


def test_set_apn_name_n27(apn_service):
    """
    Test to verify setting and retrieving the APN name.
    """
    logging.info("Starting test_set_apn_name")
    try:
        apn_service.login_admin()
        apn_name = apn_service.get_apn_name()
        apn_service.set_apn_name(apn_name)

        # Verify the APN name was set correctly
        apn_service.print_apn()
        expected_message = f"apn_name={apn_name}"

        result = apn_service.wait_for_message(expected_message)
        assert result, f"Expected APN name '{expected_message}' was not received."

        logging.info("APN name test passed successfully.")

    except AssertionError as e:
        logging.error(f"Test failed: {e}")
        raise  # Re-raise the exception to ensure pytest reports the failure
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise  # Re-raise the exception to ensure pytest reports the failure


def test_set_apn_login_n27(apn_service):
    """
    Test to verify setting and retrieving the APN login.
    """
    logging.info("Starting test_set_apn_login")
    try:
        apn_service.login_admin()
        apn_login = "ppp"
        assert len(apn_login) <= 32, "APN login exceeds maximum length"
        apn_service.set_apn_login(apn_login)

        # Verify the APN login was set correctly
        apn_service.print_apn()
        expected_message = f"apn_login={apn_login}"

        result = apn_service.wait_for_message(expected_message)
        assert result, f"Expected APN login '{expected_message}' was not received."

        logging.info("APN login test passed successfully.")

    except AssertionError as e:
        logging.error(f"Test failed: {e}")
        raise  # Re-raise the exception to ensure pytest reports the failure
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise  # Re-raise the exception to ensure pytest reports the failure


def test_set_apn_password_n27(apn_service):
    """
    Test to verify setting and retrieving the APN password.
    """
    logging.info("Starting test_set_apn_password")
    try:
        apn_service.login_admin()
        apn_passwd = "ppp"
        assert len(apn_passwd) <= 32, "APN password exceeds maximum length"
        apn_service.set_apn_passwd(apn_passwd)

        # Verify the APN password was set correctly
        apn_service.print_apn()
        expected_message = f"apn_passwd={apn_passwd}"

        result = apn_service.wait_for_message(expected_message)
        assert result, f"Expected APN password '{expected_message}' was not received."

        logging.info("APN password test passed successfully.")

    except AssertionError as e:
        logging.error(f"Test failed: {e}")
        raise  # Re-raise the exception to ensure pytest reports the failure
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise  # Re-raise the exception to ensure pytest reports the failure


def test_set_apn_auth_n27(apn_service):
    """
    Test to verify setting and retrieving the APN authentication method.
    """
    logging.info("Starting test_set_apn_auth")
    try:
        apn_service.login_admin()
        apn_auth = "pap"
        valid_auth_methods = ["pap", "chap", "none"]
        assert apn_auth in valid_auth_methods, f"APN auth '{apn_auth}' is not valid"
        assert len(apn_auth) <= 16, "APN auth method exceeds maximum length"
        apn_service.set_apn_auth(apn_auth)

        # Verify the APN authentication method was set correctly
        apn_service.print_apn()
        expected_message = f"apn_auth={apn_auth}"

        result = apn_service.wait_for_message(expected_message)
        assert result, f"Expected APN authentication method '{expected_message}' was not received."

        logging.info("APN authentication method test passed successfully.")

    except AssertionError as e:
        logging.error(f"Test failed: {e}")
        raise  # Re-raise the exception to ensure pytest reports the failure
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise  # Re-raise the exception to ensure pytest reports the failure


def test_set_apn_tries_n27(apn_service):
    """
    Test to verify setting and retrieving the APN tries parameter.
    """
    logging.info("Starting test_set_apn_tries")
    try:
        apn_service.login_admin()
        apn_tries = 8

        assert 4 <= apn_tries <= 360, "APN tries value must be between 4 and 360"

        apn_service.set_apn_tries(apn_tries)

        # Verify the APN tries parameter was set correctly
        apn_service.print_apn()
        expected_message = f"apn_tries={apn_tries}"

        result = apn_service.wait_for_message(expected_message)
        assert result, f"Expected APN tries parameter '{expected_message}' was not received."

        logging.info("APN tries parameter test passed successfully.")

    except AssertionError as e:
        logging.error(f"Test failed: {e}")
        raise  # Re-raise the exception to ensure pytest reports the failure
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise  # Re-raise the exception to ensure pytest reports the failure


