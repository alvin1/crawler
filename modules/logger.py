import logging
import logging.handlers
from .settings import Settings


class Logger(object):
    def __init__(self, log_path='var/log/crawler_log.txt'):
        formatter = logging.Formatter(Settings.LOGGING_MSG_FORMAT, Settings.LOGGING_DATE_FORMAT)

        log_handler = logging.handlers.TimedRotatingFileHandler(log_path, 'midnight', 1)
        log_handler.setLevel(Settings.LOGGING_LEVEL)
        log_handler.setFormatter(formatter)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(Settings.LOGGING_LEVEL)
        console_handler.setFormatter(formatter)

        self.logger = logging.getLogger('crawler_log')
        self.logger.addHandler(log_handler)
        self.logger.addHandler(console_handler)

    def error(self, msg):
        self.logger.error(msg)

    def info(self, msg):
        self.logger.info(msg)

    def debug(self, msg):
        self.logger.debug(msg)

    def warning(self, msg):
        self.logger.warning(msg)
