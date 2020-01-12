# This project is about fetching equity bhai copy data from bse and enables 
# search results on the web page using cherrypy

# How to Use it?
# clone the repo

# run setup.sh
/bin/bash setup.sh

# setup.sh will include setup of python3, pip3, virtaulenv, redis and pythons
# required packages along with cronsetup for data fetching scripts.

# go to ops directory
# run start_scraping.sh(if you want to run scraping script to run manually, otherwise cron will run it by default)

# run start_server.sh script for starting your server.
/bin/bash start_server.sh

# go to ip:port/ for see the magic.

# cheers!!