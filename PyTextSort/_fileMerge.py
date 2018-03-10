#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    hack by djj -_,- | good luck!
    date: 2018-03-10
"""


def merge(in_f, out_f, handler, merge_func=lambda dic1, dic2: dict(dic1, **dic2)):
    in_fp = open(in_f, 'r')
    out_fp = open(out_f, 'w')
    cur_line_dic = handler.row_encode(in_fp.readline())

    for line in in_fp:
        line_data = handler.row_encode(line)
        if handler.row_key_plus(line_data) != handler.row_key_plus(cur_line_dic):
            out_fp.write('%s\n' % handler.row_decode(line_data))
            cur_line_dic = line_data
            continue
        cur_line_dic = merge_func(cur_line_dic, line_data)
    out_f.write('%s\n' % handler.row_encode(cur_line_dic))
    out_f.close()


def merge_func1(dic1, dic2):
    for k, v in dic1.items():
        if v and isinstance(v, list):
            vals = dic2.get(k, [])
            if vals is None:
                vals = []
            if isinstance(v[0], dict):
                tmp_vals = [_ for _ in v if _ not in vals]
                vals += tmp_vals
            else:
                vals = list(set(vals + v))
            dic2[k] = vals
        elif v is None or (isinstance(v, (dict, list)) and len(v) == 0):
            continue
        else:
            dic2[k] = v
    return dic2
