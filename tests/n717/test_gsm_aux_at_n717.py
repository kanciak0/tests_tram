import re

import pytest

from common.Service import GSMService


@pytest.fixture(scope='module')
def gsm_service(request):
    """
    Fixture to initialize and provide the GSMService instance for the tests.
    """
    config_file = request.config.getoption("--serial-config")
    service = GSMService(config_file=config_file,test_file_name="log_test_gsm_aux_at_n717")
    yield service
    service.close()


@pytest.fixture(scope='module')
def gsm_setup(gsm_service):
    """
    Fixture to perform the setup for GSM service. This includes:
    - Logging in as admin
    - Verifying GSM service
    - Configuring GSM service if necessary
    - Checking and setting PIN if required

    Steps:
    1. Log in as admin and verify GSM service.
    2. Check for the expected message. If not received, configure the GSM service.
    3. Verify GSM state and handle PIN configuration if the status requires it.
    """
    # Log in as admin and verify GSM service
    gsm_service.login_admin()
    gsm_service.gsm_ver()

    # Check for expected message and configure GSM service if necessary
    if not gsm_service.wait_for_message("N717", timeout=3):
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
        # Extract status value
        status_value = int(status_message.split(":")[1].split("[")[0].strip())
        gsm_service.restart_disable(3600)
        # Check if status value is <= 3 and handle PIN if necessary
        if status_value <= 3:
            pin_value = '1234'
            pin_check_command = 'print pin\n'
            pin_set_command = f'set pin {pin_value}\n'
            pin_pattern = r'pin=\s?\d{4}'
            gsm_service.write(pin_check_command)
            pin_output = gsm_service.read_console_output(line_count=5)

            if re.search(pin_pattern, pin_output):
                print("The string contains 'pin=' followed by an optional space and 4 digits.")
                return False
            else:
                print("The string does not contain 'pin=' followed by an optional space and 4 digits.")
                gsm_service.write(pin_set_command)
                gsm_service.save()
                gsm_service.reset()
                gsm_service.wait_for_message("Modul radiowy poprawnie wykryty", timeout=60)
                return True
    except (ValueError, IndexError):
        pytest.skip("Failed to retrieve a valid GSM status.")

    # Wait for operator information to be available
    gsm_service.wait_for_message("INF: Operator sieci:", timeout=150)

    yield


def test_gsm_at_cops(gsm_service, gsm_setup):
    """
    Test to verify the +COPS command for the GSM service.
    """
    gsm_service.login_admin()

    expected_message = "+COPS: 0,"
    gsm_service.gsm_at_cops()
    result = gsm_service.wait_for_message(expected_message, timeout=10)

    assert result, f"Expected board serial message '{expected_message}' was not received."


def test_gsm_ati(gsm_service, gsm_setup):
    """
    Test to verify the ATI command for the GSM service.
    """
    gsm_service.login_admin()

    # Expected message based on the Neoway N717 AT Commands Manual
    expected_message = "V0"
    gsm_service.gsm_aux_ati()
    result = gsm_service.wait_for_message(expected_message, timeout=5)

    assert result, f"Expected board model to be '{expected_message}' was not received."


def test_gsm_at():
    """
    Placeholder for additional GSM AT command tests.
    """
    pass


def test_gsm_at_creg(gsm_service, gsm_setup):
    """
    Test to verify the +CREG command for the GSM service.
    """
    gsm_service.login_admin()

    # Expected message based on the Neoway N717 AT Commands Manual
    expected_message = "2,"
    gsm_service.gsm_at_creg()
    result = gsm_service.wait_for_message(expected_message, timeout=5)

    assert result, f"Expected network registration status '{expected_message}' was not received."
