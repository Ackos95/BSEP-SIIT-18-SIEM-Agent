#!/usr/bin/env python
# -*- coding: utf-8 -*-

from re import match
from SysLogParser.parser import SysLogParser


class ParseException(Exception):
    pass


def custom_parse_lines(file_lines, dir_config):
    log_entities = []

    for line in file_lines:
        entity = {}
        match_obj = match(dir_config['pattern-options']['matcher'], line)
        if match_obj is None:
            raise ParseException('Invalid log format')

        try:
            for index, variable in enumerate(dir_config['pattern-options']['variables']):
                entity[variable] = match_obj.group(index)
        except IndexError:
            raise ParseException('Invalid log format')

        log_entities.append(entity)

    return log_entities


def parse_log_lines(file_lines, dir_config):
    if dir_config['log-pattern'] == 'rfc5424':
        return SysLogParser.parse_rfc5424(file_lines)
    elif dir_config['log-pattern'] == 'rfc3164':
        return SysLogParser.parse_rfc3164(file_lines)
    elif dir_config['log-pattern'] == 'custom' and dir_config.get('pattern-options', None) is not None:
        return custom_parse_lines(file_lines, dir_config)
    else:
        raise Exception('Bad configuration provided')


def format_log_entries(entries):
    pass
