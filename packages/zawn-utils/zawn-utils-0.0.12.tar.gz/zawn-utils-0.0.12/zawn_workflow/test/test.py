#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2022-08-02
# @Author  : wuxiangbin
# @Site    : www.0-9.ink
# @File    : test.py
# @Software: property
# @Function:

import pandas as pd

from zawn_workflow.context.base import NodeFactory, Context

node_list = [
    {
        'node_id': 'node01',
        'node_name': '串行',
        'node_type': 'root',
        'sort': 1,
        'parent_id': '',
    },
    {
        'node_id': 'node02',
        'node_name': '发起人',
        'node_type': 'originate',
        'sort': 2,
        'parent_id': 'node01',
    },
    {
        'node_id': 'node03',
        'node_name': '条件',
        'node_type': 'condition',
        'sort': 3,
        'parent_id': 'node01',
    },
    {
        'node_id': 'node04',
        'node_name': '部门主管',
        'node_type': 'approval',
        'sort': 4,
        'parent_id': 'node03',
    },
    {
        'node_id': 'node05',
        'node_name': '并行',
        'node_type': 'parallel',
        'sort': 5,
        'parent_id': 'node03',
    },
    {
        'node_id': 'node06',
        'node_name': '副总经理',
        'node_type': 'approval',
        'sort': 6,
        'parent_id': 'node05',
    },
    {
        'node_id': 'node07',
        'node_name': '总经理',
        'node_type': 'approval',
        'sort': 7,
        'parent_id': 'node05',
    },
    {
        'node_id': 'node08',
        'node_name': '会签',
        'node_type': 'join',
        'sort': 8,
        'parent_id': 'node01',
    },
    {
        'node_id': 'node09',
        'node_name': '财务总监',
        'node_type': 'approval',
        'sort': 9,
        'parent_id': 'node08',
    },
    {
        'node_id': 'node10',
        'node_name': '董事会',
        'node_type': 'approval',
        'sort': 10,
        'parent_id': 'node08',
    },
    {
        'node_id': 'node11',
        'node_name': '出纳',
        'node_type': 'approval',
        'sort': 11,
        'parent_id': 'node01',
    },
]

import json
import unittest
from io import BytesIO

from zawn_orm.impl.mongodb import MongoDB
from zawn_orm.model import Model

with open('../../uri.json', 'rb') as fp:
    config = json.load(fp)


class TestBase(unittest.IsolatedAsyncioTestCase):
    """ 测试基类 """

    async def asyncSetUp(self) -> None:
        self.other_filter = {'org_id': '_'}
        database = MongoDB()
        await database.connect(config['mongodb_uri'])
        Model().set_database(database)


if __name__ == '__main__':
    context: Context = NodeFactory.make_node(
        node_list=node_list,
    )
    root_node = context.root_node
    context.data = {'originator_id': '-'}

    if root_node is None:
        raise Exception('根节点为空')

    status = root_node.tick()
    print(status)

    node_list = root_node.to_node_list()
    for i in node_list:
        print(i)

    print(node_list)

    with open('/Users/wuxiangbin/Desktop/工作流程_身份表.xlsx', 'rb') as fp:
        xlsx_data = BytesIO(fp.read())

    data = pd.read_excel(
        xlsx_data, 0, engine='openpyxl', dtype='str'
    ).fillna('-').to_dict(orient='records')
    for i in data:
        print(i, i['组A'])
