#!/usr/bin/env python
# -*- coding: utf-8 -*-


import time
from app.networking.ssl import check_certs
from app.config.config_loader import load_config
from app.log_watchers.initialize import LogWatchers
from app.server.server import start_firewall_server


def bootstrap():
    """
    Starting point of the application, loads config and initialize and starts file watchers,
    after that enters infinite loop on main thread.
    """

    config = load_config()
    watchers = LogWatchers(config)

    try:
        watchers.start()
        print('SIEM-Agent started')
        start_firewall_server(config)
    except KeyboardInterrupt:
        watchers.stop()
