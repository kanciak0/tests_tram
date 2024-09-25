import logging
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


import logging


def test_lwm2m_server_connection_coap(lwm2m_service):
    """
    Test to verify the LwM2M server connection using CoAP protocol.

    :param lwm2m_service: The LwM2M service instance used for interacting with the device.
    """
    logging.info("Starting LwM2M server connection test...")
    logging.critical("This is only a Coap test, device needs to be also tested for secured connection, which has to be done manually")
    result = None  # Initialize 'result' to avoid referencing before assignment

    try:
        # Log in as admin
        lwm2m_service.login_admin()

        # Get LwM2M URI
        lwm2m_uri = lwm2m_service.get_lwm2m_coap()

        expected_message = f"LWM2M serwer status: polaczony {lwm2m_uri} (STATE_READY,0)"

        # Set LwM2M URI and Bootstrap settings
        lwm2m_service.set_lwm2m_uri(lwm2m_uri)
        logging.info(f"LwM2M URI set to: {lwm2m_uri}")

        lwm2m_service.set_lwm2m_bootstrap("0")
        logging.info("LwM2M Bootstrap set to 0.")

        lwm2m_service.save()

        lwm2m_service.reset()

        # Wait for module to initialize
        lwm2m_service.wait_for_message("Modul radiowy poprawnie wykryty i zainicjowany", timeout=30)

        lwm2m_service.wait_for_message("Udana rejestracja do serwera")

        # Log in as admin again
        lwm2m_service.login_admin()

        # Verify LwM2M status
        lwm2m_service.lwm2m_status()

        # Check for the expected connection message
        result = lwm2m_service.wait_for_message(expected_message, timeout=5)
        assert result, "Failed to connect to the LwM2M server"

        logging.info("Test for LwM2M server connection completed successfully.")

    except AssertionError as e:
        logging.error(f"Test failed: {e}")
        raise
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise
    finally:
        # Handle the edge case: Log if the connection to LwM2M server failed
        if result is None or not result:
            logging.error("Failed to connect to the LwM2M server.")

# def test_lwm2m_secure_server_connection(lwm2m_service):
#     print("Testing secure LwM2M server connection...")
#     lwm2m_service.login_admin()
#     expected_message = "LWM2M serwer status: polaczony"
#     lwm2m_manager.change_lwm2m_uri('coaps://77.252.222.202:5684')
#     lwm2m_service.login_admin()
#     lwm2m_service.lwm2m_status()
#     result = lwm2m_manager.communicator.wait_for_message(expected_message, timeout=5)
#
#     assert result, "Failed to connect to the secure LwM2M server"
#     print("Test for secure LwM2M server connection completed successfully.")
#
#
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
#
#
# def test_lwm2m_bootstrap(lwm2m_manager):
#     print("Testing LwM2M bootstrap procedure...")
#     lwm2m_manager.communicator.write('set lwm2m_bootstrap 1\n')
#     lwm2m_manager.service.save()
#     lwm2m_manager.service.reset()
#     result = lwm2m_manager.communicator.wait_for_message("LwM2M bootstrap: OK", timeout=60)
#
#     assert result, "LwM2M bootstrap procedure failed"
#     print("Test for LwM2M bootstrap procedure completed successfully.")
