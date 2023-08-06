#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2022-07-19
# @Author  : wuxiangbin
# @Site    : www.0-9.ink
# @File    : util.py
# @Software: property
# @Function:
from datetime import datetime
from decimal import Decimal

import motor.motor_asyncio
from motor.core import AgnosticClient


def get_collection_name(document_class) -> str:
    """ 获取集合名 """

    chat_list = []
    for i in document_class.__name__:
        if i == i.upper():
            chat_list.append('_')
            chat_list.append(i.lower())
        else:
            chat_list.append(i)
    if chat_list[0] == '_':
        chat_list.pop(0)
    return ''.join(chat_list)


def get_type_name(obj: object) -> str:
    """ 获取类型名称 """

    if isinstance(obj, str):
        return 'string'
    elif isinstance(obj, int):
        return 'integer'
    elif isinstance(obj, float):
        return 'float'
    elif isinstance(obj, datetime):
        return 'datetime'
    elif isinstance(obj, Decimal):
        return 'decimal'
    elif isinstance(obj, list):
        return 'list'
    elif isinstance(obj, dict):
        return 'dict'
    else:
        return 'object'


def get_client(uri: str) -> AgnosticClient:
    """ 获取数据库客户端 """
    return motor.motor_asyncio.AsyncIOMotorClient(uri, tz_aware=True)
