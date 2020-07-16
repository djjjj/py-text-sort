#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    hack by djj -_,- | good luck!
    date: 2018-03-02
"""
from ._fileSort import FileSort
from .handler import TextFileHandler
from .handler import JsonFileHandler
from ._fileMerge import merge, merge_func1


__all__ = ('JsonFileHandler', 'TextFileHandler', 'sort_json_file', 'sort_file')


def sort_file(
        input_file,
        output_file,
        file_handler=None,
        row_delimiter='\n',
        block_size=None
    ):
    """

    :param input_file:
    :param output_file:
    :param file_handler:
    :param row_delimiter: 行分割符
    :param block_size: 分块大小
    :return:
    """
    from ._utils import get_CPU_core_num

    if block_size is None:
        block_size = 1024*1024*32  # 32MB
    if file_handler is None:
        file_handler = TextFileHandler()

    FileSort(
        input_file, output_file, file_handler, block_size, row_delimiter).run()


def sort_json_file(
        input_file,
        output_file,
        sort_keys,
        row_delimiter='\n',
        block_size=None,
    ):

    j_handler = JsonFileHandler(sort_keys)
    sort_file(input_file, output_file, j_handler, row_delimiter, block_size)


def merge_json_file(
        input_file,
        output_file,
        merge_keys,
        row_delimiter='\n',
        block_size=None
    ):

    tmp_sort_file = '%s.sorted' % output_file
    j_handler = JsonFileHandler(merge_keys)
    sort_file(input_file, output_file, j_handler, row_delimiter, block_size)
    merge(tmp_sort_file, output_file, j_handler, merge_func1)
