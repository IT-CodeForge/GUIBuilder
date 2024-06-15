@echo off

set PYTHON_BIN="C:\Python"
set FILE_GET_PIP="%PYTHON_BIN%\get-pip.py"

goto main

REM --------------------------------------------
:warteBisGetPipExistiert
:WAIT_LOOP
  IF NOT EXIST %FILE_GET_PIP% (
    TIMEOUT /T 1 /NOBREAK > NUL
	echo waiting...
    GOTO WAIT_LOOP
  )
goto :eof

REM --------------------------------------------
:pipNeuInstallieren
  curl https://bootstrap.pypa.io/get-pip.py -o %FILE_GET_PIP%
  call :warteBisGetPipExistiert
  
  call "%PYTHON_BIN%\python.exe" %FILE_GET_PIP%
goto :eof

REM --------------------------------------------
:pipUpgraden
  pip install --upgrade pip
goto :eof

REM --------------------------------------------
:requirementsInstallieren
  pip install --upgrade --upgrade-strategy eager -r requirements.txt
goto :eof

REM --------------------------------------------


:main
if not exist "%PYTHON_BIN%\python.exe" (
  echo "Missing Python installed at %PYTHON_BIN%
  pause
  goto :eof
)

if not exist %FILE_GET_PIP% (
  call :pipNeuInstallieren
)
call :pipUpgraden
call :requirementsInstallieren

set PYTHONPATH=.\Moduldateien;.\benoetigte_Dateien
code . 
