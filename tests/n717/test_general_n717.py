import pytest

from common.Service import SerialService


@pytest.fixture(scope='module')
def serial_service(request):
    """
    Fixture to initialize and provide the SerialService instance for the tests.
    """
    config_file = request.config.getoption("--serial-config")
    service = SerialService(config_file=config_file, test_file_name="log_test_general_n717")
    yield service
    service.close()


def test_ver_n717(serial_service):
    """
    Test to verify the version information of the TRAM device.
    """
    serial_service.ver()
    expected_message = "LCT: TRAM APATOR, version"

    result = serial_service.wait_for_message(expected_message)

    assert result, f"Expected version message '{expected_message}' was not received."


def test_hwver_n717(serial_service):
    """
    Test to verify the hardware version information of the TRAM device.
    """
    serial_service.hwver()
    expected_message = "TRAM v"

    result = serial_service.wait_for_message(expected_message)

    assert result, f"Expected hardware version message '{expected_message}' was not received."


@pytest.mark.parametrize("urc_value, expected_message", [
    (1, "URC: 1"),
    (0, "URC: 0")
])
def test_urc_with_parameters_n717(serial_service, urc_value, expected_message):
    """
    Test to verify the URC (Unsolicited Result Code) response with parameters.

    Parameters:
    urc_value: The URC value to send.
    expected_message: The expected response message.
    """
    serial_service.login_admin()
    serial_service.urc_with_parameters(urc_value)

    result = serial_service.wait_for_message(expected_message)

    assert result, f"Expected URC response message '{expected_message}' was not received."


def test_config_info_n717(serial_service):
    """
    Test to retrieve and verify configuration information from the TRAM device.
    """
    serial_service.login_admin()
    serial_service.config_info()
    expected_message = "config"

    result = serial_service.wait_for_message(expected_message)

    assert result, f"Expected configuration info message '{expected_message}' was not received."


def test_urc_without_parameters_n717(serial_service):
    """
    Test to verify the URC (Unsolicited Result Code) response without parameters.
    """
    serial_service.urc_without_parameters()
    expected_message = "URC: "

    result = serial_service.wait_for_message(expected_message)

    assert result, f"Expected URC response message '{expected_message}' was not received."


def test_board_serial_show_n717(serial_service):
    """
    Test to display and verify the board serial number of the TRAM device.
    """
    serial_service.login_admin()
    serial_service.board_serial_show()
    expected_message = "BOARD SERIAL"

    result = serial_service.wait_for_message(expected_message)

    assert result, f"Expected board serial message '{expected_message}' was not received."


def test_rtc_print_n717(serial_service):
    """
    Test to verify the rtc.print command which displays the current date and time in CET with DST.
    """
    serial_service.login_admin()
    serial_service.rtc_print()
    expected_message = "RTC: "

    result = serial_service.wait_for_message(expected_message)

    assert result, f"Expected RTC print message starting with '{expected_message}' was not received."


def test_rtc_print2_n717(serial_service):
    """
    Test to verify the rtc.print2 command which displays the current date and time in a different format.
    """
    serial_service.login_admin()
    serial_service.rtc_print2()
    expected_message = "RTC: "

    result = serial_service.wait_for_message(expected_message)

    assert result, f"Expected RTC print2 message starting with '{expected_message}' was not received."


def test_rtc_print_utc_n717(serial_service):
    """
    Test to verify the rtc.print.utc command which displays the current date and time in UTC format.
    """
    serial_service.login_admin()
    serial_service.rtc_print_utc()
    expected_message = "TZ: CET"

    result = serial_service.wait_for_message(expected_message)
    assert result, f"Expected RTC UTC print message starting with '{expected_message}' was not received."


def test_rtc_set_time_n717(serial_service):
    """
    Test to verify setting the time using the rtc.set.time command.
    """
    serial_service.login_admin()
    test_time = "12 34 56"
    parsed_time = test_time.replace(" ", ":")
    serial_service.rtc_set_time(test_time)

    expected_message = f"time set to {parsed_time}"

    result = serial_service.wait_for_message(expected_message)
    assert result, f"Expected time set confirmation message '{expected_message}' was not received."


def test_rtc_set_date_n717(serial_service):
    """
    Test to verify setting the date using the rtc.set.date command.
    """
    serial_service.login_admin()

    test_date = "2024 08 29"

    parsed_date = test_date.replace(" ", "-")

    serial_service.rtc_set_date(test_date)

    expected_message = f"date set to {parsed_date}"

    result = serial_service.wait_for_message(expected_message)
    assert result, f"Expected date set confirmation message '{expected_message}' was not received."


def test_restart_disable_n717(serial_service):
    """
    Test to verify the restart.disable command.
    """
    serial_service.login_admin()
    disable_duration = 600

    serial_service.restart_disable(duration=disable_duration)

    expected_message = f"LCT: Blokada resetu wlaczona na {disable_duration} s"
    result = serial_service.wait_for_message(expected_message)

    assert result, f"Expected restart.disable confirmation message '{expected_message}' was not received."

"""
# TODO: Implement a comprehensive test for changing passwords.
# This should include:
# - Verifying maximum password length (up to 31 characters)
# - Testing default password '@!0lsaHjaD'
# - Ensuring that a successful password change returns "OK password set" message

# def test_passwd(config_manager, serial_service):

#     Test to verify the password change functionality.

#     serial_service.passwd()
#     expected_message = "OK password set"
#     result = serial_service.communicator.wait_for_message(expected_message)
#
#     assert result, f"Expected password change confirmation message '{expected_message}' was not received."
"""


#def test_defaults_n717(config_manager, serial_service):
#    """
#    Test to reset the TRAM device to its default settings.
#    """
#    serial_service.login_admin()
#    serial_service.defaults()
#    expected_message = "LCT: OK"
#
#    result = serial_service.communicator.wait_for_message(expected_message)
#
#    assert result, f"Expected defaults confirmation message '{expected_message}' was not received."

