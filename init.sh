#!/bin/bash

if python3 -m venv -h > /dev/null 2>&1
then
  echo "virtualenv is installed to create venv for python"
else
  pip3 install virtualenv
  echo "virtualenv has been installed"
fi

if ls "venv" > /dev/null 2>&1
then
  echo "Python virtual-env still available"
else
  python3 -m venv ./venv
  echo "Python venv has been created"
fi

source venv/bin/activate
pip install -r requirements.txt
echo "Python venv has been installed with requirements.txt"
