@echo off
cd %~dp0\..\backend

call .\.venv\Scripts\activate
coverage run --source app,test -m pytest test

echo Saving report as html file in %cd%\htmlcov
coverage html

echo Clearing up...
call .\.venv\Scripts\deactivate
