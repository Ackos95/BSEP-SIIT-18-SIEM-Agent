#!/usr/bin/env python
# -*- coding: utf-8 -*-

from json import load
from os.path import join, dirname


def load_config():
    """
    Simple as it can be, loads json config file, and returns an python object representation

    :return: {Dictionary} python object representation of the json configuration
    """

    try:
        with open(join(dirname(__file__), '../../config/agent-config.json')) as config_file:
            config = load(config_file)

        return config
    except IOError:
        print('No configuration file provided')
        exit(1)
