#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2022-08-01
# @Author  : wuxiangbin
# @Site    : www.0-9.ink
# @File    : base.py
# @Software: property
# @Function:
import logging
from abc import ABC
from typing import Union, List, Optional, Type

from zawn_workflow.data.exception import NodeNotFoundError


class NodeType(object):
    """ 节点类型 """

    root = 'root'  # 根
    originate = 'originate'  # 发起
    approval = 'approval'  # 审批
    serial = 'serial'  # 串行
    join = 'join'  # 会签
    parallel = 'parallel'  # 并行
    condition = 'condition'  # 条件
    loop = 'loop'  # 循环


class NodeStatus(object):
    """ 节点状态 """

    FUTURE: str = 'FUTURE'  # 现在还没有走到的节点状态
    WAITING: str = 'WAITING'  # 只有复杂节点有该状态，表示在等待子节点审批
    READY: str = 'READY'  # 可以进行审批操作的简单节点是Ready状态
    SKIP: str = 'SKIP'  # 当一个并行节点的子节点状态为非(Ready, Waiting)时，其它兄弟节点及其子节点的状态被置为Skip
    COMPLETE: str = 'COMPLETE'  # 已经审批完成的节点状态


class HandlerType(object):
    """ 处理人类型 """

    STATIC: str = 'STATIC'  # 设计阶段静态录入人员
    FORM: str = 'FORM'  # 运行阶段表单动态录入人员
    RELATION: str = 'RELATION'  # 通过映射函数获取人员


class Context(object):
    """ 上下文类 """

    def __init__(self):
        self.root_node: Optional[Node] = None
        self._data: List[dict] = []
        self._node_dict: dict = {}

    @property
    def data(self) -> dict:
        return_data: dict = self._data.pop(0) if len(self._data) > 0 else {}
        return return_data

    @data.setter
    def data(self, value: dict):
        self._data.append(value)

    def register(self, node: 'Node'):
        """ 注册节点信息 """
        if self.root_node is None:
            self.root_node = node
        self._node_dict[node.node_id] = node

    def get_node(self, node_id: str) -> 'Node':
        """ 通过node_id获取节点 """
        return self._node_dict.get(node_id)

    def change_status(self, node_id: str, status: str):
        """ 修改节点状态 """
        try:
            node = self._node_dict[node_id]
            node.status = status
        except Exception as e:
            message = f'{e}'
            logging.error(message, exc_info=True)

    def tick(self, form_data: dict) -> 'Context':
        """ 嘀嗒方法，每帧刷新新数据 """
        self._data = form_data
        self.root_node.tick()
        return self

    def to_node_list(self, node_list: List[dict] = None, parent_id: str = '', mapping: dict = None) -> List[dict]:
        """ 转成节点列表 """
        self.root_node.to_node_list(node_list=node_list, parent_id=parent_id, mapping=mapping)


class Node(ABC):
    """ 节点类 """
    node_type = 'base'

    def __init__(self, node_id: str, node_name: str, raw_data: dict):
        self.node_id: str = node_id
        self.node_name: str = node_name
        self.parent: Optional[Node] = None
        self.children: List[Node] = []
        self.max_children: int = -1
        self._context: Optional[Context] = None
        self._status: str = NodeStatus.FUTURE
        # 处理类型、处理人id
        self._handler_type: str = HandlerType.STATIC
        self._handler_id: str = ''  # 静态时为指定id，动态时为上下文的字段名，映射时为函数名称
        # 分支条件，下标和子节点对应，不足时不执行
        self._conditions: List[str] = []
        # 存放原始数据
        self.raw_data = raw_data

    @property
    def context(self):
        return self._context

    @context.setter
    def context(self, value: Context):
        self._context = value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value: str):
        self._status = value

    @property
    def handler_type(self):
        return self._handler_type

    @handler_type.setter
    def handler_type(self, value: str):
        self._handler_type = value

    @property
    def handler_id(self):
        return self._handler_id

    @handler_id.setter
    def handler_id(self, value: str):
        self._handler_id = value

    @property
    def conditions(self):
        return self._conditions

    @conditions.setter
    def conditions(self, value: str):
        self._conditions = value

    def __repr__(self):
        return f'<{self.node_type} {self.node_id}.{self.node_name}>'

    def __str__(self):
        return f'{self.node_id}.{self.node_name}'

    def __eq__(self, other):
        return isinstance(other, Node) and self.node_id == other.node_id

    def set_parent(self, node: 'Node'):
        """ 设置父节点 """
        self.parent = node

    def get_children_count(self) -> int:
        """ 获取子节点数量 """
        return len(self.children)

    def is_index_valid(self, index: int) -> bool:
        """ 校验下标合法 """
        return 0 <= index < self.get_children_count()

    def get_child(self, index: int) -> Union['Node', None]:
        """ 获取子节点 """
        if index >= self.get_children_count() or index < 0:
            return None
        return self.children[index]

    def add_child(self, node: 'Node') -> 'Node':
        """ 增加子节点 """
        if 0 <= self.max_children <= self.get_children_count():
            return self
        self.children.append(node)
        return self

    def remove_child(self, node: 'Node') -> 'Node':
        """ 删除子节点 """
        for i in range(self.get_children_count()):
            if node.node_id == self.get_child(i).node_id:
                self.children.pop(i)
                break
        return self

    def to_node_list(self, node_list: List[dict] = None, parent_id: str = '', mapping: dict = None) -> List[dict]:
        """ 转成节点列表 """

        node_list = node_list or []
        mapping = mapping or {}

        id_field_name = mapping.get('node_id') or 'node_id'
        name_field_name = mapping.get('node_name') or 'node_name'
        type_field_name = mapping.get('node_type') or 'node_type'
        sort_field_name = mapping.get('sort') or 'sort'
        parent_field_name = mapping.get('parent_id') or 'parent_id'
        status_field_name = mapping.get('status') or 'status'
        handler_type_field_name = mapping.get('handler_type') or 'handler_type'
        handler_id_field_name = mapping.get('handler_id') or 'handler_id'
        conditions_field_name = mapping.get('conditions') or 'conditions'

        data = self.raw_data
        data.update({
            id_field_name: self.node_id,
            name_field_name: self.node_name,
            type_field_name: self.node_type,
            sort_field_name: len(node_list) + 1,
            parent_field_name: parent_id,
            status_field_name: self.status,
            handler_type_field_name: self.handler_type,
            handler_id_field_name: self.handler_id,
            conditions_field_name: self.conditions,
        })
        node_list.append(data)

        for child in self.children:
            child.to_node_list(node_list=node_list, parent_id=self.node_id, mapping=mapping)

        return node_list

    def tick(self) -> str:
        """ 嘀嗒方法，每帧刷新新数据 """
        running_status = self.on_tick(self.context)
        return running_status

    def on_tick(self, context: Context) -> str:
        """ 嘀嗒执行方法 """
        return self.status

    def pre_condition(self):
        """ 前置条件，满足前置条件才能进入该节点 """
        pass

    def post_condition(self):
        """ 后置条件，满足后置条件该节点才能审批完成 """
        pass

    def pre_script(self):
        """ 前置脚本，开始审批该节点时执行 """
        pass

    def post_script(self):
        """ 后置脚本，审批完成该节点时执行 """


class RootNode(Node):
    """ 根节点 """
    node_type = NodeType.root

    def on_tick(self, context: Context) -> str:
        """ 嘀嗒执行方法 """
        # 逐一遍历每个子节点，当子节点处于完成，才会执行下一个子节点

        # 如果节点状态是已完成，则直接返回已完成
        if self.status == NodeStatus.COMPLETE:
            return self.status

        # 等待状态
        self.status = NodeStatus.WAITING

        # 遍历每个子节点，执行嘀嗒方法
        # 如果嘀嗒方法返回不是完成状态，则直接返回等待状态
        for child in self.children:
            child_status = child.tick()
            if child_status != NodeStatus.COMPLETE:
                return self.status

        # 当所有子节点都是完成状态时，返回完成状态
        self.status = NodeStatus.COMPLETE
        return self.status


class OriginateNode(Node):
    """ 发起节点 """
    node_type = NodeType.originate

    def __init__(self, node_id: str, node_name: str, raw_data: dict):
        super().__init__(node_id, node_name, raw_data)
        self.max_children = 0  # 不允许添加子节点

    def on_tick(self, context: Context) -> str:
        """ 嘀嗒执行方法 """
        # 首先进入准备状态，等待审核事件后进入完成状态

        # 如果节点状态是已完成，则直接返回已完成
        if self.status == NodeStatus.COMPLETE:
            return self.status

        # 准备状态，没有发起人数据时将一直处于这个状态
        self.status = NodeStatus.READY
        handler_id = context.data.get('handler_id')
        if not handler_id:
            return self.status

        # 设置发起人信息，并标记完成状态
        self.handler_type = HandlerType.STATIC
        self.handler_id = handler_id
        self.status = NodeStatus.COMPLETE
        return self.status


class ApprovalNode(Node):
    """ 审批节点 """
    node_type = NodeType.approval

    def __init__(self, node_id: str, node_name: str, raw_data: dict):
        super().__init__(node_id, node_name, raw_data)
        self.max_children = 0  # 不允许添加子节点

    def on_tick(self, context: Context) -> str:
        """ 嘀嗒执行方法 """
        # 首先进入准备状态，等待审核事件后进入完成状态

        # 如果节点状态是已完成，则直接返回已完成
        if self.status == NodeStatus.COMPLETE:
            return self.status

        # 转换处理人信息
        if self.handler_type == HandlerType.FORM:
            self.handler_id = context.data.get(self.handler_id) or self.handler_id

        elif self.handler_type == HandlerType.RELATION:
            originator_id = context.data.get('originator_id') or ''
            command = f'{self.handler_id}("{originator_id}")'
            try:
                handler_id = eval(command, context.data)
                self.handler_id = handler_id or self.handler_id
            except Exception as e:
                logging.info(f'审批节点获取映射处理人出错:{command}:{e}')
        else:
            pass

        # 准备状态，没有发起人数据时将一直处于这个状态
        self.status = NodeStatus.READY
        return self.status


class SerialNode(RootNode):
    """ 串行节点 """
    node_type = NodeType.serial


class JoinNode(Node):
    """ 会签节点 """
    node_type = NodeType.join

    def on_tick(self, context: Context) -> str:
        """ 嘀嗒执行方法 """
        # 首先进入等待状态，等待所有子节点都是完成状态时进入完成状态

        # 进入等待状态
        self.status = NodeStatus.WAITING

        # 同时执行子节点，并检查完成状态
        status_list = []
        for child in self.children:
            child_status = child.tick()
            status_list.append(child_status == NodeStatus.COMPLETE)

        # 所有子节点状态都是完成状态时，返回完成状态
        if all(status_list):
            self.status = NodeStatus.COMPLETE
        return self.status


class ParallelNode(Node):
    """ 并行节点 """
    node_type = NodeType.parallel

    def on_tick(self, context: Context) -> str:
        """ 嘀嗒执行方法 """
        # 首先进入等待状态，等待任一子节点是完成状态时进入完成状态

        # 进入等待状态
        self.status = NodeStatus.WAITING

        # 同时执行子节点，并检查完成状态
        status_list = []
        for child in self.children:
            child_status = child.tick()
            status_list.append(child_status == NodeStatus.COMPLETE)

        # 任一子节点状态是完成状态时，返回完成状态
        if any(status_list):
            self.status = NodeStatus.COMPLETE

        # 如果是完成状态，需要把未完成的子节点设置为跳过状态
        if self.status == NodeStatus.COMPLETE:
            node_list = [self.children[i] for i in range(len(status_list)) if not status_list[i]]
            for node in node_list:
                node.status = NodeStatus.SKIP

        return self.status


class ConditionNode(Node):
    """ 条件节点 """
    node_type = NodeType.condition

    def on_tick(self, context: Context) -> str:
        """ 嘀嗒执行方法 """
        # 首先进入等待状态，等待任一子节点是完成状态时进入完成状态

        # 进入等待状态
        self.status = NodeStatus.WAITING

        # 检查条件长度，如果为0直接完成状态
        condition_length = len(self.conditions)
        if condition_length == 0:
            self.status = NodeStatus.COMPLETE
            return self.status

        # 逐一遍历每个子节点，判断条件指定情况和子节点执行情况
        status_list = [False] * len(self.children)
        for index, child in enumerate(self.children):
            # 没有判断条件的跳过
            if index >= condition_length:
                continue

            # 条件不是字符串，或空字符串的跳过
            condition = self.conditions[index]
            if not isinstance(condition, str) or condition == '':
                continue

            # 条件判断结果为false时跳过
            try:
                condition_status = bool(eval(condition, self.context.data))
                if not condition_status:
                    continue
            except Exception as e:
                logging.info(f'条件节点判断条件时出错:{index}:{condition}:{e}')

            # 执行子节点，检查执行结果是否为完成
            child_status = child.tick()
            status_list[index] = (child_status == NodeStatus.COMPLETE)

        # 任一子节点状态是完成状态时，返回完成状态
        if any(status_list):
            self.status = NodeStatus.COMPLETE

        # 如果是完成状态，需要把未完成的子节点设置为跳过状态
        if self.status == NodeStatus.COMPLETE:
            node_list = [self.children[i] for i in range(len(status_list)) if not status_list[i]]
            for node in node_list:
                node.status = NodeStatus.SKIP

        return self.status


class LoopNode(Node):
    """ 循环节点 """
    node_type = NodeType.loop

    def __init__(self, node_id: str, node_name: str, raw_data: dict):
        super().__init__(node_id, node_name, raw_data)
        self.max_children = 1  # 只允许添加1个子节点
        self.max_loop_count = 1
        self.current_loop_count = 0


class NodeFactory(object):
    """ 节点工厂 """

    # 节点类字典
    node_class_dict = {
        i.node_type: i for i in
        (RootNode, OriginateNode, ApprovalNode, SerialNode, JoinNode, ParallelNode, ConditionNode)
    }

    @classmethod
    def make_node(cls, node_list: List[dict], mapping: dict = None) -> Context:
        """ 制造节点 """

        # 实例化上下文对象
        context = Context()
        if not node_list:
            return context

        mapping = mapping or {}
        id_field_name = mapping.get('node_id') or 'node_id'
        name_field_name = mapping.get('node_name') or 'node_name'
        type_field_name = mapping.get('node_type') or 'node_type'
        sort_field_name = mapping.get('sort') or 'sort'
        parent_field_name = mapping.get('parent_id') or 'parent_id'
        status_field_name = mapping.get('status') or 'status'

        for i in sorted(node_list, key=lambda x: x.get(sort_field_name)):
            node_id = i[id_field_name]
            node_type = i[type_field_name]
            node_class: Type[Node] = cls.node_class_dict.get(node_type)
            if node_class is None:
                raise NodeNotFoundError(f'节点数据无法获取节点类:{id}:{type}')

            # 实例化节点对象
            node = node_class(
                node_id=node_id,
                node_name=i[name_field_name],
                raw_data=i,
            )
            node.status = i.get(status_field_name, NodeStatus.FUTURE)
            node.context = context
            # 加入节点字典中，用于增加子节点
            context.register(node)
            # 如果有父节点id时，把当前节点加入到父节点中
            parent_id = i[parent_field_name]
            if parent_id:
                context.get_node(parent_id).add_child(node)

        return context
