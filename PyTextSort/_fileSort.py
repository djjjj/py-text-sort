#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    hack by djj -_,- | good luck!
    date: 2018-03-03
"""
import os

import shutil

from ._fileSplit import FileSplit, SubFile


class FileSort(object):

    FILE_PREFIX = '.~file_sort'

    def __init__(
            self,
            in_file_path,
            out_file_path,
            file_handler,
            block_size,
            delimiter):
        self._in = in_file_path
        self._in_dir, self._in_name = os.path.split(in_file_path)
        self._out = out_file_path
        self._handler = file_handler
        self._block_size = block_size
        self._delimiter = delimiter
        self._tmp_files = []

    def run(self):
        self._split()
        while len(self._tmp_files) > 1:
            left_file = self._tmp_files.pop(0)
            right_file = self._tmp_files.pop(0)
            self._merge_sort(
                left_file,
                right_file,
                self._gen_tmp_file(
                    left_file[left_file.rfind('s_')+2:],
                    right_file[right_file.rfind('s_')+2:]
                ))
        shutil.move(self._tmp_files.pop(0), self._out)

    def _gen_tmp_file(self, *ids):
        return os.path.join(
            self._in_dir,
            '%s_%s_%s' % (self.FILE_PREFIX, self._in_name, '-'.join(ids))
        )

    def _split(self):
        fs = FileSplit(self._in, self._block_size, self._delimiter)
        for fp_start, fp_end in fs:
            f_name = self._gen_tmp_file(str(fp_start), str(fp_end))
            self._save_block(fp_start, fp_end, f_name)

    def _save_block(self, start, end, out_file):
        sub_file = SubFile(self._in, start, end)
        with open(out_file, 'w') as out:
            sorted_lines = sorted(
                sub_file,
                key=lambda x: self._handler.row_key(x)
            )
            out.write(''.join(sorted_lines))
        self._tmp_files.append(out_file)

    def _merge_sort(self, left_file, right_file, out_file):
        with open(out_file, 'w') as out, \
                open(left_file) as left, \
                open(right_file) as right:
            l_line = left.readline()
            r_line = right.readline()
            l_key = self._handler.row_key(l_line)
            r_key = self._handler.row_key(r_line)
            while l_line and r_line:
                if l_key < r_key:
                    out.write(l_line)
                    for l_line in left:
                        l_key = self._handler.row_key(l_line)
                        if l_key >= r_key:
                            break
                        out.write(l_line)
                    else:
                        break
                else:
                    out.write(r_line)
                    for r_line in right:
                        r_key = self._handler.row_key(r_line)
                        if l_key < r_key:
                            break
                        out.write(r_line)
                    else:
                        break

            if l_line:
                out.write(l_line)
                for line in left:
                    out.write(line)
            else:
                out.write(r_line)
                for line in right:
                    out.write(line)
        os.remove(left_file)
        os.remove(right_file)
        self._tmp_files.append(out_file)
