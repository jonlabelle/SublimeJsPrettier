set PYTHON=%~1
set PATH=%PYTHON%;%PYTHON%\Scripts;%PATH%

pytest
flake8
