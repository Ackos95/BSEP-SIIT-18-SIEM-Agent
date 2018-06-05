#!/usr/bin/env python
# -*- coding: utf-8 -*-

import http.client
import json

from app.networking.ssl import get_agent_ssl_context


def parse_server_url(auth_server_url):
    parsed_url = auth_server_url.split(':')

    return (auth_server_url, 443) if len(parsed_url) == 1 else (parsed_url[0], int(parsed_url[1]))


def get_config(auth_server_url, cert_config):
    """
    Fetches configuration for current agent from authorization server

    :return {{}}: Configuration object fetched from authorization server
    """

    host_name, port = parse_server_url(auth_server_url)
    conn = http.client.HTTPSConnection(host=host_name, port=port, context=get_agent_ssl_context(cert_config))

    conn.request('GET', '/agents/agent-config')
    res = conn.getresponse()

    if res.status == 200:
        return json.loads(res.read().decode('utf-8'), encoding='utf-8')
    else:
        return {}
