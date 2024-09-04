import pytest

from common.Service import SerialService


@pytest.fixture(scope='module')
def serial_service(request):
    """
    Fixture to initialize and provide the SerialService instance for the tests.
    """
    config_file = request.config.getoption("--serial-config")
    service = SerialService(config_file=config_file,test_file_name="log_test_uplink_n717")
    yield service
    service.close()


@pytest.mark.skip("Configuration not working")
def test_uplink1_rs485_custom_n717(serial_service):
    """
    Test to verify the uplink1 configuration with RS485 and custom settings.
    This test is marked as deprecated and should not be run for the current firmware version.
    """
    print("Testing uplink1 configuration with RS485 and custom settings...")
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

    print("Uplink1 configuration with RS485 and custom settings completed successfully.")


def test_uplink1_rs232_custom_speed_n717(serial_service):
    """
    Test to verify the uplink1 configuration with RS232 and custom initial speed.
    """
    print("Testing uplink1 configuration with RS232 and custom initial speed...")
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

    print("Uplink1 configuration with RS232 and custom initial speed completed successfully.")


def test_uplink1_rs232_custom_framing_n717(serial_service):
    #TODO: ONLY WORKS WITH APAP-BIN WHY THO?, TRANSPARENT NOT WORKING
    print("Testing uplink1 configuration with RS232 and custom framing...")
    serial_service.login_admin()
    # Set the uplink1 configuration
    uplink="rs232:8E1,srv,tcp:8500,apap-bin"
    serial_service.write(f"set uplink1 {uplink}\n")

    serial_service.save()
    serial_service.reset()

    serial_service.wait_for_message("Modul radiowy poprawnie wykryty i zainicjowany")
    serial_service.login_admin()

    serial_service.write("print uplink\n")
    response = serial_service.wait_for_message(uplink)

    assert response, "Uplink1 configuration mismatch or not set correctly."

    print("Uplink1 configuration with RS232 and custom framing completed successfully.")