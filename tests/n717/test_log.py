import logging
import re
from pickletools import markobject

import pytest

# Assuming SerialService provides methods for writing to and reading from the serial console
from common.Service import SerialService


@pytest.fixture(scope='module')
def serial_service(request):
    config_file = request.config.getoption("--serial-config")
    service = SerialService(config_file=config_file)
    yield service
    service.ser.close()


def test_log_dump(serial_service):
    """
    Test to verify the log.dump command without parameters (last 20 entries).
    """
    logging.info("Starting test_log_dump without parameters")
    try:
        serial_service.login_admin()
        serial_service.write("log.dump\n")
        pattern = r'\d{2}:\d{2}:\d{2} \(\d{4}\)'
        log_message = serial_service.read_console_output(line_count=20,timeout=5)
        assert re.search(pattern, log_message), "Test failed: Expected log entries were not received."
        logging.info("log.dump without parameters test passed successfully.")
    except AssertionError as e:
        logging.error(f"Test failed: {e}")
        raise
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise


def test_log_dump_with_number(serial_service):
    """
    Test to verify the log.dump command with a specific number of entries.
    """
    logging.info("Starting test_log_dump without parameters")
    try:
        serial_service.login_admin()
        serial_service.write("log.dump 10\n")
        pattern = r'\d{2}:\d{2}:\d{2} \(\d{4}\)'
        log_message = serial_service.read_console_output(line_count=10,timeout=5)
        assert re.search(pattern, log_message), "Test failed: Expected log entries were not received."
        logging.info("log.dump without parameters test passed successfully.")
    except AssertionError as e:
        logging.error(f"Test failed: {e}")
        raise
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise

@pytest.mark.skip(reason="WIP")
def test_log_dump_with_date(serial_service):
    """
    Test to verify the log.dump command with date parameters.
    """
    logging.info("Starting test_log_dump with date parameters")
    try:
        serial_service.login_admin()
        serial_service.write("log.dump date 2023-08-08:00:00:00 2016-08-08:21:00:00\n")
        result = serial_service.wait_for_message("Blad logowania do APN", timeout=5)

        assert result, "Test failed: Expected log entries for the date range were not received."
        logging.info("log.dump with date parameters test passed successfully.")
    except AssertionError as e:
        logging.error(f"Test failed: {e}")
        raise
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise


def test_log_more_start(serial_service):
    """
    Test to verify log.more.start initializes the log with 100 entries.
    """
    logging.info("Starting test_log_more_start")
    try:
        serial_service.login_admin()
        serial_service.write("log.more.start\n")
        result = serial_service.wait_for_message("START", timeout=5)

        assert result, "Test failed: log.more.start did not return the expected message."
        logging.info("log.more.start test passed successfully.")
    except AssertionError as e:
        logging.error(f"Test failed: {e}")
        raise
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise


def test_log_more_next(serial_service):
    """
    Test to verify log.more command retrieves the next set of log entries.
    """
    logging.info("Starting test_log_more_next")
    try:
        serial_service.login_admin()
        serial_service.write("log.more 7\n")
        result = serial_service.wait_for_message("LOG-MORE: NEXT 7", timeout=5)

        assert result, "Test failed: log.more did not return the next set of entries as expected."
        logging.info("log.more test passed successfully.")
    except AssertionError as e:
        logging.error(f"Test failed: {e}")
        raise
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise
