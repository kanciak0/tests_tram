import logging
import os

import pytest

from common.Service import APNService


@pytest.fixture(scope='module')
def apn_service(request):
    """
    Fixture to initialize and provide the SerialService instance for the tests.
    """
    config_file = request.config.getoption("--serial-config")
    apn_service = APNService(config_file=config_file)
    logging.info("---------------------------------SWITCHING ACTIVE RADIO TO N717---------------------------------")
    yield apn_service



# @pytest.fixture(scope='module')
# def gsm_service():
#     gsm_service = GSMService(config_file='config.txt')
#     yield gsm_service
#     gsm_service.close()


@pytest.fixture(scope="module", autouse=True)
def radio_setup_n717(apn_service):
    apn_service.login_admin()
    apn_service.gsm_ver()
    expected_radio = apn_service.wait_for_message("717",timeout=5)
    if expected_radio is False:
        apn_service.set_active_radio(radio_id=2)
        apn_service.save()
        apn_service.reset()
        apn_service.wait_for_message("Modul radiowy poprawnie wykryty")
        apn_service.login_admin()
        apn_service.gsm_ver()
        expected_radio = apn_service.wait_for_message("N717")
        if expected_radio is False:
            pytest.fail("Nie przelaczono na poprawny modul radiowy")
    yield
    apn_service.save()
    apn_service.reset()
    apn_service.wait_for_message("Modul radiowy poprawnie wykryty i zainicjowany")

def test_set_apn_name_n717(apn_service):
    """
    Test to verify setting and retrieving the APN name.
    """
    logging.info("Starting test_set_apn_name")
    try:
        apn_service.login_admin()
        apn_name = apn_service.get_apn_name()
        apn_service.set_apn_name(apn_name)

        apn_service.print_apn()
        expected_message = f"apn_name={apn_name}"
        result = apn_service.wait_for_message(expected_message)

        assert result, f"Expected APN name '{expected_message}' was not received."
        logging.info("APN name test passed successfully.")
    except AssertionError as e:
        logging.error(f"Test failed: {e}")
        raise
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise


def test_set_apn_login_n717(apn_service):
    """
    Test to verify setting and retrieving the APN login.
    """
    logging.info("Starting test_set_apn_login")
    try:
        apn_service.login_admin()
        apn_login = "ppp"
        assert len(apn_login) <= 32, "APN login exceeds maximum length"
        apn_service.set_apn_login(apn_login)

        apn_service.print_apn()
        expected_message = f"apn_login={apn_login}"
        result = apn_service.wait_for_message(expected_message)

        assert result, f"Expected APN login '{expected_message}' was not received."
        logging.info("APN login test passed successfully.")
    except AssertionError as e:
        logging.error(f"Test failed: {e}")
        raise
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise


def test_set_apn_password_n717(apn_service):
    """
    Test to verify setting and retrieving the APN password.
    """
    logging.info("Starting test_set_apn_password")
    try:
        apn_service.login_admin()
        apn_passwd = "ppp"
        assert len(apn_passwd) <= 32, "APN password exceeds maximum length"
        apn_service.set_apn_passwd(apn_passwd)

        apn_service.print_apn()
        expected_message = f"apn_passwd={apn_passwd}"
        result = apn_service.wait_for_message(expected_message)

        assert result, f"Expected APN password '{expected_message}' was not received."
        logging.info("APN password test passed successfully.")
    except AssertionError as e:
        logging.error(f"Test failed: {e}")
        raise
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise


def test_set_apn_auth_n717(apn_service):
    """
    Test to verify setting and retrieving the APN authentication method.
    """
    logging.info("Starting test_set_apn_auth")
    try:
        apn_service.login_admin()
        apn_auth = "pap"
        valid_auth_methods = ["pap", "chap", "none"]
        assert apn_auth in valid_auth_methods, f"APN auth '{apn_auth}' is not valid"
        assert len(apn_auth) <= 16, "APN auth method exceeds maximum length"
        apn_service.set_apn_auth(apn_auth)

        apn_service.print_apn()
        expected_message = f"apn_auth={apn_auth}"
        result = apn_service.wait_for_message(expected_message)

        assert result, f"Expected APN authentication method '{expected_message}' was not received."
        logging.info("APN authentication method test passed successfully.")
    except AssertionError as e:
        logging.error(f"Test failed: {e}")
        raise
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise


def test_set_apn_tries_n717(apn_service):
    """
    Test to verify setting and retrieving the APN tries parameter.
    """
    logging.info("Starting test_set_apn_tries")
    try:
        apn_service.login_admin()
        apn_tries = 8
        assert 4 <= apn_tries <= 360, "APN tries value must be between 4 and 360"

        apn_service.set_apn_tries(apn_tries)
        apn_service.print_apn()
        expected_message = f"apn_tries={apn_tries}"
        result = apn_service.wait_for_message(expected_message)

        assert result, f"Expected APN tries parameter '{expected_message}' was not received."
        logging.info("APN tries parameter test passed successfully.")
    except AssertionError as e:
        logging.error(f"Test failed: {e}")
        raise
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise


