import pytest

from common.Service import APNService


@pytest.fixture(scope='module')
def apn_service(request):
    """
    Fixture to initialize and provide the SerialService instance for the tests.
    """
    config_file = request.config.getoption("--serial-config")
    apn_service = APNService(config_file=config_file,test_file_name="log_test_apn_n27")
    yield apn_service
    apn_service.close()


# @pytest.fixture(scope='module')
# def gsm_service():
#     gsm_service = GSMService(config_file='config.txt')
#     yield gsm_service
#     gsm_service.close()


@pytest.fixture(scope="module", autouse=True)
def radio_setup_n27(apn_service):
    """
    Fixture to ensure the radio module N27 is active and properly initialized.
    """
    apn_service.login_admin()
    apn_service.gsm_ver()
    expected_radio = apn_service.wait_for_message("N27",timeout=5)
    if expected_radio is False:
        apn_service.set_active_radio(radio_id=1)
        apn_service.save()
        apn_service.reset()
        apn_service.wait_for_message("Modul radiowy poprawnie wykryty i zainicjowany")
        apn_service.login_admin()
        apn_service.gsm_ver()
        expected_radio = apn_service.wait_for_message("N27")
        if expected_radio is False:
            pytest.fail("Nie przelaczono na poprawny modul radiowy")
    yield


def test_set_apn_name(apn_service):
    """
    Test to verify setting and retrieving the APN name.
    """
    apn_service.login_admin()
    apn_name = "vpn.static.pl"
    apn_service.set_apn_name(apn_name)

    # Verify the APN name was set correctly
    apn_service.print_apn()
    expected_message = f"apn_name={apn_name}"

    result = apn_service.wait_for_message(expected_message)
    assert result, f"Expected APN name '{expected_message}' was not received."


def test_set_apn_login(apn_service):
    """
    Test to verify setting and retrieving the APN login.
    """
    apn_service.login_admin()
    apn_login = "ppp"
    assert len(apn_login) <= 32, "APN login exceeds maximum length"
    apn_service.set_apn_login(apn_login)

    # Verify the APN login was set correctly
    apn_service.print_apn()
    expected_message = f"apn_login={apn_login}"

    result = apn_service.wait_for_message(expected_message)
    assert result, f"Expected APN login '{expected_message}' was not received."


def test_set_apn_password(apn_service):
    """
    Test to verify setting and retrieving the APN password.
    """
    apn_service.login_admin()
    apn_passwd = "ppp"
    assert len(apn_passwd) <= 32, "APN password exceeds maximum length"

    apn_service.set_apn_passwd(apn_passwd)

    # Verify the APN password was set correctly
    apn_service.print_apn()
    expected_message = f"apn_passwd={apn_passwd}"

    result = apn_service.wait_for_message(expected_message)
    assert result, f"Expected APN password '{expected_message}' was not received."


def test_set_apn_auth(apn_service):
    """
    Test to verify setting and retrieving the APN authentication method.
    """
    apn_service.login_admin()
    apn_auth = "pap"
    valid_auth_methods = ["pap", "chap", "none"]
    assert apn_auth in valid_auth_methods, f"APN auth '{apn_auth}' is not valid"
    assert len(apn_auth) <= 16, "APN auth method exceeds maximum length"
    apn_service.set_apn_auth(apn_auth)

    # Verify the APN authentication method was set correctly
    apn_service.print_apn()
    expected_message = f"apn_auth={apn_auth}"

    result = apn_service.wait_for_message(expected_message)
    assert result, f"Expected APN authentication method '{expected_message}' was not received."


def test_set_apn_tries(apn_service):
    """
    Test to verify setting and retrieving the APN tries parameter.
    """
    apn_service.login_admin()
    apn_tries = 8

    assert 4 <= apn_tries <= 360, "APN tries value must be between 4 and 360"

    apn_service.set_apn_tries(apn_tries)

    # Verify the APN tries parameter was set correctly
    apn_service.print_apn()
    expected_message = f"apn_tries={apn_tries}"

    result = apn_service.wait_for_message(expected_message)
    assert result, f"Expected APN tries parameter '{expected_message}' was not received."




