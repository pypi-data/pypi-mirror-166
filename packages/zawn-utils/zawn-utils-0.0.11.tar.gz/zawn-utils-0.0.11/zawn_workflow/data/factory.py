#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2022-08-21
# @Author  : wuxiangbin
# @Site    : www.0-9.ink
# @File    : factory.py
# @Software: zawn_utils
# @Function:
from zawn_orm import field, model
from zawn_orm.state import BaseState


class State(BaseState):
    SUBMIT: str = 'S1'
    DELETE: str = 'S2'


class WorkUser(model.Model):
    """ 工作用户 """

    user_id = field.StringField()
    user_name = field.StringField()

    org_id = field.StringField()  # 所属机构id
    status = field.StringField()  # 状态
    create_at = field.DatetimeField()  # 创建时间
    create_by = field.StringField()  # 创建人
    update_at = field.DatetimeField()  # 更新时间
    update_by = field.StringField()  # 更新人

    state = State()  # 有限状态机


class WorkGroup(model.Model):
    """ 工作用户组 """

    group_type = field.StringField()
    group_name = field.StringField()
    user_id = field.StringField()
    target_id = field.StringField()

    org_id = field.StringField()  # 所属机构id
    status = field.StringField()  # 状态
    create_at = field.DatetimeField()  # 创建时间
    create_by = field.StringField()  # 创建人
    update_at = field.DatetimeField()  # 更新时间
    update_by = field.StringField()  # 更新人

    state = State()  # 有限状态机


class WorkForm(model.Model):
    """ 工作表单 """

    form_id = field.StringField()  # 表单id
    form_label = field.StringField()  # 表单标签，每个独立表单都有一样的标签
    form_name = field.StringField()  # 表单字段名
    form_type = field.StringField()  # 表单类型
    placeholder = field.StringField()  # 占位符
    disabled = field.BooleanField()  # 是否禁用
    required = field.BooleanField()  # 是否必填

    org_id = field.StringField()  # 所属机构id
    status = field.StringField()  # 状态
    create_at = field.DatetimeField()  # 创建时间
    create_by = field.StringField()  # 创建人
    update_at = field.DatetimeField()  # 更新时间
    update_by = field.StringField()  # 更新人

    state = State()  # 有限状态机


class WorkModel(model.Model):
    """ 工作模型 """

    model_id = field.StringField()  # 模型id
    model_key = field.StringField()  # 模型key
    model_name = field.StringField()  # 模型名称
    model_type = field.StringField()  # 模型分类类型
    version = field.IntegerField()  # 模型版本号，模型key重复时+1

    org_id = field.StringField()  # 所属机构id
    status = field.StringField()  # 状态
    create_at = field.DatetimeField()  # 创建时间
    create_by = field.StringField()  # 创建人
    update_at = field.DatetimeField()  # 更新时间
    update_by = field.StringField()  # 更新人


class WorkNode(model.Model):
    """ 工作节点 """

    node_id = field.StringField()  # 节点id
    parent_id = field.StringField()  # 父节点id
    node_name = field.StringField()  # 节点名称
    node_type = field.StringField()  # 节点类型
    sort = field.StringField()  # 排序序号
    handler_type = field.StringField()  # 处理人类型，不指定、指定、表单、关联、用户组
    handler_id = field.StringField()  # 处理人id

    form_label = field.StringField()  # 表单标签
    model_id = field.StringField()  # 模型id

    org_id = field.StringField()  # 所属机构id
    status = field.StringField()  # 状态
    create_at = field.DatetimeField()  # 创建时间
    create_by = field.StringField()  # 创建人
    update_at = field.DatetimeField()  # 更新时间
    update_by = field.StringField()  # 更新人

    state = State()  # 有限状态机


class WorkInstance(model.Model):
    """ 工作实例 """

    instance_id = field.StringField()  # 实例id
    instance_name = field.StringField()  # 实例名称，以发起人姓名+模型名称为名
    step = field.IntegerField()  # 当前步进数
    completion_rate = field.IntegerField()  # 完成率 0-100区间

    model_id = field.StringField()  # 所属模型id

    org_id = field.StringField()  # 所属机构id
    status = field.StringField()  # 状态
    create_at = field.DatetimeField()  # 创建时间
    create_by = field.StringField()  # 创建人
    update_at = field.DatetimeField()  # 更新时间
    update_by = field.StringField()  # 更新人

    state = State()  # 有限状态机


class WorkTask(model.Model):
    """ 工作任务 """

    task_id = field.StringField()  # 任务id
    parent_id = field.StringField()  # 父任务id
    task_name = field.StringField()  # 任务名称
    task_type = field.StringField()  # 任务类型
    sort = field.StringField()  # 排序序号
    handler_type = field.StringField()  # 处理人类型，不指定、指定、表单、关联、用户组
    handler_id = field.StringField()  # 处理人id

    instance_id = field.StringField()  # 所属实例id

    org_id = field.StringField()  # 所属机构id
    status = field.StringField()  # 状态
    create_at = field.DatetimeField()  # 创建时间
    create_by = field.StringField()  # 创建人
    update_at = field.DatetimeField()  # 更新时间
    update_by = field.StringField()  # 更新人

    state = State()  # 有限状态机


class WorkRecord(model.Model):
    """ 工作记录 """

    record_id = field.StringField()  # 记录id
    handler_id = field.StringField()  # 用户id
    event = field.StringField()  # 事件，同意、驳回
    comment = field.IntegerField()  # 评论
    step = field.IntegerField()  # 步进数

    task_id = field.StringField()  # 所属任务id
    instance_id = field.StringField()  # 所属实例id

    org_id = field.StringField()  # 所属机构id
    status = field.StringField()  # 状态
    create_at = field.DatetimeField()  # 创建时间
    create_by = field.StringField()  # 创建人
    update_at = field.DatetimeField()  # 更新时间
    update_by = field.StringField()  # 更新人

    state = State()  # 有限状态机


class WorkStore(model.Model):
    """ 工作贮存 """

    store_id = field.StringField()  # 贮存id
    label = field.StringField()  # 表单展示标题
    name = field.StringField()  # 表单字段名称
    type = field.StringField()  # 表单类型 包含基本类型和自定义类型
    value = field.StringField()  # 表单值 统一序列化为字符串

    record_id = field.StringField()  # 所属记录id
    task_id = field.StringField()  # 所属任务id
    instance_id = field.StringField()  # 所属实例id

    org_id = field.StringField()  # 所属机构id
    status = field.StringField()  # 状态
    create_at = field.DatetimeField()  # 创建时间
    create_by = field.StringField()  # 创建人
    update_at = field.DatetimeField()  # 更新时间
    update_by = field.StringField()  # 更新人

    state = State()  # 有限状态机


class DataFactory(object):
    """ 数据工厂 """

    work_user: model.Model = None
    work_group: model.Model = None
    work_model: model.Model = None
    work_node: model.Model = None
    work_form: model.Model = None
    work_instance: model.Model = None
    work_task: model.Model = None
    work_value: model.Model = None
    work_record: model.Model = None

    _this = None
    _instance: 'DataFactory' = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            instance = super().__new__(cls, *args, **kwargs)
            instance.work_user = WorkUser()
            instance.work_group = WorkGroup()
            instance.work_model = WorkModel()
            instance.work_node = WorkNode()
            instance.work_form = WorkForm()
            instance.work_instance = WorkInstance()
            instance.work_task = WorkTask()
            instance.work_record = WorkRecord()
            instance.work_store = WorkStore()
            cls._instance = instance
        return cls._instance


if __name__ == '__main__':
    data_factory = DataFactory()
    print(id(data_factory))
    data_factory = DataFactory()
    print(id(data_factory))
