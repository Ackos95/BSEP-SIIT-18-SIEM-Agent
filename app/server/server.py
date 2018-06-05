#!/usr/env/bin python
# -*- coding: utf-8 -*-

import http.server
from app.server.request_handler import get_configured_FirewallRequestHandler
from app.networking.ssl import get_agent_ssl_context


def start_firewall_server(config):
    httpd = http.server.HTTPServer(('', config['static']['firewall']['port']), get_configured_FirewallRequestHandler(config))
    httpd.socket = get_agent_ssl_context(config['static']['cert']).wrap_socket(httpd.socket)

    httpd.serve_forever()
