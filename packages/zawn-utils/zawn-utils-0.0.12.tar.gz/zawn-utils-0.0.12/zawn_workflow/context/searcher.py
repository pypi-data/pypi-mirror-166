#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2022-08-20
# @Author  : wuxiangbin
# @Site    : www.0-9.ink
# @File    : searcher.py
# @Software: zawn_utils
# @Function:
from typing import List

from zawn_helper.search_helper import SearchHelper
from zawn_workflow.context.context import BaseContext


class WorkFlowSearcher(BaseContext):
    """ 工作流程查询器 """

    async def search_user(self, user_id_list: List[str], **kwargs):
        """ 查询工作用户 """

        self.query = self.data_factory.work_user.new_query({
            'user_id': {'$in': user_id_list},
            **kwargs,
        })

        return self

    async def search_group(self):
        """ 查询工作用户组 """
        pass

    async def search_model(self, model_id: str = None, model_key: str = None, **kwargs):
        """ 查询工作模型 """

        filter = kwargs
        if model_id:
            filter['model_id'] = model_id
        if model_key:
            filter['model_key'] = model_key

        self.query = self.data_factory.work_model.new_query(filter)

        return self

    async def search_model_detail(self, model_id: str, **kwargs):
        """ 查询工作模型详情 """

        work_model = self.data_factory.work_model
        work_node = self.data_factory.work_node
        work_form = self.data_factory.work_form

        filter = {
            **kwargs,
            'model_id': model_id,
            '$pipeline': [
                *SearchHelper.join(
                    work_node.table_name, 'model_id', 'model_id',
                    'nodes',
                ),
                *SearchHelper.join(
                    work_form.table_name, 'nodes.form_label', 'form_label',
                    'forms',
                ),
            ],
        }
        self.query = work_model.new_query(filter)

        return self

    async def search_node(self):
        """ 查询工作节点 """
        pass

    async def search_form(self):
        """ 查询工作表单 """
        pass

    async def search_instance(self):
        """ 查询工作实例 """
        pass

    async def search_task(self):
        """ 查询工作任务 """
        pass

    async def search_value(self):
        """ 查询工作表单值 """
        pass
