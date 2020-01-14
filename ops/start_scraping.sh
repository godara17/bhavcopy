#!/bin/bash

# stop previously running container 
docker container ls | grep scraping:0.0.1 | awk '{print $1}' | xargs docker stop

redis_host=$(hostname -I | (cut -d" " -f1))
redis_port=2728
# start scraping docker image
docker run -d -e REDIS_HOST=$redis_host -e REDIS_PORT=$redis_port scraping:0.0.1
