import logging
import os
import sys
import time

import pytest

from common.Service import GSMService

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

@pytest.fixture(scope='module')
def gsm_service(request):
    """
    Fixture to initialize and provide the GSMService instance for the tests.
    """
    config_file = request.config.getoption("--serial-config")
    service = GSMService(config_file=config_file)
    yield service
    # Closing the serial connection for cleanup
    service.ser.close()


def test_set_auto_radio_mode_n27(gsm_service):
    """
    Test to verify setting the radio mode to auto.
    """
    logging.info("Starting test_set_auto_radio_mode_n27")
    try:
        expected_messages = ["LTE", "EDGE", "GPRS"]
        auto_conf_bands = 'GSM900,GSM1800,LTE2100,LTE1800,LTE900,LTE800,LTE450B31'
        auto_radio_mode = "auto"

        print("Testing setting radio mode to auto...")
        gsm_service.login_admin()
        gsm_service.write(f"set radio_mode {auto_radio_mode}\n")
        gsm_service.write(f"set conf_bands {auto_conf_bands}\n")

        gsm_service.save()
        gsm_service.reset()
        gsm_service.wait_for_message("Zmiana trybu radiowego na: auto")
        gsm_service.login_admin()
        gsm_service.gsm_rat()
        result = gsm_service.wait_for_one_of_expected_messages(expected_messages, timeout=5)
        if not result:
            gsm_service.restart_disable(3600)
            gsm_service.wait_for_message("RAT",timeout=30)
            gsm_service.gsm_rat()
            result = gsm_service.wait_for_one_of_expected_messages(expected_messages, timeout=5)
            if not result:
                pytest.fail("Expected messages not received after setting auto radio mode.")

        # Check radio_mode
        gsm_service.write('print radio_mode\r\n')
        response = gsm_service.wait_for_message("radio_mode=auto", timeout=5)
        assert response, \
            f"Expected radio_mode={auto_radio_mode} was not set correctly."

        # Check conf_bands
        gsm_service.write('print conf_bands\r\n')
        response = gsm_service.wait_for_all_expected_messages(auto_conf_bands)
        assert response, \
            f"Expected conf_bands={auto_conf_bands} was not set correctly"

        logging.info("Test for setting radio mode to auto completed successfully.")
    except AssertionError as e:
        logging.error(f"Test failed: {e}")
        raise
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise


def test_set_lte_radio_mode_n27(gsm_service):
    """
    Test to verify setting the radio mode to LTE.
    """
    logging.info("Starting test_set_lte_radio_mode_n27")
    try:
        expected_messages = ["LTE", "EDGE", "GPRS"]
        lte_conf_bands = 'LTE2100,LTE1800,LTE900,LTE800,LTE450B31'
        lte_radio_mode = "lte"

        print("Testing setting radio mode to LTE...")
        gsm_service.login_admin()
        gsm_service.write(f"set radio_mode {lte_radio_mode}\n")
        gsm_service.write(f"set conf_bands {lte_conf_bands}\n")

        gsm_service.save()
        gsm_service.reset()
        gsm_service.wait_for_message("Zmiana trybu radiowego na: lte")
        gsm_service.login_admin()
        gsm_service.gsm_rat()
        result = gsm_service.wait_for_one_of_expected_messages(expected_messages, timeout=5)
        if not result:
            gsm_service.restart_disable(3600)
            gsm_service.wait_for_message("RAT",timeout=30)
            gsm_service.gsm_rat()
            result = gsm_service.wait_for_one_of_expected_messages(expected_messages, timeout=5)
            if not result:
                pytest.fail("Expected messages not received after setting lte radio mode.")

        # Check radio_mode
        gsm_service.write('print radio_mode\r\n')
        response = gsm_service.wait_for_message("radio_mode=lte", timeout=5)
        assert response, \
            f"Expected radio_mode={lte_radio_mode} was not set correctly."

        # Check conf_bands
        gsm_service.write('print conf_bands\r\n')
        response = gsm_service.wait_for_all_expected_messages(lte_conf_bands)
        assert response, \
            f"Expected conf_bands={lte_conf_bands} was not set correctly"

        logging.info("Test for setting radio mode to lte completed successfully.")
    except AssertionError as e:
        logging.error(f"Test failed: {e}")
        raise
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise


def test_set_gsm_radio_mode_n27(gsm_service):
    """
    Test to verify setting the radio mode to GSM.
    """
    logging.info("Starting test_set_gsm_radio_mode_n27")
    try:
        expected_messages = ["EDGE", "GPRS"]
        gsm_conf_bands = 'GSM900,GSM1800'
        gsm_radio_mode = "2g"

        print("Testing setting radio mode to GSM...")
        gsm_service.login_admin()
        gsm_service.write(f"set radio_mode {gsm_radio_mode}\n")
        gsm_service.write(f"set conf_bands {gsm_conf_bands}\n")

        gsm_service.save()
        gsm_service.reset()
        gsm_service.wait_for_message("Zmiana trybu radiowego na: 2g")
        gsm_service.login_admin()
        gsm_service.gsm_rat()
        result = gsm_service.wait_for_one_of_expected_messages(expected_messages, timeout=5)
        if not result:
            gsm_service.restart_disable(3600)
            gsm_service.wait_for_message("RAT",timeout=30)
            gsm_service.gsm_rat()
            result = gsm_service.wait_for_one_of_expected_messages(expected_messages, timeout=5)
            if not result:
                pytest.fail("Expected messages not received after setting lte radio mode.")

            # Check radio_mode
        gsm_service.write('print radio_mode\r\n')
        response = gsm_service.wait_for_message("radio_mode=2g", timeout=5)
        assert response, \
            f"Expected radio_mode={gsm_radio_mode} was not set correctly."

        # Check conf_bands
        gsm_service.write('print conf_bands\r\n')
        response = gsm_service.wait_for_all_expected_messages(gsm_conf_bands)
        assert response, \
            f"Expected conf_bands={gsm_conf_bands} was not set correctly"

        logging.info("Test for setting radio mode to lte completed successfully.")
    except AssertionError as e:
        logging.error(f"Test failed: {e}")
        raise
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise


def test_set_pref_bands_to_lte_n27(gsm_service):
    """
    Test to verify setting preferred bands to LTE.
    """
    logging.info("Starting test_set_pref_bands_to_lte_n27")
    try:
        lte_pref_bands = 'LTE2100,LTE1800'

        print("Testing setting preferred bands to LTE...")
        gsm_service.login_admin()
        gsm_service.write(f'set pref_bands {lte_pref_bands}\r\n')

        gsm_service.save()
        gsm_service.reset()
        gsm_service.wait_for_message("Wlaczanie modulu radiowego")

        gsm_service.login_admin()
        gsm_service.write('print pref_bands\r\n')

        # Wait for the response and extract the relevant part
        response = gsm_service.wait_for_message_and_take_value("LCT:", timeout=30)
        read_value = response.split(':')[1].strip().split('\r\n')[0] if response else None

        assert read_value == f"pref_bands={lte_pref_bands}", \
            f"Expected pref_bands={lte_pref_bands}, but got {read_value}"

        logging.info(f"Pref bands are correctly set to {read_value}")
        logging.info("Test for setting preferred bands to LTE completed successfully.")
    except AssertionError as e:
        logging.error(f"Test failed: {e}")
        raise
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise


def test_set_pref_bands_to_2g_n27(gsm_service):
    """
    Test to verify setting preferred bands to 2G.
    """
    logging.info("Starting test_set_pref_bands_to_2g_n27")
    try:
        gsm_pref_bands = 'GSM900,GSM1800'

        print("Testing setting preferred bands to 2G...")
        gsm_service.login_admin()
        gsm_service.write(f'set pref_bands {gsm_pref_bands}\r\n')

        gsm_service.save()
        gsm_service.reset()
        gsm_service.wait_for_message("Wlaczanie modulu radiowego")

        gsm_service.login_admin()
        gsm_service.write('print pref_bands\r\n')

        # Wait for the response and extract the relevant part
        response = gsm_service.wait_for_message_and_take_value("LCT:", timeout=30)
        read_value = response.split(':')[1].strip().split('\r\n')[0] if response else None

        assert read_value == f"pref_bands={gsm_pref_bands}", \
            f"Expected pref_bands={gsm_pref_bands}, but got {read_value}"

        logging.info(f"Pref bands are correctly set to {read_value}")
        logging.info("Test for setting preferred bands to 2G completed successfully.")
    except AssertionError as e:
        logging.error(f"Test failed: {e}")
        raise
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise


def test_tcp_port_change_n27(gsm_service):
    """
    Test to verify changing the TCP port value.
    """
    logging.info("Starting test_tcp_port_change_n27")
    try:
        tcp_port_value = '1234'

        print("Testing changing TCP port value...")
        gsm_service.login_admin()
        print(f"Changing TCP port to {tcp_port_value}")
        gsm_service.write(f"set lct_tcp_port {tcp_port_value}\r\n")
        gsm_service.wait_for_message("LCT: OK")
        gsm_service.save()
        gsm_service.reset()
        gsm_service.wait_for_message("Wlaczanie modulu radiowego")
        gsm_service.login_admin()
        expected_message = "lct_tcp_port=1234"
        gsm_service.write('print lct_tcp_port\r\n')
        result = gsm_service.wait_for_message(expected_message)
        assert result, f"Expected TCP port {expected_message} was not received"

        logging.info("Test for changing TCP port value completed successfully.")
    except AssertionError as e:
        logging.error(f"Test failed: {e}")
        raise
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise
