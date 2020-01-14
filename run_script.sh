#!/bin/bash

# Here we will run our docker images

cd ops

# start redis
/bin/bash start_redis.sh

# start scraping
/bin/bash start_scraping.sh

# start server
/bin/bash start_server.sh

# set cron for scraping
sudo /bin/bash set_scraping_cron.sh
