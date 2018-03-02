#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    hack by djj -_,- | good luck!
    date: 2018-03-02
"""
import json

from hashlib import md5

from ._textFileHandler import TextFileHandler


class JsonFileReader(TextFileHandler):

    def __init__(self, in_file_path, out_file_path, sort_keys):
        """

        :param in_file_path:
        :param out_file_path:
        :param sort_keys:
        """
        assert len(sort_keys) > 0
        super(JsonFileReader, self).__init__(in_file_path, out_file_path)
        self._keys = sort_keys

    def __iter__(self):
        """

        :return: row_key and row_data
        """
        for _ in self._input:
            try:
                json_data = json.loads(_)
                key = md5(reduce(
                    lambda _str, field: _str+json_data.get(field, ''),
                    self._keys, ''
                )).hexdigest()
                yield key, json_data
            except ValueError:
                print('expect a string of dict type: %s' % _)
                continue
            except AttributeError:
                print('expect a string of dict type: %s' % _)
                continue

    def save(self, value):
        self._ret.write(json.dumps(value)+'\n')
