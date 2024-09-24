@echo off

REM Navigate to the target directory
cd /d "C:\Users\dgtla\PycharmProjects\tests_tram\tests"

REM Run pytest with the first config file and log everything
start "" cmd /c pytest --serial-config=../common/config_file.txt --tb=short --log-cli-level=DEBUG --log-cli-date-format= --log-file=pytest_output_1.log


REM Run pytest with the second config file and log everything
REM start "" cmd /c pytest --serial-config=../common/config_file_3.txt --tb=short --log-cli-level=DEBUG --log-cli-date-format= --log-file=pytest_output_1.log --reruns 3

REM Pause to keep the original command window open
pause

