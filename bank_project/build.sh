#!/usr/bin/env bash

# exit on error

set -o errexit
pip install -r bank_project/requirements.txt
python bank_project/manage.py collectstatic --no-input
python bank_project/manage.py migrate