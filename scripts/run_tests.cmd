@echo off
setlocal

set PYTHON=%~1
if defined PYTHON set PATH=%PYTHON%;%PYTHON%\Scripts;%PATH%
set SCRIPTSDIR=%~dp0

pushd "%SCRIPTSDIR%" && pushd ..

echo.
echo. > Run pytest
py.test .

echo.
echo. > Run flake8
flake8 .

echo.
echo. > Run pylint
pylint JsPrettier.py

echo.
echo. > Run markdownlint
markdownlint .

popd && popd

echo.
echo. Finished.
endlocal
