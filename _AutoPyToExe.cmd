:: V1.3

@echo off

FOR /F "tokens=* USEBACKQ" %%F IN (`powershell -Command "[guid]::NewGuid().ToString()"`) DO (
SET uuid=%%F
)

set GLOBAL_BUILD_DIR=%tmp%\ITT-auto-py-to-exe-build-dir
set BUILD_DIR=%GLOBAL_BUILD_DIR%\%uuid%
set TMP_CONFIG_PATH=%tmp%\auto-py-to-exe-config_%uuid%.json
set TMP_WINDOWS_DEFENDER_SCRIPT_PATH=%tmp%\ITT-add_windows_defender_exclusion_%uuid%.cmd

:: Create the Windows Defender exclusion script
echo @echo off > %TMP_WINDOWS_DEFENDER_SCRIPT_PATH%
echo :: Use the passed PATH variable >> %TMP_WINDOWS_DEFENDER_SCRIPT_PATH%
echo set "DIR_PATH=%GLOBAL_BUILD_DIR%" >> %TMP_WINDOWS_DEFENDER_SCRIPT_PATH%
echo. >> %TMP_WINDOWS_DEFENDER_SCRIPT_PATH%
echo :: Check if the script is running as Admin >> %TMP_WINDOWS_DEFENDER_SCRIPT_PATH%
echo net session ^>nul 2^>^&1 >> %TMP_WINDOWS_DEFENDER_SCRIPT_PATH%
echo if %%errorlevel%% neq 0 ( >> %TMP_WINDOWS_DEFENDER_SCRIPT_PATH%
echo     echo This script requires administrative privileges. >> %TMP_WINDOWS_DEFENDER_SCRIPT_PATH%
echo     echo Requesting elevation... >> %TMP_WINDOWS_DEFENDER_SCRIPT_PATH%
echo     powershell -Command "Start-Process '%%~f0' -Verb RunAs" >> %TMP_WINDOWS_DEFENDER_SCRIPT_PATH%
echo     exit /b >> %TMP_WINDOWS_DEFENDER_SCRIPT_PATH%
echo ) >> %TMP_WINDOWS_DEFENDER_SCRIPT_PATH%
echo. >> %TMP_WINDOWS_DEFENDER_SCRIPT_PATH%
echo :: Add the directory to Windows Defender exclusions >> %TMP_WINDOWS_DEFENDER_SCRIPT_PATH%
echo echo Adding %%DIR_PATH%% to Windows Defender exclusions... >> %TMP_WINDOWS_DEFENDER_SCRIPT_PATH%
echo powershell -Command "Add-MpPreference -ExclusionPath '%%DIR_PATH%%'" >> %TMP_WINDOWS_DEFENDER_SCRIPT_PATH%
echo. >> %TMP_WINDOWS_DEFENDER_SCRIPT_PATH%
echo if %%errorlevel%% equ 0 ( >> %TMP_WINDOWS_DEFENDER_SCRIPT_PATH%
echo     echo Successfully added %%DIR_PATH%% to Windows Defender exclusion list. >> %TMP_WINDOWS_DEFENDER_SCRIPT_PATH%
echo ) else ( >> %TMP_WINDOWS_DEFENDER_SCRIPT_PATH%
echo     echo Failed to add %%DIR_PATH%% to Windows Defender exclusion list. >> %TMP_WINDOWS_DEFENDER_SCRIPT_PATH%
echo ) >> %TMP_WINDOWS_DEFENDER_SCRIPT_PATH%

setlocal EnableDelayedExpansion

call _start_CMD.cmd NO_CMD

cls

pip install --upgrade --upgrade-strategy eager auto-py-to-exe

set FILENAME=
IF EXIST .\src\main.py (
	set FILENAME="%cd%\src\main.py"
) ELSE (
	IF EXIST .\src\main.pyw (
		set FILENAME="%cd%\src\main.pyw"
	)
)

IF NOT EXIST %GLOBAL_BUILD_DIR% (
	mkdir %GLOBAL_BUILD_DIR%
	cmd /c "%TMP_WINDOWS_DEFENDER_SCRIPT_PATH%"
)

rmdir /S /Q %BUILD_DIR%
mkdir %BUILD_DIR%
robocopy . "%BUILD_DIR%" /s /e /XD ".venv" ".git" ".svn"



IF EXIST .\auto-py-to-exe.json (
	set newpath=!cd:\=/!
	del /f %TMP_CONFIG_PATH%
	for /f "tokens=*" %%i in (.\auto-py-to-exe.json) do (
		set line=%%i
		call :set_line
	)

	cls
	auto-py-to-exe -lang de -c "%TMP_CONFIG_PATH%" -bdo "%BUILD_DIR%" -o "%cd%\build" %FILENAME%
) ELSE (
	cls
	auto-py-to-exe -lang de -bdo "%BUILD_DIR%" -o "%cd%\build" %FILENAME%
)

rmdir /S /Q %BUILD_DIR%
del /f %TMP_CONFIG_PATH%
del /f %TMP_WINDOWS_DEFENDER_SCRIPT_PATH%

goto :eof

:set_line
set line=!line:%%path%%=%newpath%!
echo !line! >> %TMP_CONFIG_PATH%

:eof