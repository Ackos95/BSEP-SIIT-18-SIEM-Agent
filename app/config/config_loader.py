#!/usr/bin/env python
# -*- coding: utf-8 -*-

from json import load

from app.utils.path import get_in_config_folder
from app.networking.api import get_config


def load_static_config():
    """
    Simple as it can be, loads json config file, and returns an python object representation

    :return: {Dictionary} python object representation of the json configuration
    """

    try:
        with open(get_in_config_folder('agent-config.json')) as config_file:
            config = load(config_file)

        return config
    except IOError:
        print('No configuration file provided')
        exit(1)


def load_agent_config(auth_server_url, cert_config):
    """
    Fetch configuration for given agent from authorization server, and turn it into Dictionary

    :return: {Dictionary} python object representation of the dynamic agent configuration
    """

    return get_config(auth_server_url, cert_config)


def load_config():
    static_conf = load_static_config()

    return {
        'agent': load_agent_config(static_conf['authorizationServerIpAndPort'], static_conf['cert']),
        'static': static_conf
    }
