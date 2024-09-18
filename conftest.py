import logging
import os
import time
from datetime import datetime

import pytest

from common.Service import GSMService
from common.communicator import SerialCommunicator


def pytest_addoption(parser):
    parser.addoption(
        "--serial-config",
        action="store",
        default="../../common/config_file.txt",
        help="Path to the serial configuration file",
    )

failed_tests = []

# Hook to collect failed tests
def pytest_runtest_logreport(report):
    if report.failed and report.when == 'call':
        failed_tests.append(report)

# Hook to rerun the failed tests after the test session ends
@pytest.hookimpl(tryfirst=True)
def pytest_sessionfinish(session, exitstatus):
    if failed_tests:
        print(f"\nRerunning {len(failed_tests)} failed tests...")
        for test in failed_tests:
            session.items = [item for item in session.items if item.nodeid == test.nodeid]
            session.config.hook.pytest_runtestloop(session=session)

# Fixture to reset the failed tests list
@pytest.fixture(scope="session", autouse=True)
def reset_failed_tests():
    global failed_tests
    failed_tests = []
# import os
# import subprocess


 # def pytest_sessionfinish(session, exitstatus):
 #     """Hook called after the whole test run finishes."""
 #     rerun_flag = 'PYTEST_RERUN_FAILED_TESTS'
 #
 #     if exitstatus != 0:  # There are failed tests
 #         # Check if the environment variable is set
 #         if os.getenv(rerun_flag) is None:
 #             print("\nSome tests failed, rerunning only the failed tests...")
 #             # Set the environment variable to indicate that rerun has occurred
 #             os.environ[rerun_flag] = '1'
 #             # Run only the failed tests
 #             subprocess.run(['pytest', '--lf'])
 #         else:
 #             print("\nFailed tests already rerun.")
 #     else:
 #         print("\nAll tests passed, no need to rerun.")
 #         # Optionally, clear the environment variable if it exists
 #         if rerun_flag in os.environ:
 #             del os.environ[rerun_flag]
