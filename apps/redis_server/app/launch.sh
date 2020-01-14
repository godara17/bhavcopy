#!/bin/bash

# redis.Redis(host="machine ip address", port=2728, password="redis@54321", db=0)
# docker run -d -p 2728:2728  redis_server:0.0.1
while true
do
    if [[ $(ps -ef | grep redis-server| grep -v grep) ]]
    then
        echo ""
    else
        echo "starting redis-server"
        redis-server 2728.conf
    fi
    sleep 30s
done

