import pytest

from common.Service import SerialService, MockService
from tester_tram.managers.config_manager import ConfigurationManager


@pytest.fixture(scope='module')
def serial_service():
    """
    Fixture to initialize and provide the SerialService instance for the tests.
    """
    service = SerialService(config_file='config.txt')
    yield service
    service.close()


@pytest.fixture(scope='module')
def mock_service():
    mock_service = MockService()
    yield mock_service
    mock_service.close()


@pytest.mark.parametrize("urc_value, expected_message", [
    ("2", "URC: 4"),
    ("adiosjfioadgjs", "URC: Mock_Info"),
    ("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAASCDZHCJKDBFEKJFNESJKCDSasdsafe","")
])
def test_mock_urc_with_parameters_n27(config_manager, serial_service, urc_value, expected_message):
    """
    Test to verify the URC (Unsolicited Result Code) response with parameters.

    Parameters:
    urc_value: The URC value to send.
    expected_message: The expected response message.
    """
    #TODO: UNEXPECTED BEHAVIOR, WHEN GIVEN STRING, MODULE SETS URC TO 0, GIVEN RANDOM INT IT GETS ITS VALUE TO 1
    #TODO: IF ITS DIFFERENT FROM 0 OR 1
    serial_service.login_admin()
    serial_service.urc_with_parameters(urc_value)

    result = serial_service.wait_for_message(expected_message)

    assert result, f"Expected URC response message '{expected_message}' was not received."

@pytest.mark.parametrize("radio_mode, expected_response", [
    ("12345", "LCT: Blad, tylko auto, 2g, lte"),
    ("AOIJFIODSJLKCMZXDKLVLLLLLLLLLLLLLLLLLsadSDDDDDDDDDD", "LCT: Blad, tylko auto, 2g, lte"),  # Assuming this is a valid mode
    ("Mockinformation", "LCT: Blad, tylko auto, 2g, lte"),    # Assuming this is a valid mode
    ("invalid_mode", "LCT: Blad, tylko auto, 2g, lte")  # Invalid mode example
])
def test_set_radio_mode_with_parameters(config_manager, mock_service, radio_mode, expected_response):
    """
    Test to verify the response of setting the radio mode with different inputs.

    Parameters:
    radio_mode: The radio mode to set.
    expected_response: The expected response message from the device.
    """
    mock_service.login_admin()
    mock_service.mock_set_radio_mode(radio_mode)

    # Assuming that the command's output is captured similarly to the URC test
    result = mock_service.wait_for_message(expected_response)

    assert result, f"Expected response message '{expected_response}' was not received for radio mode '{radio_mode}'."

@pytest.mark.parametrize("active_radio, expected_response", [
    ("12345", "LCT: Blad, tylko auto, 2g, lte"),
    ("AOIJFIODSJLKCMZXDKLVLLLLLLLLLLLLLLLLLsadSDDDDDDDDDD", "LCT: Blad, tylko auto, 2g, lte"),
    ("Mockinformation", "LCT: Blad, tylko auto, 2g, lte"),
    ("invalid_radio", "LCT: Blad, tylko auto, 2g, lte")
])
def test_set_active_radio_with_parameters(mock_service, active_radio, expected_response):
    """
    Test to verify the response of setting the active radio with different inputs.

    Parameters:
    active_radio: The active radio setting to test.
    expected_response: The expected response message from the device.
    """
    #TODO: UNEXPECTED BEHAVIOR, WHEN GIVEN STRING, MODULE SETS ACTIVE RADIO TO 0, GIVEN RANDOM INT IT GETS ITS VALUE EVEN AFTER SAVE, MODEM WILL SWITCH TO N27
    #TODO: IF ITS DIFFERENT FROM 1 OR 2
    mock_service.login_admin()
    mock_service.mock_set_active_radio(active_radio)

    result = mock_service.wait_for_message(expected_response)

    assert result, f"Expected response message '{expected_response}' was not received for active radio '{active_radio}'."