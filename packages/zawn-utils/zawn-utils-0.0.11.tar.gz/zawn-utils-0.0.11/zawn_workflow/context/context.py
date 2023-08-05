#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2022-08-22
# @Author  : wuxiangbin
# @Site    : www.0-9.ink
# @File    : context.py
# @Software: zawn_utils
# @Function:
import logging
from io import BytesIO
from typing import List, Tuple, Union

import pandas

from zawn_orm.database import Operation, Query
from zawn_orm.model import Model
from zawn_workflow.data.factory import DataFactory

response_mapping = {
    '000': (0, '操作成功'),
    '001': (0, '查询成功'),
    '002': (2, '未找到用户信息'),
    '020': (20, '找到的记录并不唯一，无法启动工作流程'),
    '999': (-1, '未知状态'),
}


class BaseContext(object):
    """ 上下文基类 """

    model = Model()
    data_factory = DataFactory()
    logger = logging

    operation_flag: bool = False  # 操作标识，True时不允许继续操作，表示有其他操作正在执行
    operation_list: List[Operation] = []
    query: Query = None

    def response_data(
            self, key: str, data: Union[list, dict], extra: list = None) -> Tuple[int, str, Union[list, dict]]:
        """ 响应数据 """

        code, message = response_mapping.get(key) or response_mapping.get('999')
        if extra and isinstance(extra, (list, tuple)):
            message = ':'.join([message, *extra])
        return code, message, data

    def read_xlsx(self, xlsx_data: BytesIO, sheet_index: int = 0) -> List[dict]:
        """ 读取xlsx文件 """
        data = pandas.read_excel(
            xlsx_data, sheet_index, engine='openpyxl', dtype='str',
        ).fillna('').to_dict(orient='records')
        return data

    async def execute(self) -> dict:
        """ 执行数据库操作 """
        if self.operation_flag:
            return {}

        self.operation_flag = True
        result = await self.model.execute(self.operation_list)
        self.operation_flag = False

        return result

    async def search(self) -> Tuple[dict, list]:
        """ 执行数据库查询 """
        data = await self.model.search(self.query)
        return data
