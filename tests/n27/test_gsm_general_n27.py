from typing import re

import pytest

from common.Service import GSMService


@pytest.fixture(scope='module')
def gsm_service(request):
    """
    Fixture to initialize and provide the GSMService instance for the tests.
    """
    config_file = request.config.getoption("--serial-config")
    service = GSMService(config_file=config_file)
    yield service
    service.close()


def test_gsm_ver_n27(gsm_service):
    """
    Test to verify the GSM module type and firmware version.
    """
    gsm_service.login_admin()
    gsm_service.gsm_ver()
    expected_message = "LCT: Typ modulu: "  # Example expected output

    result = gsm_service.wait_for_message(expected_message)

    assert result, f"Expected GSM version message '{expected_message}' was not received."


def test_gsm_ids_n27(gsm_service):
    """
    Test to verify the IMEI, IMSI, and SIM ID (ICCID) numbers.
    """
    gsm_service.login_admin()
    gsm_service.gsm_ids()
    expected_message = "SIMID "

    result = gsm_service.wait_for_message(expected_message)

    assert result, f"Expected GSM IDs message '{expected_message}' was not received."


def test_gsm_band_n27(gsm_service):
    """
    Test to verify the radio band used by the device and ensure correct APN and PIN settings.
    """


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

    # Wait for any of the expected messages or "???"
    result = gsm_service.wait_for_one_of_expected_messages(expected_messages, timeout=5)

    if result is False:
        expected_apn_name = "vpn.static.pl"
        pin_value = '1234'
        pin_check_command = 'print pin\n'
        pin_set_command = f'set pin {pin_value}\n'
        # Handle the "???" case by checking and setting APN and PIN
        gsm_service.write("print apn\n")
        result = gsm_service.wait_for_message(expected_apn_name)

        if not result:
            print(f"APN name is not set correctly, setting it to '{expected_apn_name}'")
            gsm_service.write(f"set apn_name {expected_apn_name}")
            gsm_service.save()
            gsm_service.reset()
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
            gsm_service.login_admin()
            gsm_service.gsm_band()
            return True
        # After setting APN and PIN, recheck the GSM band

    # Assert that one of the expected messages was received
    assert result, f"Expected one of the GSM/LTE band messages {expected_messages}, but got '{result}'."


def test_gsm_rssi_n27(gsm_service):
    """
    Test to verify the current signal strength (RSSI) and bit error rate (BER).
    """
    gsm_service.login_admin()
    gsm_service.gsm_rssi()
    expected_message = "RSSI: "  # Example expected output

    result = gsm_service.wait_for_message(expected_message)

    assert result, f"Expected GSM RSSI message '{expected_message}' was not received."


def test_gsm_rssiex_n27(gsm_service):
    """
    Test to verify the extended signal strength (RSSI) and bit error rate (BER).
    """
    gsm_service.login_admin()
    gsm_service.gsm_rssiex()
    expected_message = "Temp: "  # Example expected output

    result = gsm_service.wait_for_message(expected_message)

    assert result, f"Expected GSM RSSIex message '{expected_message}' was not received."


def test_gsm_regstate_n27(gsm_service):
    """
    Test to verify the registration status in GSM and GPRS networks.
    """
    gsm_service.login_admin()
    gsm_service.gsm_regstate()
    expected_message = "Siec GSM: "  # Example expected output

    result = gsm_service.wait_for_message(expected_message)

    assert result, f"Expected GSM registration state message '{expected_message}' was not received."


def test_gsm_state_n27(gsm_service):
    """
    Test to verify the state of the GSM module.
    """
    gsm_service.login_admin()
    gsm_service.gsm_state()
    expected_message = "Stan kanalu sterujacego: "  # Example expected output

    result = gsm_service.wait_for_message(expected_message)

    assert result, f"Expected GSM state message '{expected_message}' was not received."


def test_gsm_status_n27(gsm_service):
    """
    Test to verify the status of the GSM module.
    """
    gsm_service.login_admin()
    gsm_service.gsm_status()
    expected_message = "LCT: Radio status: "  # Example expected output

    result = gsm_service.wait_for_message(expected_message)

    assert result, f"Expected GSM status message '{expected_message}' was not received."


def test_gsm_cellinfo_n27(gsm_service):
    """
    Test to verify the information about the serving cell.
    """
    gsm_service.login_admin()
    gsm_service.gsm_cellinfo()
    expected_message = "LAC"  # Replace with the expected output

    result = gsm_service.wait_for_message(expected_message)

    assert result, f"Expected GSM cell info message '{expected_message}' was not received."
