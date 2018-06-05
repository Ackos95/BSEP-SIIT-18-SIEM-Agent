#!/usr/bin/env python
# -*- coding: utf-8 -*-

import http.client
import json

from app.networking.ssl import get_agent_ssl_context


def parse_server_url(auth_server_url):
    parsed_url = auth_server_url.split(':')

    return (auth_server_url, 443) if len(parsed_url) == 1 else (parsed_url[0], int(parsed_url[1]))


def get_post_headers():
    return {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    }


def get_config(auth_server_url, cert_config):
    """
    Fetches configuration for current agent from authorization server
    """

    host_name, port = parse_server_url(auth_server_url)
    conn = http.client.HTTPSConnection(host=host_name, port=port, context=get_agent_ssl_context(cert_config))

    conn.request('GET', '/agents/agent-config')
    return conn.getresponse()


def post_logs(destination_ip, cert_config, log_entries):
    """
    Posts new logs to destination ip (siem core or firewall agent)
    """

    host_name, port = parse_server_url(destination_ip)
    conn = http.client.HTTPSConnection(host=host_name, port=port, context=get_agent_ssl_context(cert_config))

    conn.request('POST', '/agents/logs', json.dumps(log_entries), get_post_headers())
    return conn.getresponse()


def post_check_agent(destination_ip, cert_config, agent_cert_data):
    """
    Posts request to check if agent can send data to me
    """

    host_name, port = parse_server_url(destination_ip)
    conn = http.client.HTTPSConnection(host=host_name, port=port, context=get_agent_ssl_context(cert_config))

    conn.request('POST', '/agents/check-agent', json.dumps(agent_cert_data), get_post_headers())
    return conn.getresponse()
