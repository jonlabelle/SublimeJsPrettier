@echo off
setlocal

set PYTHON=%~1
if defined PYTHON set PATH=%PYTHON%;%PYTHON%\Scripts;%PATH%

set SCRIPTSDIR=%~dp0
pushd "%SCRIPTSDIR%" && pushd ..

echo. > Install pip requirements
pip install -r requirements.txt

echo. > Install npm packages
npm install -g markdownlint-cli

popd && popd
echo.
echo. Finished.
endlocal
