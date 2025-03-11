@echo off

FOR /F "tokens=* USEBACKQ" %%F IN (`powershell -Command "[guid]::NewGuid().ToString()"`) DO (
SET uuid=%%F
)

set BUILD_DIR=%tmp%\ITT-auto-py-to-exe-build-dir_%uuid%
set TMP_CONFIG_PATH=%tmp%\auto-py-to-exe-config.json

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

goto :eof

:set_line
set line=!line:%%path%%=%newpath%!
echo !line! >> %TMP_CONFIG_PATH%

:eof