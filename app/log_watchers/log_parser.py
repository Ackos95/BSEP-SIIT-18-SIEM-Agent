#!/usr/env/bin python
# -*- coding: utf-8 -*-

import re
import socket
import datetime
import platform


def _extract_value(line, log_config, regex_key):
    if regex_key not in log_config:
        return None

    match = re.search(re.compile(log_config[regex_key]), line)

    return match.groupdict()['value'] \
        if match is not None and 'value' in match.groupdict() is not None else None


def _get_timestamp(time_str, date_time_format):
    try:
        return int(datetime.datetime.strptime(time_str, date_time_format).timestamp())
    except ValueError:
        return 0


def _parse_log_line(line, log_config, dir_path, file_path):
    """
    {
       context: "SYSLOG koji korisnik je ulogovan (STRING)",
       severity: "STRING",
       timestamp: "long",
       message: "STRING",
       rawMessage: "Raw message (as read)",
       hostName: "Host name (STRING)" // system variable,
       filePath: "Puna putanja do fajla",
       directoryPath: "Putanja direktorijuma koji se posmatra",
       isPersonalLog: "Boolean",
       cn: "Common name sertifikata", // agent ne setuje svoj common name (to je reseno na firewall)
    }
    """

    return {
        'context': _extract_value(line, log_config, 'contextRegex'),
        'severity': _extract_value(line, log_config, 'severityRegex'),
        'timestamp': _get_timestamp(_extract_value(line, log_config, 'timestampRegex'), log_config['dateTimeFormat']),
        'message': _extract_value(line, log_config, 'messageRegex'),
        'rawMessage': line,
        'hostName': socket.gethostname(),
        'filePath': file_path,
        'directory': dir_path,
        'operatingSystem': platform.system().upper(),
        'operatingSystemVersion': platform.platform(),
        'personalLog': True
    }


def parse_log_lines(log_lines, log_configs, dir_path, file_path):
    return list(map(lambda line: _parse_log_line(line, log_configs[0], dir_path, file_path), log_lines))\
        if log_configs is not None and len(log_configs) > 0 else []
