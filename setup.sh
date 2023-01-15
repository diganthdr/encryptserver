#!/bin/bash    

# pre-requisite: python 3.9.4

# set up virtual environment
python -m venv dev-venv

# activate virtual environment
source dev-venv/bin/activate

# install dependencies 
pip3 install -r requirements.txt

# run unit tests on server
cd server; python -m unittest discover
cd ..

echo "SETUP done!"

# TODO: export paths
# export PATH=$PATH:

# run unit tests on client (non integration test)
# TODO: At the moment, this requires server and client running.