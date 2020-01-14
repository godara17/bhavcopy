import sys
import os, os.path

BASE_PATH = os.getenv("BASE_PATH")
sys.path.append(BASE_PATH)

from common.equity_bhav_cp_db_mgmt import EquityBhavCopyDBManager
from utils import LoggerUtility
from datetime import datetime
import cherrypy

log_data = dict(
    logging_conf=BASE_PATH + "/utils/conf/logging.conf",
    log_file=BASE_PATH + "/logs/app_logs.log",
)
logger = LoggerUtility(log_data).logger


class BhavCopyEquity(object):
    @cherrypy.expose
    def index(self):
        return open(BASE_PATH + "/public/html/index.html")


@cherrypy.expose
class ListService(object):
    @cherrypy.tools.accept(media="text/plain")
    @cherrypy.tools.json_out()
    def GET(self):
        try:
            ebc_mngr = EquityBhavCopyDBManager()
            records = ebc_mngr.get_top_records()
            last_upd_ts = ebc_mngr.get_last_update_ts() + int(5.5*60*60)
            
            format_date = lambda ts: datetime.strftime(
                datetime.fromtimestamp(ts), "%H:%M %d %b %y"
            ) if ts else "NA"
            return dict(
                status="SUCCESS",
                records=records,
                last_upd_ts=format_date(last_upd_ts),
            )
        except Exception as e:
            logger.error("Exception while getting records")
            logger.error(e)
            return dict(status="ERROR", msg=e.msg)


@cherrypy.expose
class SearchService(object):
    @cherrypy.tools.accept(media="text/plain")
    @cherrypy.tools.json_out()
    def GET(self, name=None):
        try:
            ebc_mngr = EquityBhavCopyDBManager()
            records = ebc_mngr.search_by_name(name)
            return dict(status="SUCCESS", records=records)
        except Exception as e:
            logger.error("Exception while searching record")
            logger.error(e)
            return dict(status="ERROR", msg=e.msg)


if __name__ == "__main__":
    cherrypy.server.unsubscribe()

    server1 = cherrypy._cpserver.Server()
    server1.socket_port = 2729
    server1._socket_host = "0.0.0.0"
    server1.thread_pool = 2
    server1.subscribe()

    conf = {
        "/": {
            "tools.sessions.on": True,
            "tools.staticdir.root": os.path.abspath(os.getcwd()),
        },
        "/static": {
            "tools.staticdir.on": True,
            "tools.staticdir.dir": "./public",
        },
        "/list": {
            "request.dispatch": cherrypy.dispatch.MethodDispatcher(),
            "tools.response_headers.on": True,
            "tools.response_headers.headers": [("Content-Type", "text/plain")],
        },
        "/search": {
            "request.dispatch": cherrypy.dispatch.MethodDispatcher(),
            "tools.response_headers.on": True,
            "tools.response_headers.headers": [("Content-Type", "text/plain")],
        },
    }
    equity = BhavCopyEquity()
    equity.list = ListService()
    equity.search = SearchService()
    cherrypy.quickstart(equity, "/", conf)
