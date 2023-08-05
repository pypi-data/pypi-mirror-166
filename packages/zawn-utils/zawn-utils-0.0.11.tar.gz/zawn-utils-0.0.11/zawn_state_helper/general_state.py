#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2022-07-21
# @Author  : wuxiangbin
# @Site    : www.0-9.ink
# @File    : general_state.py
# @Software: property
# @Function:

from zawn_state_helper import base


class GeneralContext(base.BaseContext):
    """ 一般上下文类 """

    def __init__(self, ):
        state_class_list = list(GeneralState.__subclasses__())
        super().__init__(state_class_list)


class GeneralState(base.BaseState):
    """ 一般状态类 """

    def input(self, context: base.BaseContext) -> bool:
        """ 录入事件 """
        return False

    def submit(self, context: base.BaseContext) -> bool:
        """ 提交事件 """
        return False

    def delete(self, context: base.BaseContext) -> bool:
        """ 删除事件 """
        return False

    def approve(self, context: base.BaseContext) -> bool:
        """ 审核事件 """
        return False

    def refuse(self, context: base.BaseContext) -> bool:
        """ 拒绝事件 """
        return False

    def agree(self, context: base.BaseContext) -> bool:
        """ 同意事件 """
        return False

    def publish(self, context: base.BaseContext) -> bool:
        """ 发布事件 """
        return False

    def withdraw(self, context: base.BaseContext) -> bool:
        """ 撤回事件 """
        return False

    def cancel(self, context: base.BaseContext) -> bool:
        """ 作废事件 """
        return False


class DraftState(GeneralState):
    """ 草稿状态类 """

    name = '草稿状态'
    status = 'S1'

    def input(self, context: base.BaseContext) -> bool:
        context.set_state(DraftState())
        return True

    def submit(self, context: base.BaseContext) -> bool:
        context.set_state(RecordedState())
        return True

    def approve(self, context: base.BaseContext) -> bool:
        context.set_state(ReviewedState())
        return True


class RecordedState(GeneralState):
    """ 已录入状态类 """

    name = '已录入状态'
    status = 'S2'


class DeletedState(GeneralState):
    """ 已删除状态类 """

    name = '已删除状态'
    status = 'S3'


class ReviewedState(GeneralState):
    """ 审核中状态类 """

    name = '审核中状态'
    status = 'S4'


class ApprovalState(GeneralState):
    """ 审核中状态类 """

    name = '已审批状态'
    status = 'S5'


class PublishedState(GeneralState):
    """ 已发布状态类 """

    name = '已发布状态'
    status = 'S6'


class WithdrawnState(GeneralState):
    """ 已撤回状态类 """

    name = '已撤回状态'
    status = 'S7'


class RevokedState(GeneralState):
    """ 已作废状态类 """

    name = '已作废状态'
    status = 'S8'


if __name__ == '__main__':
    s1 = DraftState()
    context = GeneralContext()

    is_success = context.request('approve', s1.status)
    if not is_success:
        print('没有该事件')
    s4 = context.get_status_value()
    print(s4)

    is_success = context.request('submit')
    if not is_success:
        print('没有该事件')
    s2 = context.get_status_value()
    print(s2)
