#!/bin/bash

BASE_DIR=$(dirname "$0")
cd $BASE_DIR
source venv/bin/activate
test -d logs || mkdir "logs"
python users.py > logs/users.log 2> logs/users.errors &
echo "service users started with pid $!"
python offers.py > logs/offers.log 2> logs/offers.errors &
echo "service offers started with pid $!"
