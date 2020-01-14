#!/usr/bin/env bash

image_name=redis_server
image_tag=0.0.1

# create docker image
docker build -t $image_name:$image_tag .
