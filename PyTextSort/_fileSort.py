#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    hack by djj -_,- | good luck!
    date: 2018-03-03
"""
import time
import os

import shutil

from multiprocessing import Manager, Pool

from ._fileSplit import FileSplit, SubFile


import sys

if sys.version_info < (3, 0):
    import types
    import copy_reg
    reload(sys)
    sys.setdefaultencoding('utf8')

    def _pickle_method(m):
        if m.im_self is None:
            return getattr, (m.im_class, m.im_func.func_name)
        else:
            return getattr, (m.im_self, m.im_func.func_name)

    copy_reg.pickle(types.MethodType, _pickle_method)


class FileSort(object):

    FILE_PREFIX = '.~file_sort'

    def __init__(
            self,
            in_file_path,
            out_file_path,
            file_handler,
            block_size,
            delimiter,
            process_num):
        self._p_pool = Pool(processes=process_num)
        self._in = in_file_path
        self._in_dir, self._in_name = os.path.split(in_file_path)
        self._out = out_file_path
        self._handler = file_handler
        self._block_size = block_size
        self._delimiter = delimiter
        self._tmp_files = Manager().list()
        self._count = Manager().Value('i', -1)

    def run(self):
        self._split()
        while self._count.value != 0:
            if len(self._tmp_files) > 1:
                left_file = self._tmp_files.pop()
                right_file = self._tmp_files.pop()
                self._p_pool.apply_async(
                    self._merge_sort,
                    (left_file, right_file, self._gen_tmp_file(
                        left_file[left_file.rfind('_')+1:],
                        right_file[right_file.rfind('_')+1:]
                    ))
                )
            time.sleep(0.3)
        self._p_pool.close()
        self._p_pool.join()
        shutil.move(self._tmp_files.pop(), self._out)

    def _gen_tmp_file(self, *ids):
        return os.path.join(
            self._in_dir,
            '%s_%s_%s' % (self.FILE_PREFIX, self._in_name, '-'.join(ids))
        )

    def _split(self):
        fs = FileSplit(self._in, self._block_size, self._delimiter)
        count = 0
        for fp_start, fp_end in fs:
            f_name = self._gen_tmp_file(str(fp_start), str(fp_end))
            self._p_pool.apply_async(
                self._save_block,
                (fp_start, fp_end, f_name,)
            )
            count += 1
        self._count.value += count

    def _save_block(self, start, end, out_file):
        sub_file = SubFile(self._in, start, end)
        with open(out_file, 'w') as out:
            sorted_lines = sorted(
                [_ for _ in sub_file],
                key=lambda x: self._handler.row_key(x)
            )
            out.write('%s' % ''.join(sorted_lines))
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
        self._count.value -= 1

    def __getstate__(self):
        self_dict = self.__dict__.copy()
        del self_dict['_p_pool']
        return self_dict

    def __setstate__(self, state):
        self.__dict__.update(state)


class FileMerge(FileSort):

    FILE_PREFIX = '.~file_merge'

    def _save_block(self, start, end, out_file):
        sub_file = SubFile(self._in, start, end)
        with open(out_file, 'w') as out:
            sorted_lines = sorted(
                [self._handler.row_encode(_) for _ in sub_file],
                key=lambda x: self._handler.row_key_plus(x)
            )
            merged_lines = self._merge(iter(sorted_lines))
            out.write('%s\n' % '\n'.join(merged_lines))
        self._tmp_files.append(out_file)

    def _merge(self, _in):
        ret = []
        cur_line_dic = next(_in)
        for line_data in _in:
            if self._handler.row_key_plus(line_data) != self._handler.row_key_plus(cur_line_dic):
                ret.append(self._handler.row_decode(cur_line_dic))
                cur_line_dic = line_data
            else:
                cur_line_dic = self._handler.row_merge(cur_line_dic, line_data)
        ret.append(self._handler.row_decode(cur_line_dic))
        return ret

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
                    while l_line:
                        l_key = self._handler.row_key(l_line)
                        if l_key >= r_key:
                            break
                        out.write(l_line)
                        l_line = left.readline()
                elif l_key > r_key:
                    while r_line:
                        r_key = self._handler.row_key(r_line)
                        if l_key <= r_key:
                            break
                        out.write(r_line)
                        r_line = right.readline()
                elif l_key == r_key:
                    l_line = self._handler.row_decode(
                        self._handler.row_merge(
                            self._handler.row_encode(l_line),
                            self._handler.row_encode(r_line)
                        )
                    ) + '\n'
                    r_line = right.readline()
                    if r_line:
                        r_key = self._handler.row_key(r_line)

            while l_line:
                out.write(l_line)
                l_line = left.readline()
            while r_line:
                out.write(r_line)
                r_line = right.readline()
        os.remove(left_file)
        os.remove(right_file)
        self._tmp_files.append(out_file)
        self._count.value -= 1
