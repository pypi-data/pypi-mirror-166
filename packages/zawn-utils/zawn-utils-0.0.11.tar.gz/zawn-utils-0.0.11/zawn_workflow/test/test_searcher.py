#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2022-08-31
# @Author  : wuxiangbin
# @Site    : www.0-9.ink
# @File    : test_searcher.py
# @Software: zawn_utils
# @Function:
import unittest

from zawn_workflow.context.searcher import WorkFlowSearcher
from zawn_workflow.test.test import TestBase


class TestSearcher(TestBase):
    """ 查询器模块测试 """

    async def test__searcher__search_user(self):
        """ 测试用户信息查询 """

        work_flow_searcher = WorkFlowSearcher()
        user_id_list = ['U0006', 'U0007']

        meta, data = await (await work_flow_searcher.search_user(user_id_list, **self.other_filter)).search()

        self.assertEqual(meta['total'], 2)
        self.assertIn(data[0]['user_name'], ['成铭衔05', '成铭衔06'])

    async def test__searcher__search_model(self):
        """ 测试工作模型查询 """

        work_flow_searcher = WorkFlowSearcher()
        model_key = 'test_workflow_01'

        meta, data = await (await work_flow_searcher.search_model(model_key=model_key, **self.other_filter)).search()

        self.assertEqual(meta['total'], 1)
        self.assertEqual(data[0]['model_key'], model_key)

    async def test__searcher__search_model_detail(self):
        """ 测试工作模型详情查询 """

        work_flow_searcher = WorkFlowSearcher()
        model_id = 'WM0001'

        meta, data = await (
            await work_flow_searcher.search_model_detail(model_id=model_id, **self.other_filter)).search()

        self.assertEqual(meta['total'], 1)
        self.assertEqual(len(data[0]['nodes']), 11)


if __name__ == '__main__':
    unittest.main()
