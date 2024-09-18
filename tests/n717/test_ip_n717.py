import logging
import os
import sys
import time

import pytest

from common.Service import SerialService

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

@pytest.fixture(scope='module')
def serial_service(request):
    config_file = request.config.getoption("--serial-config")
    service = SerialService(config_file=config_file)
    yield service
    service.ser.close()


def test_ip_iface_n717(serial_service):
    """
    Test to verify IP interface configuration.
    """
    logging.info("Starting test_ip_iface_n27")
    try:
        serial_service.login_admin()
        print("Testing IP interface...")

        # First attempt
        serial_service.write("ip.iface\n")
        result = serial_service.wait_for_message("DNS2", timeout=5)

        if not result:
            # Wait 30 seconds before retrying
            time.sleep(30)

            # Second attempt
            serial_service.write("ip.iface\n")
            result = serial_service.wait_for_message("DNS2", timeout=5)

        # If the result is still False, this assertion will fail the test.
        assert result, "Test failed: Expected message not received after two attempts."
        logging.info("IP interface test completed successfully.")
    except AssertionError as e:
        logging.error(f"Test failed: {e}")
        raise
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise


def test_ip_state_n717(serial_service):
    """
    Test to verify IP state.
    """
    logging.info("Starting test_ip_state_n27")
    try:
        serial_service.login_admin()
        print("Testing IP state...")
        serial_service.write("ip.state\n")
        response = serial_service.wait_for_message("Uplink task")

        # Check for uplink state
        assert response, "Uplink state is not running or missing."
        logging.info("IP state test completed successfully.")
    except AssertionError as e:
        logging.error(f"Test failed: {e}")
        raise
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise

def test_ip_ping_n717(serial_service, address="8.8.8.8"):
    """
    Test to verify IP ping functionality.
    """
    logging.info(f"Starting test_ip_ping_n27 to {address}")
    try:
        print(f"Testing IP ping to {address}...")
        serial_service.login_admin()
        serial_service.write(f"ip.ping {address}\n")

        # Wait for the resolved address message
        resolved_message = serial_service.wait_for_message(f"PING: resolved: {address} -> {address}")
        assert resolved_message, "Ping resolution message not received."

        # Wait for the "Done" message to confirm completion
        done_message = serial_service.wait_for_message("PING: Done")
        assert done_message, "Ping completion message 'PING: Done' not received."

        logging.info(f"Ping test to {address} completed successfully.")
    except AssertionError as e:
        logging.error(f"Test failed: {e}")
        raise
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise

@pytest.mark.skip(reason="Deprecated for this firmware version.")
def test_server_ip_n717(serial_service, server_ip="192.168.1.1"):
    """
    Test the configuration of the server IP for ping tests.
    """
    logging.info(f"Starting test_server_ip_n27 with server IP {server_ip}")
    try:
        print(f"Testing server IP configuration with {server_ip}...")
        serial_service.write(f"test_server_ip {server_ip}\n")
        response = serial_service.wait_for_message(f"Server IP set to {server_ip}")
        assert response, "Server IP configuration message not received."
        logging.info(f"Server IP test with {server_ip} completed successfully.")
    except AssertionError as e:
        logging.error(f"Test failed: {e}")
        raise
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise

@pytest.mark.skip(reason="Deprecated for this firmware version.")
def test_server_ip2_n717(serial_service, server_ip2="192.168.1.2"):
    """
    Test the configuration of the second server IP for ping tests.
    """
    logging.info(f"Starting test_server_ip2_n27 with secondary server IP {server_ip2}")
    try:
        print(f"Testing secondary server IP configuration with {server_ip2}...")
        serial_service.write(f"test_server_ip2 {server_ip2}\n")
        response = serial_service.wait_for_message(f"Secondary Server IP set to {server_ip2}")
        assert response, "Secondary Server IP configuration message not received."
        logging.info(f"Secondary Server IP test with {server_ip2} completed successfully.")
    except AssertionError as e:
        logging.error(f"Test failed: {e}")
        raise
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise

@pytest.mark.skip(reason="Deprecated for this firmware version.")
def test_failure_action_n717(serial_service, action="prev-config"):
    """
    Test the failure action configuration.
    """
    logging.info(f"Starting test_failure_action_n27 with action {action}")
    try:
        print(f"Testing failure action configuration with {action}...")
        serial_service.write(f"test_failure_action {action}\n")
        response = serial_service.wait_for_message(f"Failure action set to {action}")
        assert response, "Failure action configuration message not received."
        logging.info(f"Failure action test with {action} completed successfully.")
    except AssertionError as e:
        logging.error(f"Test failed: {e}")
        raise
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise

@pytest.mark.skip(reason="Deprecated for this firmware version.")
def test_testing_interval_n717(serial_service, interval=120):
    """
    Test the testing interval configuration.
    """
    logging.info(f"Starting test_testing_interval_n27 with interval {interval}")
    try:
        print(f"Testing testing interval configuration with {interval} seconds...")
        serial_service.write(f"testing_interval {interval}\n")
        response = serial_service.wait_for_message(f"Testing interval set to {interval} seconds")
        assert response, "Testing interval configuration message not received."
        logging.info(f"Testing interval test with {interval} seconds completed successfully.")
    except AssertionError as e:
        logging.error(f"Test failed: {e}")
        raise
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise

@pytest.mark.skip(reason="Deprecated for this firmware version.")
def test_ping_size_n717(serial_service, size=64):
    """
    Test the ping size configuration.
    """
    logging.info(f"Starting test_ping_size_n27 with size {size}")
    try:
        print(f"Testing ping size configuration with {size} bytes...")
        serial_service.write(f"test_ping_size {size}\n")
        response = serial_service.wait_for_message(f"Ping size set to {size} bytes")
        assert response, "Ping size configuration message not received."
        logging.info(f"Ping size test with {size} bytes completed successfully.")
    except AssertionError as e:
        logging.error(f"Test failed: {e}")
        raise
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise

@pytest.mark.skip(reason="Deprecated for this firmware version.")
def test_ping_count_n717(serial_service, count=3):
    """
    Test the ping count configuration.
    """
    logging.info(f"Starting test_ping_count_n27 with count {count}")
    try:
        print(f"Testing ping count configuration with {count} pings...")
        serial_service.write(f"test_ping_count {count}\n")
        response = serial_service.wait_for_message(f"Ping count set to {count}")
        assert response, "Ping count configuration message not received."
        logging.info(f"Ping count test with {count} pings completed successfully.")
    except AssertionError as e:
        logging.error(f"Test failed: {e}")
        raise
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise

@pytest.mark.skip(reason="Deprecated for this firmware version.")
def test_ping_tout_n717(serial_service, timeout=1000):
    """
    Test the ping timeout configuration.
    """
    logging.info(f"Starting test_ping_tout_n27 with timeout {timeout}")
    try:
        print(f"Testing ping timeout configuration with {timeout} ms...")
        serial_service.write(f"test_ping_tout {timeout}\n")
        response = serial_service.wait_for_message(f"Ping timeout set to {timeout} ms")
        assert response, "Ping timeout configuration message not received."
        logging.info(f"Ping timeout test with {timeout} ms completed successfully.")
    except AssertionError as e:
        logging.error(f"Test failed: {e}")
        raise
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise


@pytest.mark.skip(reason="Deprecated for this firmware version.")
def test_ping_ratio_n717(serial_service, ratio=75):
    """
    Test the ping ratio configuration.
    """
    logging.info(f"Starting test_ping_ratio_n27 with ratio {ratio}")
    try:
        print(f"Testing ping ratio configuration with {ratio}%...")
        serial_service.write(f"test_ping_ratio {ratio}\n")
        response = serial_service.wait_for_message(f"Ping ratio set to {ratio}%")
        assert response, "Ping ratio configuration message not received."
        logging.info(f"Ping ratio test with {ratio}% completed successfully.")
    except AssertionError as e:
        logging.error(f"Test failed: {e}")
        raise
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise


@pytest.mark.skip(reason="Deprecated for this firmware version.")
def test_ping_delay_n717(serial_service, delay=90):
    """
    Test the ping delay configuration.
    """
    logging.info(f"Starting test_ping_delay_n27 with delay {delay}")
    try:
        print(f"Testing ping delay configuration with {delay} seconds...")
        serial_service.write(f"test_ping_delay {delay}\n")
        response = serial_service.wait_for_message(f"Ping delay set to {delay} seconds")
        assert response, "Ping delay configuration message not received."
        logging.info(f"Ping delay test with {delay} seconds completed successfully.")
    except AssertionError as e:
        logging.error(f"Test failed: {e}")
        raise
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise