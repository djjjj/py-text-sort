#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    hack by djj -_,- | good luck!
    date: 2018-03-02
"""
from os.path import getsize


class SubFile(object):
    def __init__(self, file_path, start, end):
        fp = open(file_path, 'rb')
        fp.seek(start)
        self.fp = fp
        self.end = end - start

    def __iter__(self):
        line = self.fp.readline()
        self.end -= len(line)
        while self.end >= 0 and line:
            yield line
            line = self.fp.readline()
            self.end -= len(line)


class FileSplit(object):

    def __init__(self, in_file_path, block_size, delimiter='\n'):
        self._fp = open(in_file_path, 'rb')
        self._size = getsize(in_file_path)
        self._split_num = self._size / block_size + 1
        self._delimiter = delimiter

    def __iter__(self):
        step = self._size / self._split_num
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
            yield SubFile(self._fp.name, start, end)
