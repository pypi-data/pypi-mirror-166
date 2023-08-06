#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2022-09-01
# @Author  : wuxiangbin
# @Site    : www.0-9.ink
# @File    : search_helper.py
# @Software: zawn_utils
# @Function:
import re
from datetime import timedelta, datetime
from typing import List


class SearchHelper(object):
    """ 搜索助手类 """

    key_regex = re.compile('^[0-9a-zA-Z_]+$')
    default_skip: int = 0
    default_limit: int = 10

    @classmethod
    def match(cls, conditions: List[dict]):
        query = [{'$match': {'$and': conditions}}]
        return query

    @classmethod
    def sort_desc_by_create_time(cls):
        query = [{'$sort': {'create_at': -1, '_id': -1}}]
        return query

    @classmethod
    def skip_limit(cls, skip: int = default_skip, limit: int = default_limit):
        query = []
        if skip > 0:
            query.append({'$skip': skip})
        if limit > 0:
            query.append({'$limit': limit})
        return query

    @classmethod
    def unwind(cls, path: str, preserve: bool = True):
        query = [{'$unwind': {'path': path, 'preserveNullAndEmptyArrays': preserve}}]
        return query

    @classmethod
    def join(
            cls, from_collection: str, local_field: str, foreign_field: str,
            as_name: str, unwind_path: str = None, set_fields: dict = None,
            preserve: bool = True):
        query = [
            {'$lookup': {
                'from': from_collection,
                'localField': local_field,
                'foreignField': foreign_field,
                'as': as_name,
            }},
        ]
        # 这里改为最后参数unwind_path不是None时，才增加$unwind语句
        if unwind_path is not None:
            query.extend(cls.unwind(unwind_path, preserve))
        if set_fields:
            query.extend([
                {'$set': {
                    i: f'${as_name}.{set_fields[i]}' for i in set_fields
                }},
                {'$unset': [as_name]},
            ])
        return query

    @classmethod
    def group_by(cls, fields: [dict, str], count: dict):
        ''' 分组统计 '''

        query = []
        group_query = {'$group': {
            '_id': fields,
            'root': {'$mergeObjects': '$$ROOT'},
        }}
        group_query['$group'].update(count)
        query.append(group_query)

        if len(count) != 0:
            query.append({'$set': {f'root.{i}': f'${i}' for i in count}})
        query.append({'$replaceRoot': {'newRoot': '$root'}})

        return query

    @classmethod
    def join2(cls, from_collection, join_fields, set_fields):
        ''' 联表查询语句，多字段联表
        set_fields={原表字段名: 关联表字段名}

        *QueryUtils.join2(
            'aid_train_result',
            {'train_code': 'train_code', 'aid_user_code': 'aid_user_code'},
            {
                'theory_result': 'theory_result',
                'trial_result': 'trial_result',
                'recovery_result': 'recovery_result',
                'rescue_result': 'rescue_result',
                'attendance': 'attendance',
            },
        ),
        '''

        let_fields = {}
        conditions = []
        for k in join_fields:
            let_fields[k] = f'${k}'
            conditions.append({'$eq': [f'${join_fields[k]}', f'$${k}']})
        conditions.append({'$ne': ['$status', '-1']})

        for k in set_fields:
            set_fields[k] = {'$first': f'${from_collection}.{set_fields[k]}'}

        pipeline = [
            {'$lookup': {
                'from': from_collection,
                'let': let_fields,
                'pipeline': [
                    {'$match': {'$expr': {'$and': conditions}}},
                ],
                'as': from_collection,
            }},
            {'$set': set_fields},
            {'$unset': [from_collection]},
        ]

        return pipeline

    @classmethod
    def range_query(
            cls, key: str, value: [list, str],
            query_type: str, offset_time: timedelta = timedelta()):
        ''' 生成返回搜索条件
        搜索类型 query_type:[date,datetime,number,code]
        '''
        query = []
        if query_type == 'date':
            date_format = '%Y-%m-%d'
            one_day = timedelta(days=1)
            if isinstance(value, list) and len(value) == 2:
                start = datetime.strptime(value[0], date_format) + offset_time
                end = datetime.strptime(value[1], date_format) + offset_time + one_day
                query.append({key: {'$gte': start, '$lt': end}})
            elif isinstance(value, str):
                dt = datetime.strptime(value, date_format) + offset_time
                query.append({key: {'$gte': dt, '$lt': dt + one_day}})
            else:
                raise Exception(f'时间搜索条件 {key}:[start,end]')

        elif query_type == 'datetime':
            datetime_format = '%Y-%m-%dT%H:%M:%S.%fZ'
            if isinstance(value, list) and len(value) == 2:
                start = datetime.strptime(value[0], datetime_format)
                end = datetime.strptime(value[1], datetime_format)
                query.append({key: {'$gte': start, '$lt': end}})
            elif isinstance(value, str):
                query.append({key: datetime.strptime(value, datetime_format)})
            else:
                raise Exception(f'时间搜索条件 {key}:[start,end]')

        elif query_type == 'number':
            if isinstance(value, list) and len(value) == 2:
                query.append({key: {'$gte': value[0], '$lte': value[1]}})
            elif isinstance(value, (int, float)):
                query.append({key: value})
            elif isinstance(value, str):
                query.append({key: float(value)})
            else:
                raise Exception(f'数字搜索条件 {key}:[start,end]')

        elif query_type == 'code':
            if isinstance(value, list):
                query.append({key: {'$in': value}})
            elif isinstance(value, str):
                query.append({key: value})
            else:
                raise Exception(f'数字搜索条件 {key}:[code1,code2,...]')

        elif query_type == 'status':
            if isinstance(value, list):
                query.append({key: {'$in': value}})
            elif isinstance(value, str):
                query.append({key: value})
            else:
                query.append({key: {'$ne': '-1'}})

        else:
            raise Exception('必传query_type:[date,datetime,number,code]')

        return query
