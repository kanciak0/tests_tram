import logging

import pytest

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

# Global fixture that runs once at the start of the session
@pytest.fixture(scope='session', autouse=True)
def log_configuration():
    logging.info("Saving current configuration:")