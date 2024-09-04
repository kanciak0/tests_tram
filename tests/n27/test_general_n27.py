import pytest

from common.Service import SerialService


@pytest.fixture(scope='module')
def serial_service(request):
    """
    Fixture to initialize and provide the SerialService instance for the tests.
    """
    config_file = request.config.getoption("--serial-config")
    service = SerialService(config_file=config_file,test_file_name="log_test_general_n27")
    yield service
    service.close()


def test_ver_n27(serial_service):
    """
    Test to verify the version information of the TRAM device.
    """
    #It only checks if this command works.
    serial_service.ver()
    expected_message = "TRAM APATOR, version"

    result = serial_service.wait_for_message(expected_message)

    assert result, f"Expected version message '{expected_message}' was not received."


def test_hwver_n27(serial_service):
    """
    Test to verify the hardware version information of the TRAM device.
    """
    serial_service.hwver()
    #It only checks if this command works.
    expected_message = "TRAM v"

    result = serial_service.wait_for_message(expected_message)

    assert result, f"Expected hardware version message '{expected_message}' was not received."


@pytest.mark.parametrize("urc_value, expected_message", [
    (1, "URC: 1"),
    (0, "URC: 0")
])
def test_urc_with_parameters_n27(serial_service, urc_value, expected_message):
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


def test_config_info_n27(serial_service):
    """
    Test to retrieve and verify configuration information from the TRAM device.
    """
    serial_service.login_admin()
    serial_service.config_info()
    expected_message = "config"

    result = serial_service.wait_for_message(expected_message)

    assert result, f"Expected configuration info message '{expected_message}' was not received."


def test_urc_without_parameters_n27(serial_service):
    """
    Test to verify the URC (Unsolicited Result Code) response without parameters.
    """
    serial_service.urc_without_parameters()
    expected_message = "URC: "

    result = serial_service.wait_for_message(expected_message)

    assert result, f"Expected URC response message '{expected_message}' was not received."


def test_board_serial_show_n27(serial_service):
    """
    Test to display and verify the board serial number of the TRAM device.
    """
    serial_service.login_admin()
    serial_service.board_serial_show()
    expected_message = "BOARD SERIAL"

    result = serial_service.wait_for_message(expected_message)

    assert result, f"Expected board serial message '{expected_message}' was not received."

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


#def test_defaults_n27(config_manager, serial_service):
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

