#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    hack by djj -_,- | good luck!
    date: 2018-03-02
"""
import os

from _fileSplit import FileSplit, SubFile


CASE_DIR = os.path.join(os.path.dirname(__file__), 'case_file_split')


class Case1(object):
    CASE_FILES = [os.path.join(CASE_DIR, _) for _ in ['100w_lines', 'empty']]
    CASE_BLOCK_SIZE = [1024*1024*10]
    CASE_RESULT = [
        168336,
        166119,
        166513,
        166250,
        166495,
        166287,
        0
    ]

    @classmethod
    def run(cls):
        j = 0
        for f in cls.CASE_FILES:
            for block_size in cls.CASE_BLOCK_SIZE:
                fs = FileSplit(f, block_size, '\n')
                for start, end in fs:
                    out = open('%s-%s-%s-%s' % (f, block_size, start, end), 'w')
                    count = 0
                    for line in SubFile(f, start, end):
                        out.write(str(line, encoding='utf8'))
                        count += 1
                    assert count == cls.CASE_RESULT[j]
                    j += 1
                    out.close()


if __name__ == '__main__':
    Case1.run()
