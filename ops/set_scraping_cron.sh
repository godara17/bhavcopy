#!/bin/bash

# setup crontab
file='/var/spool/cron/crontabs/'$(whoami)
cp scraping_crontab $file
chmod 600 -R $file
chown -R $(whoami):crontab $file

# restart cron service
sudo service cron restart
