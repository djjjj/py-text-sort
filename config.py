#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    hack by djj -_,- | good luck!
    date: 2018-03-02
"""
import os

import yaml


class Config(object):

    def __init__(self):
        default = yaml.load(open(os.path.join(
            os.path.dirname(__file__), 'default_configs.yaml'
        ), 'r'))
        for key, value in default:
            setattr(self, key, value)


CONFIG = Config()
