#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    hack by djj -_,- | good luck!
    date: 2018-03-02
"""
from ._fileSort import FileSort, FileMerge
from .handler import TextFileHandler
from .handler import JsonFileHandler


__all__ = ('JsonFileHandler', 'TextFileHandler', 'sort_json_file', 'sort_file')


def sort_file(
        input_file,
        output_file,
        file_handler=None,
        row_delimiter='\n',
        block_size=None,
        p_num=None,
        merge=False):
    """

    :param input_file:
    :param output_file:
    :param file_handler:
    :param row_delimiter: 行分割符
    :param block_size: 分块大小
    :param p_num: 进程数量
    :param merge: 是否用keys合并
    :return:
    """
    from ._utils import get_CPU_core_num

    if block_size is None:
        block_size = 1024*1024*32  # 32MB
    if p_num is None:
        p_num = get_CPU_core_num() + 1
    if file_handler is None:
        file_handler = TextFileHandler()

    if merge:
        fs = FileMerge(
            input_file, output_file, file_handler, block_size, row_delimiter, p_num)
    else:
        fs = FileSort(
            input_file, output_file, file_handler, block_size, row_delimiter, p_num)
    fs.run()


def sort_json_file(
        input_file,
        output_file,
        sort_keys,
        row_delimiter='\n',
        block_size=None,
        p_num=None):

    j_handler = JsonFileHandler(sort_keys)
    sort_file(input_file, output_file, j_handler, row_delimiter, block_size, p_num)


def merge_json_file(
        input_file,
        output_file,
        merge_keys,
        row_delimiter='\n',
        block_size=None,
        p_num=None):

    j_handler = JsonFileHandler(merge_keys)
    sort_file(input_file, output_file, j_handler, row_delimiter, block_size, p_num, True)
