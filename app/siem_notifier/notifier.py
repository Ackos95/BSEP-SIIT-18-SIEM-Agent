#!/usr/bin/env python
# -*- coding: utf-8 -*-

from requests import post


def notify_siem_core(core_url, data):
    """
    Notify function, sending POST request to `SIEM-Core` with new (prepared) data

    :param core_url: url address for `SIEM-Core` (HTTP(S))
    :param data: iterable containing all of the `SysLogParser.SysLogEntry` objects to be sent
    :param agent_id: API_KEY for agent when updating SIEM-Core
    """

    print('TODO: NOTIFY SIEM-CORE', core_url, data)
    # request = post(core_url, data=''.join(data), headers={'Authorization': agent_id})
    # print('[{}] POST {}: "{}"'.format(request.status_code, core_url, request.text))
