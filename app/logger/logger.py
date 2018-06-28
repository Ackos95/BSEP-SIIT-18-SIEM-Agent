#!/usr/env/bin python
# -*- coding: utf-8 -*-

from logging import getLogger, Formatter, FileHandler, ERROR
from app.utils.path import get_in_root_folder


# Global app logger
app_logger = None

LOG_TYPES = [
    {
        "name": "self-logs",
        "contextRegex": "(?: - )(?P<value>.*?)(?: - )",
        "messageRegex": "(?:.*)(?: - )(?P<value>.*)$",
        "severityRegex": "(?P<value>TRACE|DEBUG|INFO|WARN|ERROR|FATAL)",
        "timestampRegex": "^(?P<value>.*?)(?: -)",
        "dateTimeFormat": "%Y-%m-%d %H:%M:%S"
      }
]


def _create_handler():
    """
    Helper method for creating syslog formatter

    :return: {logging.handlers.SysLogHandler}
    """

    handler = FileHandler(get_in_root_folder('logs/app.log'))
    handler.setFormatter(Formatter('%(asctime)s - %(name)s - [%(levelname)s] - %(message)s', '%Y-%m-%d %H:%M:%S'))

    return handler


def _setup_logger(logger_name):
    """
    Helper function for creating and setting up logger

    :param logger_name: (string) logger name
    :return: {logger.Logger}
    """

    logger = getLogger(logger_name)
    logger.setLevel(ERROR)  # always set DEBUG level so that logger is writing any level
    logger.addHandler(_create_handler())

    return logger


def get_logger():
    global app_logger

    # TODO: check threading compatibility with global objects
    # TODO: add logger config (static)
    if app_logger is None:
        app_logger = _setup_logger('')

    return app_logger
