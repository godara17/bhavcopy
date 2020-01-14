#!/usr/bin/env bash

image_name=scraping
image_tag=0.0.1

# copy common and utils inside app directory
cp -rf ../../src/common app/.
cp -rf ../../src/utils app/.

# create docker image
docker build -t $image_name:$image_tag .

# remove common and utils once image is created
rm -rf app/common
rm -rf app/utils
