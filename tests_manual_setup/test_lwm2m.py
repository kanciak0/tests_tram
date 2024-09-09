import re

import pytest
from common.Service import LWM2MService

"""
In order to run these tests, you need to configure lwm2m server also on website for tests to fully operate
"""


@pytest.fixture(scope='module')
def lwm2m_service(request):
    config_file = request.config.getoption("--serial-config")
    service = LWM2MService(config_file=config_file)
    yield service
    service.ser.close()


def test_lwm2m_server_connection(lwm2m_service):
    lwm2m_service.login_admin()
    print("Testing LWM2M server connection...")
    expected_message = "LwM2M serwer status: polaczony"

    # Change LwM2M URI
    lwm2m_uri = 'coap://77.252.222.202:5683'
    set_command = f'set lwm2m_uri {lwm2m_uri}\n'
    lwm2m_service.write(set_command)
    lwm2m_service.save()
    lwm2m_service.reset()

    # Wait for the module to be initialized
    lwm2m_service.wait_for_message("Modul radiowy poprawnie wykryty i zainicjowany", timeout=60)
    print(f"LwM2M URI changed to {lwm2m_uri}.")

    # Verify the new URI
    lwm2m_service.write('lwm2m.status\n')
    lwm2m_output = lwm2m_service.read_console_output(line_count=5)

    # Check if the URI is set correctly
    lwm2m_pattern = rf'lwm2m_uri=\s?{re.escape(lwm2m_uri)}'
    if re.search(lwm2m_pattern, lwm2m_output):
        print(f"LwM2M URI is correctly set to '{lwm2m_uri}'.")
    else:
        print(f"LwM2M URI verification failed. Expected '{lwm2m_uri}'.")

    # Check for the expected message
    result = lwm2m_service.wait_for_message(expected_message, timeout=5)
    assert result, "Failed to connect to the LwM2M server"
    print("Test for LwM2M server connection completed successfully.")


def test_lwm2m_secure_server_connection(lwm2m_manager,lwm2m_service):
    print("Testing secure LwM2M server connection...")
    lwm2m_service.login_admin()
    expected_message = "LWM2M serwer status: polaczony"
    lwm2m_manager.change_lwm2m_uri('coaps://77.252.222.202:5684')
    lwm2m_service.login_admin()
    lwm2m_service.lwm2m_status()
    result = lwm2m_manager.communicator.wait_for_message(expected_message, timeout=5)

    assert result, "Failed to connect to the secure LwM2M server"
    print("Test for secure LwM2M server connection completed successfully.")


# def test_lwm2m_reconnect_mechanism(lwm2m_manager,lwm2m_service):
#     print("Testing LwM2M reconnect mechanism...")
#
#     # Set an invalid URI to simulate disconnection
#     lwm2m_service.lwm2m_reconnect()
#     result = lwm2m_manager.communicator.wait_for_message("LWM2m serwer status: niepolaczony", timeout=60)
#
#     assert not result, "Device is still connected after setting an invalid URI"
#
#     # Restore the correct URI and verify reconnection
#     lwm2m_manager.change_lwm2m_uri('coap://77.252.222.202:5683')
#     lwm2m_manager.check_and_set_lwm2m()
#     result = lwm2m_manager.communicator.wait_for_message("LWM2M serwer status: polaczony", timeout=60)
#
#     assert result, "Device failed to reconnect after setting the correct URI"
#     print("Test for LwM2M reconnect mechanism completed successfully.")


# def test_lwm2m_bootstrap(lwm2m_manager):
#     print("Testing LwM2M bootstrap procedure...")
#     lwm2m_manager.communicator.write('set lwm2m_bootstrap 1\n')
#     lwm2m_manager.service.save()
#     lwm2m_manager.service.reset()
#     result = lwm2m_manager.communicator.wait_for_message("LwM2M bootstrap: OK", timeout=60)
#
#     assert result, "LwM2M bootstrap procedure failed"
#     print("Test for LwM2M bootstrap procedure completed successfully.")
