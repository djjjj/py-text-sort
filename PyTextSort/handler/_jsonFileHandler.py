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
        json_data = self.row_encode(val)
        key = self.row_key_plus(json_data)
        return key

    def row_key_plus(self, dic):
        key = None
        try:
            key = reduce(lambda _str, field: (
                '%s%s' % (_str, dic.get(field, ''))
            ).encode('utf8'), self._keys, '')
        except AttributeError:
            print('expect a string of dict type: %s' % dic)
        return key

    @staticmethod
    def row_encode(val):
        line = {}
        try:
            line = json.loads(val)
        except ValueError:
            print('expect a string of dict type: %s' % val)
        return line

    @staticmethod
    def row_decode(val):
        return json.dumps(val, ensure_ascii=False)
