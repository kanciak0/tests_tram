# import pytest
# from tester_tram.common.Service import SerialService
#
# @pytest.fixture
# def serial_service():
#     # Initialize SerialService without needing a config file
#     service = SerialService(config_file='config.txt')  # Adjust the path if necessary
#     yield service
#     service.close()
#
#
# def test_set_pin(pin_manager):
#     print("Testing setting PIN...")
#     result = pin_manager.set_pin()
#     assert result == (['PIN OK'], 'PIN')
#     print("Test for setting PIN completed successfully.")
#
#
# def test_check_pin(pin_manager):
#     print("Testing checking PIN...")
#     pin_manager.check_pin()
#     print("Test for checking PIN completed successfully.")
