import re
import logging
import pytest

from common.Service import GSMService

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


@pytest.fixture(scope='module')
def gsm_service(request):
    """
    Fixture to initialize and provide the GSMService instance for the tests.
    """
    config_file = request.config.getoption("--serial-config")
    service = GSMService(config_file=config_file)
    yield service
    service.ser.close()


@pytest.fixture(scope='module')
def gsm_setup(gsm_service):
    """
    Fixture to perform the setup for GSM service. This includes:
    - Logging in as admin
    - Verifying GSM service
    - Configuring GSM service if necessary
    - Checking and setting PIN if required
    """

    # Log in as admin and verify GSM service
    gsm_service.login_admin()
    gsm_service.gsm_ver()

    # Check for expected message and configure GSM service if necessary
    if not gsm_service.wait_for_message("N717", timeout=3):
        logging.info("Configuring GSM service")
        gsm_service.set_active_radio(2)
        gsm_service.wait_for_message("LCT: OK")
        gsm_service.save()
        gsm_service.reset()
        gsm_service.wait_for_message(
            "Modul radiowy poprawnie wykryty i zainicjowany", timeout=30
        )
        gsm_service.login_admin()

    # Verify GSM state
    gsm_service.gsm_state()
    status_message = gsm_service.read().strip()

    try:
        status_value = int(status_message.split(":")[1].split("[")[0].strip())
        gsm_service.restart_disable(3600)

        if status_value <= 3:
            logging.info("PIN handling is required for GSM setup")
            pin_value = gsm_service.get_pin()
            pin_check_command = 'print pin\n'
            pin_set_command = f'set pin {pin_value}\n'
            pin_pattern = r'pin=\s?\d{4}'
            gsm_service.write(pin_check_command)
            pin_output = gsm_service.read_console_output(line_count=5)

            if re.search(pin_pattern, pin_output):
                logging.info("PIN is already set.")
                return False
            else:
                logging.info("Setting PIN for GSM service")
                gsm_service.write(pin_set_command)
                gsm_service.save()
                gsm_service.reset()
                gsm_service.wait_for_message("Modul radiowy poprawnie wykryty", timeout=60)
                return True
    except (ValueError, IndexError):
        logging.error("Failed to retrieve a valid GSM status.")
        pytest.skip("Failed to retrieve a valid GSM status.")

    # Wait for operator information
    gsm_service.wait_for_message("INF: Operator sieci:", timeout=150)

    logging.info("GSM setup fixture completed")
    yield


def test_gsm_at_cops(gsm_service, gsm_setup):
    """
    Test to verify the +COPS command for the GSM service.
    """
    logging.info("Starting test_gsm_at_cops")

    try:
        gsm_service.login_admin()
        expected_message = "+COPS: 0,"
        gsm_service.gsm_at_cops()
        result = gsm_service.wait_for_message(expected_message, timeout=10)

        assert result, f"Expected board serial message '{expected_message}' was not received."
        logging.info("GSM AT +COPS test passed successfully.")
    except AssertionError as e:
        logging.error(f"Test failed: {e}")
        raise
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise


def test_gsm_ati(gsm_service, gsm_setup):
    """
    Test to verify the ATI command for the GSM service.
    """
    logging.info("Starting test_gsm_ati")

    try:
        gsm_service.login_admin()
        expected_message = "V0"
        gsm_service.gsm_aux_ati()
        result = gsm_service.wait_for_message(expected_message, timeout=5)

        assert result, f"Expected board model to be '{expected_message}' was not received."
        logging.info("GSM ATI test passed successfully.")
    except AssertionError as e:
        logging.error(f"Test failed: {e}")
        raise
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise


def test_gsm_at():
    """
    Placeholder for additional GSM AT command tests.
    """
    logging.info("Starting test_gsm_at (placeholder)")
    pass


def test_gsm_at_creg(gsm_service, gsm_setup):
    """
    Test to verify the +CREG command for the GSM service.
    """
    logging.info("Starting test_gsm_at_creg")

    try:
        gsm_service.login_admin()
        expected_message = "2,"
        gsm_service.gsm_at_creg()
        result = gsm_service.wait_for_message(expected_message, timeout=5)

        assert result, f"Expected network registration status '{expected_message}' was not received."
        logging.info("GSM +CREG test passed successfully.")
    except AssertionError as e:
        logging.error(f"Test failed: {e}")
        raise
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise
