#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    hack by djj -_,- | good luck!
    date: 2018-03-02
"""
import json

from functools import reduce

from ._textFileHandler import TextFileHandler


class JsonFileHandler(TextFileHandler):

    def __init__(self, sort_keys):
        self._keys = sort_keys

    def row_key(self, val):
        key = None
        try:
            json_data = json.loads(val)
            key = reduce(lambda _str, field: (
                    '%s%s' % (_str, json_data.get(field, ''))
            ).encode('utf8'), self._keys, '')
        except ValueError:
            print('expect a string of dict type: %s' % val)
            raise ValueError()
        except AttributeError:
            print('expect a string of dict type: %s' % val)
        return key
