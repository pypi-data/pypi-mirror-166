#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2022-08-31
# @Author  : wuxiangbin
# @Site    : www.0-9.ink
# @File    : test_runtime.py
# @Software: zawn_utils
# @Function:
import unittest
from io import BytesIO

from zawn_workflow.context.repository import WorkFlowRepository
from zawn_workflow.data.factory import DataFactory
from zawn_workflow.test.test import TestBase


class TestRuntime(TestBase):
    """ 运行时模块测试 """

    async def test__repository__import_xlsx(self):
        """ 测试定义xlsx导入 """

        work_flow_repository = WorkFlowRepository()
        with open('测试工作流程仓库.xlsx', 'rb') as fp:
            result = await (await work_flow_repository.import_xlsx(
                xlsx_data=BytesIO(fp.read()),
                **self.other_filter,
            )).execute()

        data_factory = DataFactory()
        self.assertIn(data_factory.work_model.table_name, result)
        self.assertIn(data_factory.work_node.table_name, result)
        self.assertIn(data_factory.work_form.table_name, result)


if __name__ == '__main__':
    unittest.main()
