#!/bin/bash


# stop previously running container 
docker container ls | grep cherry_server:0.0.1 | awk '{print $1}' | xargs docker stop

redis_host=$(hostname -I | (cut -d" " -f1))
redis_port=2728
# start server docker image
docker run -d -e REDIS_HOST=$redis_host -e REDIS_PORT=$redis_port -p 2729:2729 cherry_server:0.0.1
