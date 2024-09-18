This project performs serial communication with external devices using pytest to manage tests and log the results.

Prerequisites
Python 3.x installed on your system
Make sure you download requirements.txt
pytest installed:
bash
pip install pytest
Ensure that your serial device is connected and that you know the correct COM port (e.g., COM1, COM3).

Configuration
Before running the tests, you need to configure the serial port settings in the configuration file located at:

bash
/common/config_file.txt
Example Configuration:
ini

[serial]
port = COM1              # Set this to the actual device port (e.g., COM3 on Windows, /dev/ttyUSB0 on Linux)

Update the port field to match the actual serial port on your machine (e.g., COM1, COM3, or /dev/ttyUSB0 for Linux).
Running Tests
The tests are located in the /tests directory and are managed using pytest. A batch script is provided to easily execute tests with the correct configuration files.

How to Run the Tests:
Navigate to the Project Directory:

Open a terminal or command prompt and navigate to the project’s root directory.

Update the Batch Script Path:

The provided batch script (run_tests.bat) is located in the root of the project. Before running the tests, ensure that the path inside the script points to the correct location of the tests.

In the batch file (run_tests.bat), adjust the paths if necessary:

batch
@echo off

REM Navigate to the target directory
cd /d "C:\Users\dgtla\PycharmProjects\Tram_testy\tram_testy\tests\"

REM Run pytest with the first config file and log everything
start "" cmd /c pytest --serial-config=../common/config_file.txt --tb=short --log-cli-level=DEBUG --log-file=pytest_output_1.log
Execute the Batch Script:

To run the tests, simply execute the batch script in the command prompt:

bash
run_tests.bat
The script will:

Navigate to the test directory
Run pytest with the specified config file
Log the output to pytest_output_1.log
Optional: Running Tests with Multiple Configurations
If you have multiple configurations, you can modify the batch script to run pytest with different config files. For example, uncomment and edit the following lines to use config_file_3.txt:

batch
REM Run pytest with the second config file and log everything
REM start "" cmd /c pytest --serial-config=../common/config_file_3.txt --tb=short --log-cli-level=DEBUG --log-file=pytest_output_1.log --reruns 3
Pause
At the end of the script, the pause command is used to keep the terminal window open after pytest completes, allowing you to review the results before the window closes.

Troubleshooting
Make sure the correct serial port is set in the config file.
If tests fail to run, ensure all dependencies (such as pytest) are installed and your serial device is properly connected.
