@echo off

REM Navigate to the target directory
cd /d "C:\Users\dgtla\PycharmProjects\Tram_testy\tram_testy\tests\n27"

REM Run pytest with the first config file in a new process
start "" cmd /c pytest --serial-config=../../common/config_file.txt

REM Run pytest with the second config file in another new process
start "" cmd /c pytest --serial-config=../../common/config_file_3.txt

REM (Optional) Pause to keep the original command window open
pause