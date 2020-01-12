import sys
import os

BASE_PATH = os.getenv("BASE_PATH")
sys.path.append(BASE_PATH)

from common.equity_bhav_cp_db_mgmt import EquityBhavCopyDBManager
from utils import LoggerUtility

from bs4 import BeautifulSoup
from datetime import datetime
import zipfile
import requests
import json
import csv

log_data = dict(
    logging_conf=BASE_PATH + "/utils/conf/logging.conf",
    log_file=BASE_PATH + "/logs/app_logs.log",
)
logger = LoggerUtility(log_data).logger

HOME_URL = "https://www.bseindia.com/markets/MarketInfo/BhavCopy.aspx"


class EquityBhavCopyScrapingManager:
    def __init__(self):
        self.bse_downloads = os.getcwd() + "/bse_downloads/"
        self.zip_file = "daily_equity.zip"
        if not os.path.isdir(self.bse_downloads):
            os.mkdir(self.bse_downloads)

    def get_soup_object(self, resp):
        return BeautifulSoup(resp.text, "html.parser")

    def start_scraping(self):
        data = []
        try:
            resp = requests.get(HOME_URL)
            soup_obj = self.get_soup_object(resp)
            csv_url = soup_obj.find("li", {"id": "ContentPlaceHolder1_liZip"}).find(
                "a"
            )["href"]
            csv_file = self.get_csv(csv_url)
            if csv_file:
                data = self.parse_csv(csv_file)
            
            # remove old data from redis
            self.remove_redis_data()
            # store data to redis
            self.store_data(data)
            # remove csv file here
            os.system("rm -rf " + self.bse_downloads + "/" + csv_file)
        except Exception as e:
            logger.error("Exception while start scraping")
            logger.error(e)
        return data

    def get_csv(self, url):
        csv_file = None
        try:
            resp = requests.get(url)
            zp = self.bse_downloads + self.zip_file

            # write response content to zip file
            with open(zp, "wb") as f:
                f.write(resp.content)

            # unzip daily_equity zip file to bse downloads directory
            with zipfile.ZipFile(zp, "r") as zip_ref:
                zip_ref.extractall(self.bse_downloads)

            # remove zip file after extraction
            os.system("rm -rf " + zp)

            # get latest csv file from the download directory
            csv_file = self.get_latest_csv_file()
        except Exception as e:
            logger.error("get_csv exception")
            logger.error(e)
        return csv_file

    def get_latest_csv_file(self):
        # iterate over bse downloads files to get the current equity csv file
        latest_file, latest_dt = None, None
        for f in os.listdir(self.bse_downloads):
            cur_dt = datetime.strptime(f.split(".")[0][2:], "%d%m%y")
            if not latest_file:
                latest_dt = cur_dt
                latest_file = f
            if latest_dt < cur_dt:
                latest_dt = cur_dt
                latest_file = f
        return latest_file
    
    def parse_csv(self, csv_file):
        headers = None
        data = []
        dt = datetime.strftime(
            datetime.strptime(
                csv_file.split(".")[0][2:], 
                "%d%m%y"
            ), 
            "%d-%m-%Y"
        )
        with open(self.bse_downloads + "/" + csv_file, "r") as f:
            csv_reader = csv.reader(f, delimiter=',')
            for idx, row in enumerate(csv_reader):
                try:
                    if idx == 0:
                        headers = row
                    else:
                        record = self.prepare_equity_record(headers, row)
                        record["date"] = dt
                        data.append(record)
                except Exception as e:
                    logger.error("Exception while preparing equity record")
                    logger.error(e)
        return data

    def prepare_equity_record(self, headers, row):
        record = dict()
        # format_key = lambda key: key.lower().strip().replace(" ", "_")
        req_keys = dict(
            SC_NAME="name", SC_CODE="code", LOW="low", HIGH="high", OPEN="open", CLOSE="close"
        )
        for key, val in zip(headers, row):
            if key in req_keys:
                record[req_keys[key]] = val.strip()
        return record

    def remove_redis_data(self):
        EquityBhavCopyDBManager().remove_redis_data()
    
    def store_data(self, data):
        ebc_mngr = EquityBhavCopyDBManager()
        for rec in data:
            try:
                ebc_mngr.insert_record(rec)
            except Exception as e:
                logger.error("Error While inserting record to redis")
                logger.error(e)

        # once data is stored upd last ts
        ebc_mngr.set_last_update_ts()

if __name__ == "__main__":
    data = EquityBhavCopyScrapingManager().start_scraping()
