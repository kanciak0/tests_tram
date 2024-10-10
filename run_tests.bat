@echo off
REM Navigate to the target directory
cd /d "C:\Users\dgtla\PycharmProjects\tests_tram\tests"

REM Start a new command prompt window to activate the virtual environment and run pytest
start cmd /k "call ..\venv\Scripts\activate && pytest --serial-config=../common/config_file.txt --tb=short --log-cli-level=DEBUG --log-cli-date-format= --log-file=pytest_output_1.log"

REM Pause to keep the original command window open
pause