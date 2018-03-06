#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    hack by djj -_,- | good luck!
    date: 2018-03-03
"""
import os

from _fileSort import FileSort
from handler import JsonFileHandler


CASE_DIR = os.path.join(os.path.dirname(__file__), 'case_file_sort')


class Case1(object):
    CASE_FILES = [os.path.join(CASE_DIR, _) for _ in ['10_lines', '1000000_lines']]
    CASE_BLOCK_SIZE = [1024*1024*10]
    CASE_PROCESS_NUM = [5]

    @classmethod
    def run(cls):
        handler = JsonFileHandler(['_id'])
        for f in cls.CASE_FILES:
            for block_size in cls.CASE_BLOCK_SIZE:
                for p_num in cls.CASE_PROCESS_NUM:
                    fs = FileSort(f, '%s-sorted' % f, handler, block_size, '\n', p_num)
                    fs.run()


if __name__ == '__main__':
    Case1.run()
