import logging
import time

import pytest

from common.Service import GSMService


@pytest.fixture(scope='module')
def gsm_service(request):
    config_file = request.config.getoption("--serial-config")
    service = GSMService(config_file=config_file)
    yield service
    logging.info("--------------------------------RESTORING CONFIGURATION----------------------------")
    time.sleep(5)
    service.restore_configuration(config_file='backup_logs/backup_config.txt')
    service.ser.close()


def test_mock(gsm_service):
    pass