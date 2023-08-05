#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2022-08-25
# @Author  : wuxiangbin
# @Site    : www.0-9.ink
# @File    : database.py
# @Software: zawn_utils
# @Function:
import logging
from typing import List, Dict, Tuple

from zawn_orm.exception import InvalidOperationException


class Query(object):
    """ 数据库查询类 """

    table_name: str = None
    filter: dict = None
    max_length: int = 100

    def __init__(self, table_name: str):
        self.table_name = table_name
        self.filter = {}

    def set_query(self, filter: dict) -> 'Query':
        """ 设置查询条件 """
        self.filter = filter
        return self

    def get_query(self):
        """ 获取查询条件 """
        return self.filter


class Operation(object):
    """ 数据库操作类 """

    table_name: str = None
    operation: str = None
    filter: dict = None
    update: dict = None

    def __init__(self, table_name: str):
        self.table_name = table_name

    def set_operation(self, operation: str, filter: dict, update: dict) -> 'Operation':
        """ 设置操作属性 """

        if operation not in ['insert', 'update', 'delete']:
            raise InvalidOperationException(f'{operation}是无效操作')

        self.operation = operation
        self.filter = filter
        self.update = update

        return self

    def get_operation(self):
        return self.table_name, self.operation, self.filter, self.update


class Database(object):
    """ 数据库基类 """

    singleton_mapping: Dict[str, 'Database'] = {}
    database_type: str = 'base'
    client = None
    database = None

    class OperationCount(object):
        insert: int = 0
        update: int = 0
        delete: int = 0

        def result(self) -> dict:
            return {
                'insert': self.insert,
                'update': self.update,
                'delete': self.delete,
            }

        def __str__(self) -> str:
            return str(self.result())

        def __repr__(self) -> str:
            return str(self.result())

    def __new__(cls, *args, **kwargs):
        """ 每个类有独立的单例对象 """
        instance = cls.singleton_mapping.get(cls.__name__)
        if instance is None:
            instance = super().__new__(cls, **kwargs)
            cls.singleton_mapping[cls.__name__] = instance
        return instance

    def __init__(self):
        pass

    def init(self, model_class, **kwargs):
        return self

    async def connect(self, uri: str):
        pass

    async def close(self):
        pass

    def new_query(self, table_name: str) -> Query:
        """ 获取一个新的查询 """
        return Query(table_name)

    def new_operation(self, table_name: str) -> Operation:
        """ 获取一个新的操作 """
        operation = Operation(table_name)
        return operation

    async def search(self, query: Query) -> Tuple[dict, list]:
        try:
            return await self.on_search(query)
        except Exception as e:
            logging.error(f'数据库执行查询时出错{e}', exc_info=True)
            return {'skip': 0, 'limit': 0, 'total': 0}, []

    async def on_search(self, query: Query) -> Tuple[dict, list]:
        return {'skip': 0, 'limit': 0, 'total': 0}, []

    async def execute(self, operation_list: List[Operation]) -> dict:
        try:
            return await self.on_execute(operation_list)
        except Exception as e:
            logging.error(f'数据库执行变更时出错{e}', exc_info=True)
            return {}

    async def on_execute(self, operation_list: List[Operation]) -> dict:
        result = {i.table_name: {} for i in operation_list}
        return result
