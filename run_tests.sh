#!/usr/bin/env bash

set -e
set -x

###
# Testing Requirements
#
#   pip install flake8
#   pip install flake8_docstrings
#   pip install pytest
###

py.test .
flake8 .
