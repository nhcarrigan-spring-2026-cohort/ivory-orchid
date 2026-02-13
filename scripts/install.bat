::Script to install Python, create a virtual environment and install dependencies
::Any argument passed will be passed to the venv command

@echo off
where python >nul 2>&1
if errorlevel 1 goto :installPy
python -h >nul 2>&1
if errorlevel 1 goto :installPy

:afterPy
::ensure pip and venv are installed
python -m pip -h >nul 2>&1
if errorlevel 1 goto :brokenInstallation
python -m venv -h >nul 2>&1
if errorlevel 1 goto :brokenInstallation

::make make sure we are in the project root
cd %~dp0\..

cd backend
::create and enable venv
cd .venv >nul 2>&1
if errorlevel 1 ( python -m venv .venv %1 ) else cd ..
call .venv\Scripts\activate.bat

::install dependencies
pip install -r requirements.txt >nul
cd ..

call backend\.venv\Scripts\deactivate.bat

echo Installation completed
goto :EOF

:installPy
echo Installing Python 3.13
winget install --id=Python.Python.3.13 --source=winget
if errorlevel 1 ( echo Python installed succesfully ) else goto :pyErr
python -h >nul 2>&1
if "%errorlevel%"=="0" goto afterPy
echo python was installed succesfully, but it was not found in PATH
please try to rerun the script or restart the cmd instance
pause
exit /b 1
goto :EOF

:pyErr
echo There was an issue while installing python >&2
echo please check your internet connection >&2 
echo python NOT installed
pause
exit /b 1
goto :EOF

:brokenInstallation
echo Installation failed: >&2
python -m pip -h >nul 2>&1
if errorlevel 1 echo pip is not installed >&2
python -m venv -h >nul 2>&1
if errorlevel 1 echo venv is not installed >&2
echo Please install them manually>2
echo. >&2
echo The installation of python has failed.
pause
exit /b 1
