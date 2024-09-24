#!/bin/bash

# Navigate to the target directory
cd /opt/Tram_test/tests_tram/tests || exit

# Run pytest with the first config file and log everything
pytest --serial-config=../common/config_file.txt --tb=short --log-cli-level=DEBUG --log-cli-date-format= --log-file=pytest_output_1.log &

# Run pytest with the second config file and log everything
#pytest --serial-config=../common/config_file_3.txt --tb=short --log-cli-level=DEBUG --log-cli-date-format= --log-file=pytest_output_3.log &

wait
# Keep the terminal open (if running manually, remove this line for automation)
read -p "Both tests finished. Press Enter to continue..."