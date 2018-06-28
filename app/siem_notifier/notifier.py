#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app.networking.api import post_logs


def notify_siem_core(core_url, data, cert_config):
    """
    Notify function, sending POST request to `SIEM-Core` with new (prepared) data

    :param core_url: url address for `SIEM-Core` (HTTP(S))
    :param data: iterable containing all of the `SysLogParser.SysLogEntry` objects to be sent
    :param cert_config: Configuration object containing information about client certificates
    """

    if len(data) == 0:
        return

    res = post_logs(core_url, cert_config, data)

    print('[{}] POST {}: "{}"'.format(res.status, core_url, res.read()))
