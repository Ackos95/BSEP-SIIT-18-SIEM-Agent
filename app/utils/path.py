#!/usr/env/bin python
# -*- coding: utf-8 -*-

from os.path import dirname, join


def get_in_config_folder(search_path):
    return join(join(dirname(__file__), '../../config'), search_path)
