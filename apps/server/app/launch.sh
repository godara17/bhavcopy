#!/bin/bash

export BASE_PATH="$(pwd)"

while true
do
    if [[ $(ps -ef | grep bhav_server| grep -v grep) ]]
    then
        echo ""
    else
        echo "starting redis-server"
        python3 bhav_server.py
    fi
    sleep 30s
done
