#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2022-08-25
# @Author  : wuxiangbin
# @Site    : www.0-9.ink
# @File    : tool.py
# @Software: zawn_utils
# @Function:

def get_table_name(model_class):
    """ 获取模型类的名字，转换成表名 """

    prefix_list = []
    chat_list = []
    for i in model_class.__name__:
        if i == i.upper():
            prefix_list.append(i)  # 大写前缀
            chat_list.append('_')
            chat_list.append(i.lower())
        else:
            chat_list.append(i)
    if chat_list[0] == '_':
        chat_list.pop(0)
    return ''.join(prefix_list), ''.join(chat_list)
