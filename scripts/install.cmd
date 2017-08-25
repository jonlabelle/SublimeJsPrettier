@echo off
setlocal

set PYTHON=%~1
if defined PYTHON set PATH=%PYTHON%;%PYTHON%\Scripts;%PATH%

set SCRIPTSDIR=%~dp0

echo.
echo. > Install package dependencies
echo.

pushd "%SCRIPTSDIR%" && pushd ..
pip install -r requirements.txt
npm install -g markdownlint-cli
popd && popd

echo.
echo. Finished.
echo.

endlocal
