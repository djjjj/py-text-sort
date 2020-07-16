#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    hack by djj -_,- | good luck!
    date: 2018-03-08
"""


def get_CPU_core_num():
    from multiprocessing import cpu_count

    return cpu_count()


def get_file_size(file_path):
    from os.path import getsize

    return getsize(file_path)
