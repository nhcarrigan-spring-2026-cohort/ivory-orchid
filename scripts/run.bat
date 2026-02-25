::Script to run the webserver
::Any argument passed will be passed to flask

@echo off
cd %~dp0\..\backend

call .\.venv\Scripts\activate

echo Starting server
echo To stop the server press CTRL+C, if a message appears saying "Interrupt batch script" enter 'N'
flask --app=app run %*

echo Clearing up...
call .\.venv\Scripts\deactivate
