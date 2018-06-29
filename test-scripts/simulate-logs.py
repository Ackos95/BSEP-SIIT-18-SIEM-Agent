#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re
from time import sleep
from os.path import join, dirname
from logging import getLogger, Formatter, FileHandler, DEBUG


HELP = 'help'
MESSAGE = 'message'
NAME = 'name'
LEVEL = 'level'
REPEAT = 'repeat'
REPEAT_INTERVAL = 'repeat-interval'

DEBUG_LEVEL = 'DEBUG'
INFO_LEVEL = 'INFO'
ERROR_LEVEL = 'ERROR'
FATAL_LEVEL = 'FATAL'
CRITICAL_LEVEL = 'CRITICAL'

OPTIONS = [HELP, MESSAGE, NAME, LEVEL, REPEAT_INTERVAL, REPEAT]
attr_regex = None


def get_attr_regex():
    """
    Creates option matching regex, with caching it in global variable (attr_regex)

    :return: {string} regex pattern to match all possible options
    """

    global attr_regex

    if attr_regex is None:
        attr_regex = r'--(?P<command>' +\
                     '|'.join(list(map(lambda option: '(?:{})'.format(option), OPTIONS))) +\
                     r')(?:=(?P<value>.*))?'

    return attr_regex


def print_usage():
    """ Simple function printing out help information how to use script """

    print(
        '\nUsage:\n' +
        '\tpython ./test-scripts/simulate-logs.py [options]\n\n' +
        'Possible options:\n' +
        '\t--{}:\t\t\tPrint\'s out usage info\n'.format(HELP) +
        '\t--{0}:\t\t\tSet\'s logger name (example: --{0}=MY_LOGGER), defaults to: "TEST_LOGGER"\n'.format(NAME) +
        '\t--{0}:\t\tSet\'s message to be logged (example: --{0}="Some random message"), '.format(MESSAGE) +
        'defaults to: "This is test message"\n'
        '\t--{}:\t\tSet\'s logger message level, with possible values - '.format(LEVEL) +
        '"DEBUG", "INFO", "ERROR", "FATAL" and "CRITICAL", defaults to: "DEBUG"\n',
        '\t--{0}:\t\tSet\'s how many times message should be logged (example: --{0}=3), '.format(REPEAT) +
        'defaults to: 1\n' +
        '\t--{}:\tSet\'s pause time (in seconds) between message repeats, '.format(REPEAT_INTERVAL) +
        'defaults to: 0\n\n'
    )


def simulate_log(logger, message, level):
    """
    Helper function simulating few logs for given message

    :param logger: {logging.Logger} instance
    :param message: {string} message to be logged
    :param level: {string} level of a log message
    """

    if level == 'DEBUG':
        logger.debug(message)
    elif level == 'ERROR':
        logger.error(message)
    elif level == 'CRITICAL':
        logger.critical(message)
    elif level == 'FATAL':
        logger.fatal(message)
    elif level == 'INFO':
        logger.info(message)


def create_config():
    """
    Helper method to safely pull command line arguments

    :return: logger_name (string)
    """

    ret_obj = {
        'message': 'This is test message',
        'name': 'TEST_LOGGER',
        'level': 'DEBUG',
        'repeat': 1,
        'repeat-interval': None
    }

    for arg in sys.argv[1:]:
        search_result = re.search(get_attr_regex(), arg)

        if search_result is not None:
            if search_result.group('command') == 'help':
                print_usage()
                exit(0)

            ret_obj[search_result.group('command')] = search_result.group('value')
        else:
            print_usage()
            exit(0)

    return ret_obj


def create_handler():
    """
    Helper method for creating syslog formatter

    :return: {logging.handlers.SysLogHandler}
    """

    handler = FileHandler(join(dirname(__file__), '../test-logs/simulated.log'))
    handler.setFormatter(Formatter('%(asctime)s - %(name)s - [%(levelname)s] - %(message)s', '%Y-%m-%d %H:%M:%S'))

    return handler


def setup_logger(logger_name):
    """
    Helper function for creating and setting up logger

    :param logger_name: (string) logger name
    :return: {logger.Logger}
    """

    logger = getLogger(logger_name)
    logger.setLevel(DEBUG)  # always set DEBUG level so that logger is writing any level
    logger.addHandler(create_handler())

    return logger


if __name__ == '__main__':
    config = create_config()
    app_logger = setup_logger(config['name'])

    for i in range(int(config['repeat'])):
        simulate_log(app_logger, config['message'], config['level'])
        if config['repeat-interval'] is not None and int(config['repeat']) > 1:
            sleep(int(config['repeat-interval']))
