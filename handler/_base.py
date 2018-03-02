#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    hack by djj -_,- | good luck!
    date: 2018-03-02
"""


class BaseHandler(object):

    def __init__(self, iterable_in):
        self._input = iterable_in
        self._ret = list()

    def __iter__(self):
        for _ in self._input:
            yield _, _

    def save(self, value):
        self._ret.append(value)

    @property
    def result(self):
        return self._ret
