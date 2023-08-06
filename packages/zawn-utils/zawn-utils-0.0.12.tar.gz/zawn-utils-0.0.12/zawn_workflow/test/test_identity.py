#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2022-08-21
# @Author  : wuxiangbin
# @Site    : www.0-9.ink
# @File    : test_identity.py
# @Software: zawn_utils
# @Function:
import json
import unittest
from io import BytesIO

from zawn_workflow.context.identity import WorkFlowIdentity
from zawn_workflow.data.factory import DataFactory
from zawn_workflow.test.test import TestBase

with open('../../uri.json', 'rb') as fp:
    config = json.load(fp)


class TestIdentity(TestBase):
    """ 身份模块测试 """

    async def test__identity__import_xlsx(self):
        """ 测试身份xlsx导入 """

        work_flow_identity = WorkFlowIdentity()
        with open('测试用户身份.xlsx', 'rb') as fp:
            result = await work_flow_identity.import_xlsx(
                xlsx_data=BytesIO(fp.read()),
                **self.other_filter,
            ).execute()

        data_factory = DataFactory()
        self.assertIn(data_factory.work_user.table_name, result)
        self.assertIn(data_factory.work_group.table_name, result)


if __name__ == '__main__':
    unittest.main()
