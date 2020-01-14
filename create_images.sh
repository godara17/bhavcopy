#!/bin/bash

cd apps
# create images

# create redis image
cd redis_server
/bin/bash create_image.sh
cd -

# create scraping image
cd scraping
/bin/bash create_image.sh
cd -

# create server image
cd server
/bin/bash create_image.sh
