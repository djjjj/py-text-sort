#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    hack by djj -_,- | good luck!
    date: 2018-03-02
"""
import sys

from ._utils import get_file_size


if sys.version_info < (3, 0):
    str = lambda x, y: x.encode(y, 'ignore')
    handle_delimiter = lambda x: x
else:
    handle_delimiter = lambda x: ord(x)


class SubFile(object):
    def __init__(self, file_path, start, end):
        fp = open(file_path, 'rb')
        fp.seek(start)
        self._fp = fp
        self._len = end - start

    def __iter__(self):
        line = self._fp.readline()
        self._len -= len(line)
        while self._len >= 0 and line:
            yield str(line, 'utf8')
            line = self._fp.readline()
            self._len -= len(line)
        self._fp.close()


class FileSplit(object):

    def __init__(self, in_file_path, block_size, delimiter):
        self._ret = []
        self._fp = open(in_file_path, 'rb')
        self._delimiter = handle_delimiter(delimiter)
        self._size = get_file_size(in_file_path)
        self._split_num = self._size // block_size + 1
        assert self._split_num <= 1024

    def __iter__(self):
        step = self._size // self._split_num
        end = 0
        for i in range(self._split_num):
            start = end
            end = start + step
            self._fp.seek(end)
            # find the char '\n' or other delimiter
            buf = self._fp.read(2048)
            flag = False
            while buf:
                for c in buf:
                    end += 1
                    if c == self._delimiter:
                        flag = True
                        break
                if flag:
                    break
                buf = self._fp.read(2048)
            yield start, end
        self._fp.close()
