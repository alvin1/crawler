import logging
import logging.handlers
from .settings import Settings


class Logger(object):
    def __init__(self, log_path='var/log/crawler_log.txt'):
        logging.basicConfig(level=Settings.LOGGING_LEVEL, format=Settings.LOGGING_MSG_FORMAT,
                datefmt=Settings.LOGGING_DATE_FORMAT,
                filename=log_path,
                filemode='a')

        self.logger = logging.getLogger('')

        # logging to screen, too
        console = logging.StreamHandler()
        console.setLevel(Settings.LOGGING_LEVEL)
        formatter = logging.Formatter(Settings.LOGGING_MSG_FORMAT, Settings.LOGGING_DATE_FORMAT)
        console.setFormatter(formatter)
        self.logger.addHandler(console)


    def error(self, msg):
        self.logger.error(msg)

    def info(self, msg):
        self.logger.info(msg)

    def debug(self, msg):
        self.logger.debug(msg)

    def warning(self, msg):
        self.logger.warning(msg)
