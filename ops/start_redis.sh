#!/bin/bash

# stop previously running container 
docker container ls | grep redis_server:0.0.1 | awk '{print $1}' | xargs docker stop

# start redis-server docker image
docker run -d -p 2728:2728 redis_server:0.0.1
