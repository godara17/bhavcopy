#!/bin/bash

# This file is responsible for docker setup and creating docker images

# setup docker
cd setup

/bin/bash docker_setup.sh

cd ..

/bin/bash create_images.sh
