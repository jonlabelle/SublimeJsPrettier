@echo off
setlocal

set PYTHON=%~1
if defined PYTHON set PATH=%PYTHON%;%PYTHON%\Scripts;%PATH%

set SCRIPTSDIR=%~dp0

echo.
echo. > Run tests
echo.

pushd "%SCRIPTSDIR%" && pushd ..
py.test .
flake8 .
pylint JsPrettier.py
markdownlint .
popd && popd

echo.
echo. Finished.
echo.

endlocal
