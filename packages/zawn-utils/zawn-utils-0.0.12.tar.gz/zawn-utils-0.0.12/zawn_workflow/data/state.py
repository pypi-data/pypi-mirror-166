#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2022-09-01
# @Author  : wuxiangbin
# @Site    : www.0-9.ink
# @File    : state.py
# @Software: zawn_utils
# @Function:


class WorkFlowState(object):
    """ 工作流程流程 """

    STATE_SUBMIT: str = 'S1'  # 已提交状态
    STATE_DELETE: str = 'S2'  # 已删除状态

    instance = None
    state_dict = None

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__new__(cls, *args, **kwargs)
            cls.state_dict = cls.get_state_dict()
        return cls.instance

    @classmethod
    def get_state_dict(cls, **kwargs):
        """ 获取状态字典 """
        return {
            'A1': [  # 提交
                {'from': '_', 'to': 'S1'},
            ],
            'A2': [  # 删除
                {'from': 'S1', 'to': 'S2'},
            ],
        }
