# The Dockerized project for Equity Bhav Copy

This project contains 3 docker applications for redis, scraping and server
Instruction For running the project(Assuming you have ubuntu machine)
1. clone/download the repo
2. run setup.sh script
    /bin/bash setup.sh or ./setup.sh
    This above command will setup docker(for ubuntu only)

    Once docker is up and running, setup script will call create_images.sh script automatically
3. run create_images.sh (This step will be executed automatically above step)
    if you wish to run it manually
    /bin/bash create_images.sh
4. run run_script.sh
    This script will run redis, scraping and server docker images and will as well set the cron for scraping.
    /bin/bash run_script.sh

The above step will create containers for our 3 apps redis, scraping and server.

redis will be running on port 2728
Server will be running on port 2729

# cheers!!