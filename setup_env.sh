#!/bin/sh
# This script automates the creation of Python virtual environment.
#install venv

if [ -d "virtualenv" ]; then
    echo "Virtual environment 'virtualenv' found, activating it."
else
    echo "Virtual environment not found, creating new 'virtualenv'."
    pip3 install virtualenv
    virtualenv virtualenv
    if [ $? -eq 0 ]; then
        echo "Virtual environment was successfully created."
    else
        echo "Virtual environment was NOT created, aborting."
        exit 1
    fi
fi

source virtualenv/bin/activate
if [ $? -eq 0 ]; then
    echo "Virtual environment is successfully activated."
else
    echo "Virtual environment was NOT activated, aborting."
    exit 1
fi

echo "Installing required packages."
pip3 install -r requirements.txt
if [ $? -eq 0 ]; then
    echo "All requirements were successfully installed."
else
    echo "Requirements were NOT installed properly, aborting."
    exit 1
fi
# Execute for run
echo "Configuring for the correct execution"
python3 manage.py makemigrations users
python3 manage.py makemigrations academic
python3 manage.py migrate users
python3 manage.py migrate academic
python3 manage.py migrate
python3 manage.py runserver

echo "Done!!."