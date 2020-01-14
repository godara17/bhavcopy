from utils import LoggerUtility
from datetime import datetime
import json
import redis
import os

BASE_PATH = os.getenv("BASE_PATH")
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")

log_data = dict(
    logging_conf=BASE_PATH + "/utils/conf/logging.conf",
    log_file=BASE_PATH + "/logs/app_logs.log",
)
logger = LoggerUtility(log_data).logger

"""
    Sample record key name 'equityBhvCp:code'=record
    Sample record key name for second index
    'equityBhvCpName:name' = 'equityBhvCp:code'
    Store record in redis, code would be id for the hash record
"""


class EquityBhavCopySchema:
    def __init__(self, info):
        self.name = info["name"] if "name" in info else ""
        self.code = info["code"] if "code" in info else ""
        self.open = info["open"] if "open" in info else ""
        self.close = info["close"] if "close" in info else ""
        self.low = info["low"] if "low" in info else ""
        self.high = info["high"] if "high" in info else ""
        self.date = info["date"] if "date" in info else ""


class EquityBhavCopyDBManager:
    def __init__(self):
        self.p_index_start = "equityBhvCp:"
        self.s_index_start = "equityBhvCpName:"
        self.ol_name = "equity_codes"
        self.last_upd_ts = "equity_bhv_cp_last_upd_ts"

    def get_redis_instance(self):
        return redis.Redis(
            host=REDIS_HOST, port=REDIS_PORT, password="redis@54321", db=0
        )

    def insert_record(self, info):
        try:
            ri = self.get_redis_instance()
            record = vars(EquityBhavCopySchema(info))
            # set primary key
            p_key = self.p_index_start + record["code"]
            ri.hmset(p_key, record)

            # set secondary index for searching on name field
            s_key = self.s_index_start + record["name"]
            ri.set(s_key, p_key)

            # insert record ids to list for fetching records faster
            ri.rpush(self.ol_name, record["code"])
        except Exception as e:
            logger.error("Error while inserting records")
            logger.error(e)

    def remove_redis_data(self):
        ri = self.get_redis_instance()
        try:
            keys = [key.decode() for key in ri.keys()]
            for key in keys:
                ri.delete(key)
        except Exception as e:
            logger.error("Error while removing redis records")
            logger.error(e)

    def delete_record(self, info):
        pass

    def search_by_name(self, name):
        records = []
        ri = self.get_redis_instance()
        try:
            search_key = self.s_index_start + name + "*"
            matched_keys = [key.decode() for key in ri.keys(search_key)]
            for key in matched_keys:
                try:
                    record_index = ri.get(key)
                    raw_record = ri.hgetall(record_index.decode())
                    record = self.format_record(raw_record)
                    records.append(record)
                except Exception as e:
                    logger.error(
                        "Error while fetching record from matched keys"
                    )
                    logger.error(e)
        except Exception as e:
            logger.error("Error while searching record in redis")
            logger.error(e)
        return records

    def get_top_records(self, n=10):
        records = []
        ri = self.get_redis_instance()
        try:
            codes = ri.lrange(self.ol_name, 0, n - 1)
            for code in codes:
                key = self.p_index_start + code.decode()
                record = ri.hgetall(key)
                records.append(self.format_record(record))
        except Exception as e:
            logger.error("Error while getting top records")
            logger.error(e)
        return records

    def format_record(self, raw_record):
        record = dict()
        for k, v in raw_record.items():
            record[k.decode()] = v.decode()
        return record

    def set_last_update_ts(self):
        try:
            ts = str(int(datetime.utcnow().timestamp()))
            ri = self.get_redis_instance()
            ri.set(self.last_upd_ts, ts)
        except Exception as e:
            logger.error("on_insertion_completion exception")
            logger.error(e)

    def get_last_update_ts(self):
        ts = None
        try:
            ri = self.get_redis_instance()
            ts = int(ri.get(self.last_upd_ts).decode())
        except Exception as e:
            logger.error("on_insertion_completion exception")
            logger.error(e)
        return ts


# def decode_redis(src):
#     if isinstance(src, list):
#         rv = list()
#         for key in src:
#             rv.append(decode_redis(key))
#         return rv
#     elif isinstance(src, dict):
#         rv = dict()
#         for key in src:
#             rv[key.decode()] = decode_redis(src[key])
#         return rv
#     elif isinstance(src, bytes):
#         return src.decode()
#     else:
#         raise Exception("type not handled: " +type(src))

# def search_by_name(self, name):
#     record = None
#     ri = self.get_redis_instance()
#     try:
#         s_key = self.s_index_start + name
#         record_index = ri.get(s_key)
#         if not record_index:
#             return
#         raw_record = ri.hgetall(record_index.decode())
#         if not raw_record:
#             return
#         record = self.format_record(raw_record)
#     except Exception as e:
#         logger.error("Error while searching record in redis")
#         logger.error(e)
#     return record
