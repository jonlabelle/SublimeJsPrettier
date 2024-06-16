@echo off
setlocal

set PYTHON=%~1
if defined PYTHON set PATH=%PYTHON%;%PYTHON%\Scripts;%PATH%
set SCRIPTSDIR=%~dp0

pushd "%SCRIPTSDIR%" && pushd ..

echo.
echo. > Run pytest
pytest .

echo.
echo. > Run flake8
flake8 . --count --show-source --statistics

echo.
echo. > Run pylint
pylint .

echo.
echo. > Run markdownlint
markdownlint-cli2 .

popd && popd
echo.
echo. Finished.
endlocal
