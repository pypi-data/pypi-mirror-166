#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2022-07-19
# @Author  : wuxiangbin
# @Site    : www.0-9.ink
# @File    : id_helper.py
# @Software: property
# @Function:
import os
import socket
import time


def get_machine_number(mod_number=65536):
    """ 根据主机名称和进程号生成机器号码 """
    hostname = socket.gethostname().encode('utf-8')
    machine_number = os.getpid()
    for i in hostname:
        machine_number = ((machine_number << 8) + i) % mod_number
    return machine_number


class MakeID(object):
    '''生成code'''
    sn = int(time.time()) % 65536
    maps = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    length = len(maps)
    mod_number = length ** 2
    pid = get_machine_number(length ** 4)

    @classmethod
    def mod(cls, num, length):
        ids = []
        while num >= length:
            num, y = divmod(num, length)
            ids.append(cls.maps[y])
        ids.append(cls.maps[num])
        id = ''.join(ids[::-1])
        return id

    @classmethod
    def next(cls, prefix='', code_length=16, size_type: str = 'long'):
        cls.sn = (cls.sn + 1) % cls.mod_number
        fid = cls.maps[0] * code_length
        tid = f'{cls.mod(int(time.time() * 1000), cls.length):0>6}'
        pid = f'{cls.mod(cls.pid, cls.length):0>4}'
        sid = f'{cls.mod(cls.sn, cls.length):0>2}'
        id = (fid + tid + pid + sid)[-code_length + len(prefix):]
        code = prefix + id
        return code
