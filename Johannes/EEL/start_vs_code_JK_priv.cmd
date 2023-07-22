@echo off

SET SCRIPT_LOCATION=%cd%
set PYTHONPATH=
set DEV=True
python -m pip install --upgrade pip
pip install -r requirements.txt
cd /D "C:\Users\Johannes\Desktop\Johannes seine Programme\VSCode_Portable"
cmd /c start Code.exe %SCRIPT_LOCATION%
exit