@echo off
setlocal

set PYTHON=%~1
set PATH=%PYTHON%;%PYTHON%\Scripts;%PATH%

::
:: cd to project root and install dev/test dependencies
::

set SCRIPTSDIR=%~dp0

pushd "%SCRIPTSDIR%"
pushd ..

pip install -r requirements.txt

popd
popd

endlocal
