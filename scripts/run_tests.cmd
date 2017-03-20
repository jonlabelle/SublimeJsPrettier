@echo off
setlocal

set PYTHON=%~1
set PATH=%PYTHON%;%PYTHON%\Scripts;%PATH%

::
:: cd to project root and run tests
::

set SCRIPTSDIR=%~dp0
pushd "%SCRIPTSDIR%" && pushd ..

pytest .
flake8 .
markdownlint .

popd && popd
endlocal
