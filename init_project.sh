#!/bin/bash

if python -m venv -h > /dev/null 2>&1
then
  echo "virtualenv is installed to create venv for python"
else
  pip install virtualenv
  echo "virtualenv has been installed"
fi

if ls "venv" > /dev/null 2>&1
then
  echo "Python venv available"
  source venv/bin/activate
else
  python -m venv ./venv
  pip install -r requirements.txt
  source venv/bin/activate
  echo "Python venv has been installed with requirements.txt"
fi