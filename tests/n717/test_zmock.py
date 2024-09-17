import os
import logging
import time
import subprocess
import pytest
from common.Service import GSMService


# Pytest fixture for GSM service
@pytest.fixture(scope='module')
def gsm_service(request):
    """
    Fixture to initialize GSMService and ensure configuration is restored after tests.
    """
    config_file = request.config.getoption("--serial-config")
    service = GSMService(config_file=config_file)

    # Teardown logic: Restore configuration after all tests in this module are done
    def teardown():
        logging.info("--------------------------------RESTORING CONFIGURATION--------------------------------")
        time.sleep(5)
        service.restore_configuration(config_file='backup_logs/backup_config.txt')
        service.ser.close()

    request.addfinalizer(teardown)

    yield service


# Test function (placeholder)
def test_backup(gsm_service):
    pass


# Pytest hook to rerun failed tests at the end of the session
def pytest_sessionfinish(session, exitstatus):
    """Hook called after the whole test run finishes."""
    rerun_flag = 'PYTEST_RERUN_FAILED_TESTS'

    if exitstatus != 0:  # There are failed tests
        # Check if the environment variable is set
        if os.getenv(rerun_flag) is None:
            print("\nSome tests failed, rerunning only the failed tests...")
            # Set the environment variable to indicate that rerun has occurred
            os.environ[rerun_flag] = '1'
            # Run only the failed tests
            subprocess.run(['pytest', '--lf'])
        else:
            print("\nFailed tests have already been rerun.")
    else:
        print("\nAll tests passed, no need to rerun.")
        # Optionally, clear the environment variable if it exists
        if rerun_flag in os.environ:
            del os.environ[rerun_flag]
