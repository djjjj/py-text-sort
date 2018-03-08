#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    hack by djj -_,- | good luck!
    date: 2018-03-02
"""
from ._fileSort import FileSort
from .handler import TextFileHandler
from .handler import JsonFileHandler
from ._utils import get_CPU_core_num


def sort_json_file(
        input_file,
        output_file,
        row_delimiter='\n',
        block_size=None,
        p_num=None):
    """

    :param input_file:
    :param output_file:
    :param row_delimiter: 行分割符
    :param block_size: 分块大小
    :param p_num: 进程数量
    :return:
    """
    if block_size is None:
        block_size = 1024*1024*32  # 32MB
    if p_num is None:
        p_num = get_CPU_core_num() + 1

    FileSort(
        input_file, output_file, JsonFileHandler, block_size, row_delimiter, p_num)


__all__ = [JsonFileHandler, TextFileHandler, sort_json_file]
