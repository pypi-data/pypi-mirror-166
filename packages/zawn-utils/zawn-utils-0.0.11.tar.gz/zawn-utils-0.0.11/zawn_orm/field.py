#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2022-08-25
# @Author  : wuxiangbin
# @Site    : www.0-9.ink
# @File    : field.py
# @Software: zawn_utils
# @Function:
from datetime import datetime
from decimal import Decimal
from typing import List, Union, Dict

from zawn_orm.exception import InvalidValueException


class BaseField(object):
    """ 基础字段类 """
    field_type = '__base'
    instance: 'BaseField' = None

    def __new__(cls, *args, **kwargs):
        """ 每个类有独立的单例对象 """
        instance = field_mapping.get(cls.__name__)
        if instance is None:
            instance = super().__new__(cls, **kwargs)
            field_mapping[cls.__name__] = instance
        return instance

    def __init__(self, **kwargs):
        pass

    def on_transform(self, value: object) -> object:
        return value

    def from_json(self, value):
        """ 将json数据转为dict """
        if isinstance(self.instance, BaseField):
            return self.instance.on_from_json(value)
        return self.on_from_json(value)

    def to_json(self, value):
        """ 将dict转为json """
        if isinstance(self.instance, BaseField):
            return self.instance.on_to_json(value)
        return self.on_to_json(value)

    def from_db(self, value):
        """ 将数据库的数据转为dict """
        if isinstance(self.instance, BaseField):
            return self.instance.on_from_db(value)
        return self.on_from_db(value)

    def to_db(self, value):
        """ 将dict转为数据库数据 """
        if isinstance(self.instance, BaseField):
            return self.instance.on_to_db(value)
        return self.on_to_db(value)

    def on_from_json(self, value: object) -> object:
        return self.on_transform(value)

    def on_to_json(self, value: object) -> object:
        return self.on_transform(value)

    def on_from_db(self, value: object) -> object:
        return self.on_transform(value)

    def on_to_db(self, value: object) -> object:
        return self.on_transform(value)


class ObjectField(BaseField):
    """ 对象字段类 """
    field_type = 'object'


class ArrayField(BaseField):
    """ 数组字段类 """
    field_type = 'array'

    def on_transform(self, value: Union[list, tuple]) -> list:
        return list(value)


class BooleanField(BaseField):
    """ 布尔字段类 """
    field_type = 'boolean'

    def on_transform(self, value: object) -> bool:
        return bool(value)


class StringField(BaseField):
    """ 字符串字段类 """
    field_type = 'string'

    def on_transform(self, value: object) -> str:
        return str(value)


class FloatField(BaseField):
    """ 浮点数字字段类 """
    field_type = 'float'

    def on_transform(self, value: Union[str, int, float, Decimal]) -> float:
        return float(value)


class IntegerField(BaseField):
    """ 整型数字字段类 """
    field_type = 'integer'

    def on_transform(self, value: Union[str, int, float, Decimal]) -> int:
        return int(value)


class DecimalField(BaseField):
    """ 十进制数字字段类 """
    field_type = 'decimal'

    def on_transform(self, value: Union[str, int, float, Decimal]) -> Decimal:
        return Decimal(value)


class DatetimeField(BaseField):
    """ 日期时间字段类 """
    field_type = 'datetime'
    datetime_format = '%Y-%m-%dT%H:%M:%S.%f%z'

    def on_from_json(self, value: Union[str, int, float]) -> datetime:
        if isinstance(value, str):
            return datetime.strptime(value, self.datetime_format).astimezone()
        elif isinstance(value, (int, float)):
            return datetime.fromtimestamp(int(value / 1000)).astimezone()
        elif isinstance(value, datetime):
            return value.astimezone()

        raise InvalidValueException(f'{str(value)}无法转换成{self.field_type}类型')

    def on_to_json(self, value: Union[datetime]) -> str:
        if isinstance(value, datetime):
            return value.astimezone().strftime(self.datetime_format)

        raise InvalidValueException(f'{str(value)}无法转换成{self.field_type}类型')

    def on_from_db(self, value: Union[str, int, float]) -> datetime:
        if isinstance(value, str):
            return datetime.strptime(value, self.datetime_format).astimezone()
        elif isinstance(value, (int, float)):
            return datetime.fromtimestamp(int(value / 1000)).astimezone()
        elif isinstance(value, datetime):
            return value.astimezone()

        raise InvalidValueException(f'{str(value)}无法转换成{self.field_type}类型')

    def on_to_db(self, value: Union[datetime]) -> datetime:
        if isinstance(value, str):
            return datetime.strptime(value, self.datetime_format).astimezone()
        elif isinstance(value, (int, float)):
            return datetime.fromtimestamp(int(value / 1000)).astimezone()
        elif isinstance(value, datetime):
            return value.astimezone()

        raise InvalidValueException(f'{str(value)}无法转换成{self.field_type}类型')


class EmbeddedDictField(BaseField):
    """ 内嵌字段字段类 """
    field_type = 'dict'

    def __init__(self, model, **kwargs):
        super().__init__(**kwargs)
        from zawn_orm.model import Model
        self.model: Model = model()

    def on_from_json(self, value: dict) -> dict:
        return self.model.from_json(value or {})

    def on_to_json(self, value: dict) -> dict:
        return self.model.to_json(value or {})

    def on_from_db(self, value: dict) -> dict:
        return self.model.from_db(value or {})

    def on_to_db(self, value: dict) -> dict:
        return self.model.to_db(value or {})


class EmbeddedListField(BaseField):
    """ 内嵌列表字段类 """
    field_type = 'list'

    def __init__(self, model, **kwargs):
        super().__init__(**kwargs)
        from zawn_orm.model import Model
        self.model: Model = model()

    def on_from_json(self, value: List[dict]) -> List[dict]:
        return [self.model.from_json(i) for i in (value or [])]

    def on_to_json(self, value: List[dict]) -> List[dict]:
        return [self.model.to_json(i) for i in (value or [])]

    def on_from_db(self, value: List[dict]) -> List[dict]:
        return [self.model.from_db(i) for i in (value or [])]

    def on_to_db(self, value: List[dict]) -> List[dict]:
        return [self.model.to_db(i) for i in (value or [])]


field_mapping: Dict[str, BaseField] = {}
# class Fields(object):
#     """ 字段集合 """
#
#     BaseField: Type[BaseField] = BaseField
#     ObjectField: Type[BaseField] = ObjectField
#     ArrayField: Type[BaseField] = ArrayField
#     BooleanField: Type[BaseField] = BooleanField
#     StringField: Type[BaseField] = StringField
#     FloatField: Type[BaseField] = FloatField
#     IntegerField: Type[BaseField] = IntegerField
#     DecimalField: Type[BaseField] = DecimalField
#     DatetimeField: Type[BaseField] = DatetimeField
#     EmbeddedDictField: Type[BaseField] = EmbeddedDictField
#     EmbeddedListField: Type[BaseField] = EmbeddedListField
