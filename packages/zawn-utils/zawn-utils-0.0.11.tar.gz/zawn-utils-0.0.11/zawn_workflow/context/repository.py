#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2022-08-20
# @Author  : wuxiangbin
# @Site    : www.0-9.ink
# @File    : repository.py
# @Software: zawn_utils
# @Function:
import datetime
from io import BytesIO
from typing import List

from zawn_orm.database import Operation
from zawn_workflow.context.base import NodeFactory
from zawn_workflow.context.context import BaseContext


class WorkFlowRepository(BaseContext):
    """ 工作流程仓库 """

    def import_form_data(self, form_data: list, **kwargs) -> BaseContext:
        """ 导入表单数据 """

        now = datetime.datetime.now().astimezone()
        op = kwargs.get('op', 'system')
        work_form = self.data_factory.work_form

        form_dict = {}
        form_label_list = []
        for row in form_data:
            form_id = row['表单编号']
            form_label = row['表单标签']
            form_dict[form_id] = {
                'form_id': form_id,
                'form_label': form_label,
                'form_name': row['表单字段'],
                'form_type': row['表单类型'],
                'placeholder': row['占位符'],
                'disabled': row['能否编辑'] in ['Y', '能', '是'],
                'required': row['是否必填'] in ['Y', '能', '是'],
                **kwargs,
            }
            form_label_list.append(form_label)

        # 更新旧表单的状态为已删除
        self.operation_list.append(work_form.new_operation(
            'update',
            filter={'form_label': {'$in': list(set(form_label_list))}, **kwargs},
            update={'$set': work_form.to_db({'status': work_form.state.DELETE, 'update_at': now, 'update_by': op})},
        ))

        # 新增表单
        for _, form in form_dict.items():
            self.operation_list.append(work_form.new_operation(
                'insert',
                filter={},
                update=work_form.to_db(form)
            ))

        return self

    def import_model_data(
            self, model_data: list, **kwargs) -> BaseContext:
        """ 导入模型列表 """

        work_model = self.data_factory.work_model
        model_dict = {}
        for row in model_data:
            model_id = row['模型编号']
            model_dict[model_id] = {
                'model_id': model_id,
                'model_key': row['模型KEY'],
                'model_type': row['模型分类'],
                'model_name': row['模型名称'],
                **kwargs,
            }

        for _, v in model_dict.items():
            self.operation_list.append(work_model.new_operation(
                'insert',
                filter={},
                update=work_model.to_db(v)
            ))

        return self

    def import_node_data(self, node_data: list, **kwargs) -> BaseContext:
        """ 导入节点列表 """

        work_node = self.data_factory.work_node
        node_dict = {}
        for i, row in enumerate(node_data):
            node_id = row['节点编号']
            model_id = row['模型编号']
            if model_id not in node_dict:
                node_dict[model_id] = []
            node_dict[model_id].append({
                'node_id': node_id,
                'parent_id': row['父节点编号'],
                'node_name': row['节点名称'],
                'node_type': row['节点类型'],
                'sort': i,
                'form_label': row['表单标签'],
                'model_id': model_id,
                **kwargs,
            })

        for model_id, node_list in node_dict.items():
            context = NodeFactory.make_node(node_list)
            if context is None:
                continue

            for node in context.root_node.to_node_list():
                self.operation_list.append(work_node.new_operation(
                    'insert',
                    filter={},
                    update=work_node.to_db(node)
                ))

        return self

    def import_xlsx(self, xlsx_data: BytesIO, **kwargs):
        """ 导入定义表格 """

        form_data = self.read_xlsx(xlsx_data, 0)
        model_data = self.read_xlsx(xlsx_data, 1)
        node_data = self.read_xlsx(xlsx_data, 2)
        if not (model_data and node_data and form_data):
            return self

        # 清空所有用户和用户组数据，重新写入最新数据
        self.operation_list: List[Operation] = [
            self.data_factory.work_model.new_operation(
                'delete',
                filter=kwargs,
                update={}
            ),
            self.data_factory.work_node.new_operation(
                'delete',
                filter=kwargs,
                update={}
            ),
            self.data_factory.work_form.new_operation(
                'delete',
                filter=kwargs,
                update={}
            ),
        ]

        self.import_form_data(form_data, **kwargs)
        self.import_model_data(model_data, **kwargs)
        self.import_node_data(node_data, **kwargs)
        return self
