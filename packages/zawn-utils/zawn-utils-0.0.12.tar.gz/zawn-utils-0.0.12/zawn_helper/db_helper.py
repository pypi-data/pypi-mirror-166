#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2022-08-21
# @Author  : wuxiangbin
# @Site    : www.0-9.ink
# @File    : db_helper.py
# @Software: zawn_utils
# @Function:
from typing import List


class DBOperation(object):
    """ 数据库操作声明类 """

    _default_database: str = 'test'
    _operation_list: List[str] = [
        'InsertOne',
        'UpdateOne', 'UpdateMany',
        'DeleteOne', 'DeleteMany',
    ]

    def __init__(
            self,
            database: str = None,
            collection: str = None,
            operation: str = None,
            filter: dict = None,
            update: dict = None,
    ):
        self._database = database or self._default_database
        self._collection = collection
        self._operation = operation
        self._filter = filter
        self._update = update

    def __str__(self) -> str:
        database = self.database
        collection = self.collection
        operation = self.operation
        filter = self.filter
        update = self.update
        return f'{database}.{collection}.{operation}({filter=}, {update=})'

    def __repr__(self) -> str:
        return self.__str__()

    @property
    def database(self) -> str:
        return self._database

    @database.setter
    def database(self, value: str):
        self._database = value

    @property
    def collection(self) -> str:
        return self._collection

    @collection.setter
    def collection(self, value: str):
        self._collection = value

    @property
    def operation(self) -> str:
        return self._operation

    @operation.setter
    def operation(self, value: str):
        if value not in self._operation_list:
            raise ValueError(f'{value}不是支持的操作类型')
        self._operation = value

    @property
    def filter(self) -> dict:
        return self._filter

    @filter.setter
    def filter(self, value: dict):
        self._filter = value

    @property
    def update(self) -> dict:
        return self._update

    @update.setter
    def update(self, value: dict):
        self._update = value
