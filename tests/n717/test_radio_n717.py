import pytest

from common.Service import GSMService


@pytest.fixture(scope='module')
def gsm_service(request):
    config_file = request.config.getoption("--serial-config")
    service = GSMService(config_file=config_file, test_file_name="log_test_radio_n717")
    yield service
    service.close()


def test_set_auto_radio_mode_n717(gsm_service):
    print("Testing setting radio mode to auto...")
    expected_messages = ["LTE","EDGE","GPRS"]
    auto_conf_bands = 'GSM900,GSM1800,LTE2100,LTE1800,LTE900,LTE800,LTE450B31'
    auto_radio_mode = "auto"
    gsm_service.login_admin()
    gsm_service.write(f"set radio_mode {auto_radio_mode}\n")
    gsm_service.write(f"set conf_bands {auto_conf_bands}\n")

    gsm_service.save()
    gsm_service.reset()
    gsm_service.wait_for_message("Zmiana trybu radiowego na: auto")
    gsm_service.login_admin()
    gsm_service.gsm_rat()
    result = gsm_service.wait_for_one_of_expected_messages(expected_messages, timeout=5)
    if result is False:
        pytest.fail()
    gsm_service.write('print radio_mode\r\n')
    response = gsm_service.wait_for_message_and_take_value("LCT:", timeout=30)
    read_value = response.split(':')[1].strip().split('\r\n')[0] if response else None
    assert read_value == f"radio_mode={auto_radio_mode}", \
        f"Expected radio_mode={auto_radio_mode}, but got {read_value}"
    gsm_service.write('print conf_bands\r\n')
    response = gsm_service.wait_for_message_and_take_value("LCT:", timeout=30)
    read_value = response.split(':')[1].strip().split('\r\n')[0] if response else None
    assert read_value == f"conf_bands={auto_conf_bands}", \
        f"Expected conf_bands={auto_conf_bands}, but got {read_value}"
    

    print("Test for setting radio mode to auto completed successfully.")


def test_set_lte_radio_mode_n717(gsm_service):
    print("Testing setting radio mode to auto...")
    expected_messages = ["LTE", "EDGE", "GPRS"]
    lte_conf_bands = 'LTE2100,LTE1800,LTE900,LTE800,LTE450B31'
    lte_radio_mode = "lte"
    gsm_service.login_admin()
    gsm_service.write(f"set radio_mode {lte_radio_mode}\n")
    gsm_service.write(f"set conf_bands {lte_conf_bands}\n")

    gsm_service.save()
    gsm_service.reset()
    gsm_service.wait_for_message("Zmiana trybu radiowego na: lte")
    gsm_service.login_admin()
    gsm_service.wait_for_message("RAT")
    gsm_service.gsm_rat()
    result = gsm_service.wait_for_one_of_expected_messages(expected_messages, timeout=5)
    if result is False:
        pytest.fail()
    gsm_service.write('print radio_mode\r\n')
    response = gsm_service.wait_for_message_and_take_value("LCT:", timeout=30)
    read_value = response.split(':')[1].strip().split('\r\n')[0] if response else None
    assert read_value == f"radio_mode={lte_radio_mode}", \
        f"Expected radio_mode={lte_radio_mode}, but got {read_value}"
    gsm_service.write('print conf_bands\r\n')
    response = gsm_service.wait_for_message_and_take_value("LCT:", timeout=30)
    read_value = response.split(':')[1].strip().split('\r\n')[0] if response else None
    assert read_value == f"conf_bands={lte_conf_bands}", \
        f"Expected conf_bands={lte_conf_bands}, but got {read_value}"

    print("Test for setting radio mode to auto completed successfully.")


def test_set_gsm_radio_mode_n717(gsm_service):
    print("Testing setting radio mode to auto...")
    expected_messages = ["EDGE", "GPRS"]
    gsm_conf_bands = 'GSM900,GSM1800'
    gsm_radio_mode = "2g"
    gsm_service.login_admin()
    gsm_service.write(f"set radio_mode {gsm_radio_mode}\n")
    gsm_service.write(f"set conf_bands {gsm_conf_bands}\n")

    gsm_service.save()
    gsm_service.reset()
    gsm_service.wait_for_message("Zmiana trybu radiowego na: 2g")
    gsm_service.login_admin()
    gsm_service.wait_for_message("RAT")
    gsm_service.gsm_rat()
    result = gsm_service.wait_for_one_of_expected_messages(expected_messages, timeout=5)
    if result is False:
        pytest.fail()
    gsm_service.write('print radio_mode\r\n')
    response = gsm_service.wait_for_message_and_take_value("LCT:", timeout=30)
    read_value = response.split(':')[1].strip().split('\r\n')[0] if response else None
    assert read_value == f"radio_mode={gsm_radio_mode}", \
        f"Expected radio_mode={gsm_radio_mode}, but got {read_value}"
    gsm_service.write('print conf_bands\r\n')
    response = gsm_service.wait_for_message_and_take_value("LCT:", timeout=30)
    read_value = response.split(':')[1].strip().split('\r\n')[0] if response else None
    assert read_value == f"conf_bands={gsm_conf_bands}", \
        f"Expected conf_bands={gsm_conf_bands}, but got {read_value}"

    print("Test for setting radio mode to auto completed successfully.")

#TODO: ASK ABOUT THESE TESTS, PREF_BANDS_CONF= NEVER ASSIGNING


def test_set_pref_bands_to_lte_n717(gsm_service):
    print("Testing setting preferred bands to LTE...")
    lte_pref_bands = 'LTE2100,LTE1800'
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

    # Print a confirmation message if the preferred bands are set correctly
    print(f"Pref bands are correctly set to {read_value}")

    print("Test for setting preferred bands to LTE completed successfully.")


def test_set_pref_bands_to_2g_n717(gsm_service):
    print("Testing setting preferred bands to LTE...")
    gsm_pref_bands = 'GSM900,GSM1800'
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

    # Print a confirmation message if the preferred bands are set correctly
    print(f"Pref bands are correctly set to {read_value}")

    print("Test for setting preferred bands to LTE completed successfully.")


def test_tcp_port_change_n717(gsm_service):
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
    assert result, f"expected tcp port {expected_message} was not received"
    print("Test for changing TCP port value completed successfully.")
