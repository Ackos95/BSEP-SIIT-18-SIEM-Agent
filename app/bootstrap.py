#!/usr/bin/env python
# -*- coding: utf-8 -*-


import time
from app.networking.ssl import check_certs
from app.config.config_loader import load_config
from app.log_watchers.initialize import LogWatchers


def bootstrap():
    """
    Starting point of the application, loads config and initialize and starts file watchers,
    after that enters infinite loop on main thread.
    """

    if not check_certs():
        print('Invalid certificates provided. Please add certificates into `config/certs` folder')
        return

    # print(load_config())
    watchers = LogWatchers(load_config())

    try:
        watchers.start()
        print('SIEM-Agent started')
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        watchers.stop()
