import os
import logging
import logging.config


class LoggerUtility:
    def __init__(self, log_data):
        self.logger_name = "Zerodha_Log"
        self.logger = None
        self.init_logger(log_data)

    def init_logger(self, log_data):
        logging.config.fileConfig(
            log_data["logging_conf"],
            disable_existing_loggers=False,
            defaults={"logfilename": log_data["log_file"]},
        )
        self.logger = logging.getLogger(self.logger_name)
