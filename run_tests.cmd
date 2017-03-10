@echo off

set PYTHON=%~1
set PATH=%PYTHON%;%PYTHON%\Scripts;%PATH%

python -m pytest
python -m flake8
