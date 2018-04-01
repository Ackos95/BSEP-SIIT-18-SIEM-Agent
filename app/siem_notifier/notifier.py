#!/usr/bin/env python
# -*- coding: utf-8 -*-

from requests import post
from SysLogParser.parser import SysLogParser


def notify_siem_core(core_url, data):
    """
    Notify function, sending POST request to `SIEM-Core` with new (prepared) data

    :param core_url: url address for `SIEM-Core` (HTTP(S))
    :param data: iterable containing all of the `SysLogParser.SysLogEntry` objects to be sent
    """

    # request = post(core_url, data=''.join(SysLogParser.format_rfc5424(data)))
    print('POST {}, data='.format(core_url), ''.join(SysLogParser.format_rfc5424(data)))
