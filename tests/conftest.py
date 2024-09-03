def pytest_addoption(parser):
    parser.addoption(
        "--serial-config",
        action="store",
        default="../../common/config_file.txt",
        help="Path to the serial configuration file",
    )