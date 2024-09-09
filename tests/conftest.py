import logging
import os
from datetime import datetime

import pytest

from common.communicator import SerialCommunicator


def pytest_addoption(parser):
    parser.addoption(
        "--serial-config",
        action="store",
        default="../../common/config_file.txt",
        help="Path to the serial configuration file",
    )
