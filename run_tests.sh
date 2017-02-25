#!/usr/bin/env bash

set -e
set -x

py.test .
flake8 .
