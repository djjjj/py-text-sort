#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    hack by djj -_,- | good luck!
    date: 2018-03-02
"""
from ._base import BaseHandler


class TextFileHandler(BaseHandler):

    def __init__(self, in_file_path, out_file_path):
        """

        :param in_file_path:
        :param out_file_path:
        """
        fp = open(in_file_path, 'r')
        super(TextFileHandler, self).__init__(fp)
        self._ret = open(out_file_path, 'w')

    def save(self, value):
        self._ret.write(value)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._ret.close()
