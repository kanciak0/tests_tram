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
