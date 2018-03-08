#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    hack by djj -_,- | good luck!
    date: 2018-03-02
"""
from ._base import BaseHandler


class TextFileHandler(BaseHandler):

    def row_key(self, val):
        return val
