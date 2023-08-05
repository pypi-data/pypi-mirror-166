#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2022-07-21
# @Author  : wuxiangbin
# @Site    : www.0-9.ink
# @File    : base.py
# @Software: property
# @Function:
from typing import List, Type


class BaseState(object):
    """ 状态模式:基础状态类 """

    name = '基础状态'
    status = 'S0'

    def __str__(self):
        return f'{self.status}_{self.name}'

    def __repr__(self):
        return self.name


class BaseContext(object):
    """ 状态模式:基础上下文类 """

    def __init__(self, state_class_list: List[Type[BaseState]]):
        self.state_class_mapping = {i.status: i for i in state_class_list}
        self.default_status = state_class_list[0].status

    def set_state(self, state: BaseState):
        """ 设置状态 """

        self.state = state

    def get_status_value(self) -> str:
        """ 获取状态值 """

        return self.state.status

    def request(self, action_name: str, current_status: str = None) -> str:
        """ 请求状态转换 """

        if current_status is None:
            current_status = self.default_status

        if current_status not in self.state_class_mapping:
            raise KeyError(f'{current_status}不存在')

        state = self.state_class_mapping[current_status]()
        if not hasattr(state, action_name):
            raise ValueError(f'{state}没有{action_name}事件')

        is_success = getattr(state, action_name)(self)
        if not is_success:
            return self.default_status

        return self.get_status_value()
