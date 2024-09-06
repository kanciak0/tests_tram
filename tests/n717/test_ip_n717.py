import time

import pytest

from common.Service import SerialService


@pytest.fixture(scope='module')
def serial_service(request):
    config_file = request.config.getoption("--serial-config")
    service = SerialService(config_file=config_file)
    yield service



def test_ip_iface_n717(serial_service):
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
    assert result, "Test failed: Expected message 'DNS2' not received after two attempts."


def test_ip_state_n717(serial_service):
    serial_service.login_admin()
    print("Testing IP state...")
    serial_service.write("ip.state\n")
    response = serial_service.wait_for_message("Uplink task")

    # Check for uplink state
    assert response, "Uplink state is not running or missing."
    print("IP state test completed successfully.")


def test_ip_ping_n717(serial_service, address="8.8.8.8"):
    print(f"Testing IP ping to {address}...")
    serial_service.login_admin()
    serial_service.write(f"ip.ping {address}\n")

    # Wait for the resolved address message
    resolved_message = serial_service.wait_for_message(f"PING: resolved: {address} -> {address}")
    assert resolved_message, "Ping resolution message not received."

    # Wait for the "Done" message to confirm completion
    done_message = serial_service.wait_for_message("PING: Done")
    assert done_message, "Ping completion message 'PING: Done' not received."

    print(f"Ping test to {address} completed successfully.")


@pytest.mark.skip(reason="Deprecated for this firmware version.")
def test_server_ip_n717(serial_service, server_ip="192.168.1.1"):
    """Test the configuration of the server IP for ping tests."""
    print(f"Testing server IP configuration with {server_ip}...")
    serial_service.write(f"test_server_ip {server_ip}\n")
    response = serial_service.wait_for_message(f"Server IP set to {server_ip}")
    assert response, "Server IP configuration message not received."
    print(f"Server IP test with {server_ip} completed successfully.")


@pytest.mark.skip(reason="Deprecated for this firmware version.")
def test_server_ip2_n717(serial_service, server_ip2="192.168.1.2"):
    """Test the configuration of the second server IP for ping tests."""
    print(f"Testing secondary server IP configuration with {server_ip2}...")
    serial_service.write(f"test_server_ip2 {server_ip2}\n")
    response = serial_service.wait_for_message(f"Secondary Server IP set to {server_ip2}")
    assert response, "Secondary Server IP configuration message not received."
    print(f"Secondary Server IP test with {server_ip2} completed successfully.")


@pytest.mark.skip(reason="Deprecated for this firmware version.")
def test_failure_action_n717(serial_service, action="prev-config"):
    """Test the failure action configuration."""
    print(f"Testing failure action configuration with {action}...")
    serial_service.write(f"test_failure_action {action}\n")
    response = serial_service.wait_for_message(f"Failure action set to {action}")
    assert response, "Failure action configuration message not received."
    print(f"Failure action test with {action} completed successfully.")


@pytest.mark.skip(reason="Deprecated for this firmware version.")
def test_testing_interval_n717(serial_service, interval=120):
    """Test the testing interval configuration."""
    print(f"Testing testing interval configuration with {interval} seconds...")
    serial_service.write(f"testing_interval {interval}\n")
    response = serial_service.wait_for_message(f"Testing interval set to {interval} seconds")
    assert response, "Testing interval configuration message not received."
    print(f"Testing interval test with {interval} seconds completed successfully.")


@pytest.mark.skip(reason="Deprecated for this firmware version.")
def test_ping_size_n717(serial_service, size=64):
    """Test the ping size configuration."""
    print(f"Testing ping size configuration with {size} bytes...")
    serial_service.write(f"test_ping_size {size}\n")
    response = serial_service.wait_for_message(f"Ping size set to {size} bytes")
    assert response, "Ping size configuration message not received."
    print(f"Ping size test with {size} bytes completed successfully.")


@pytest.mark.skip(reason="Deprecated for this firmware version.")
def test_ping_count_n717(serial_service, count=3):
    """Test the ping count configuration."""
    print(f"Testing ping count configuration with {count} pings...")
    serial_service.write(f"test_ping_count {count}\n")
    response = serial_service.wait_for_message(f"Ping count set to {count}")
    assert response, "Ping count configuration message not received."
    print(f"Ping count test with {count} pings completed successfully.")


@pytest.mark.skip(reason="Deprecated for this firmware version.")
def test_ping_tout_n717(serial_service, timeout=1000):
    """Test the ping timeout configuration."""
    print(f"Testing ping timeout configuration with {timeout} ms...")
    serial_service.write(f"test_ping_tout {timeout}\n")
    response = serial_service.wait_for_message(f"Ping timeout set to {timeout} ms")
    assert response, "Ping timeout configuration message not received."
    print(f"Ping timeout test with {timeout} ms completed successfully.")


@pytest.mark.skip(reason="Deprecated for this firmware version.")
def test_ping_ratio_n717(serial_service, ratio=75):
    """Test the ping ratio configuration."""
    print(f"Testing ping ratio configuration with {ratio}%...")
    serial_service.write(f"test_ping_ratio {ratio}\n")
    response = serial_service.wait_for_message(f"Ping ratio set to {ratio}%")
    assert response, "Ping ratio configuration message not received."
    print(f"Ping ratio test with {ratio}% completed successfully.")


@pytest.mark.skip(reason="Deprecated for this firmware version.")
def test_ping_delay_n717(serial_service, delay=90):
    """Test the ping delay configuration."""
    print(f"Testing ping delay configuration with {delay} seconds...")
    serial_service.write(f"test_ping_delay {delay}\n")
    response = serial_service.wait_for_message(f"Ping delay set to {delay} seconds")
    assert response, "Ping delay configuration message not received."
    print(f"Ping delay test with {delay} seconds completed successfully.")