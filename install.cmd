@echo off

set PYTHON=%~1
set PATH=%PYTHON%;%PYTHON%\Scripts;%PATH%

python -m pip install -r requirements.txt
