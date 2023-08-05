#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2022-08-25
# @Author  : wuxiangbin
# @Site    : www.0-9.ink
# @File    : model.py
# @Software: zawn_utils
# @Function:
from typing import Dict, List, Tuple, Type

from bson import ObjectId

from zawn_helper.id_helper import MakeID
from zawn_orm.database import Database, Query, Operation
from zawn_orm.exception import (
    EmptyModelException,
    InvalidFieldException,
    ExisitFieldException,
)
from zawn_orm.field import BaseField, IntegerField, field_mapping
from zawn_orm.state import BaseState
from zawn_orm.tool import get_table_name


class Model(object):
    """ 模型基类，门面模式 """

    field_list: List[Tuple[str, BaseField]] = []
    database: Database = Database()
    id_field: str = None  # 唯一字段名称
    id_prefix: str = None  # 唯一字段前缀
    table_name: str = None  # 表名
    table_prefix: str = None  # 表名前缀
    state: BaseState = BaseState()

    v = IntegerField()  # 版本号

    def __new__(cls, *args, **kwargs):
        """ 每个类有独立的单例对象 """
        instance = model_mapping.get(cls.__name__)
        if instance is None:
            instance = super().__new__(cls, **kwargs)
            model_mapping[cls.__name__] = instance
        return instance

    def __init__(self):
        self.init_table_name()  # 初始化模型的表名
        self.init_field()  # 初始化字段定义

    @classmethod
    def set_database(cls, database: Database):
        """ 设置数据库 """
        cls.database = database.init(cls)

    @classmethod
    def set_field_class(cls, field_class: Type[BaseField], force: bool = False):
        """ 设置字段类 """
        class_name = field_class.__name__
        if force:
            field_mapping.pop(class_name, None)
        elif field_mapping.pop(class_name, None):
            raise ExisitFieldException(f'已存在字段类:{class_name}')
        field_class()

    def init_table_name(self, table_name: str = ''):
        """ 初始化模型的表名 """

        if self.table_name is not None:
            return

        if table_name and isinstance(table_name, str):
            self.table_name = table_name
            return

        self.id_prefix, self.table_name = get_table_name(self.__class__)
        if self.table_prefix:
            self.table_name = '_'.join([self.table_prefix, self.table_name])

    def init_field(self):
        """ 初始化字段定义 """

        if self.field_list:
            return

        # 装载字段类型
        field_list: List[Tuple[str, BaseField]] = []
        for field_name, field_class in self.__class__.__dict__.items():
            if field_name == '__meta__' and isinstance(field_class, dict):
                for name in ['id_field', 'id_prefix', 'table_name', 'table_prefix']:
                    value = field_class.get(name)
                    if not value:
                        continue
                    self.__setattr__(name, value)

            # 过滤下划线作为前后缀的属性
            if field_name.startswith('_') or field_name.endswith('_'):
                continue

            # 过滤字段类型不是字段类的属性
            if isinstance(field_class, BaseState):
                self.state = field_class
            if not isinstance(field_class, BaseField):
                continue

            # 最后加入字段定义列表
            field_list.append((field_name, field_class))

        # 当没有获取到字段定义，则报错
        if not field_list:
            raise EmptyModelException(f'模型{self.table_name}没有定义字段')

        self.field_list = field_list

    def new_id(self) -> str:
        """ 获取一个新的id """
        return MakeID.next(self.id_prefix)

    def new_query(self, filter) -> Query:
        """ 获取一个新的查询 """
        return self.database.new_query(self.table_name).set_query(filter)

    def new_operation(self, operation: str, filter: dict, update: dict) -> Operation:
        """ 获取一个新的操作 """
        return self.database.new_operation(self.table_name).set_operation(operation, filter, update)

    def transform(self, in_data: dict, method_name: str) -> dict:
        """ 类型转换 """

        out_data = {}

        # 按照字段列表，遍历入参，将key和value转移到data
        for field_name, field_class in self.field_list:
            value = in_data.get(field_name)
            if value is None:
                continue

            # 根据方法名称，获取字段类的对应方法，将原来的值转换相应的值
            transform: callable = getattr(field_class, method_name, None)
            if transform is None:
                raise InvalidFieldException(f'字段{field_name}没有{method_name}的方法')

            # 转换类型
            out_data[field_name] = transform(value)

        return out_data

    def from_json(self, data: dict) -> dict:
        """ 转换成dict类型 """
        _id = data.get('_id')
        if _id is not None:
            data['_id'] = ObjectId(_id)
        return self.transform(data, 'from_json')

    def to_json(self, data: dict) -> dict:
        """ 转换成json类型 """
        _id = data.get('_id')
        if _id is not None:
            data['_id'] = str(_id)
        return self.transform(data, 'to_json')

    def from_db(self, data: dict) -> dict:
        """ 将数据库的数据转为dict """
        return self.transform(data, 'from_db')

    def to_db(self, data: dict) -> dict:
        """ 将dict转为数据库数据 """
        return self.transform(data, 'to_db')

    async def search(self, query: Query) -> Tuple[dict, list]:
        meta, data = await self.database.search(query)
        data = [self.from_db(i) for i in data]
        return meta, data

    async def execute(self, operation_list: List[Operation]) -> dict:
        return await self.database.execute(operation_list)


# 模型映射表
model_mapping: Dict[str, Model] = {}
