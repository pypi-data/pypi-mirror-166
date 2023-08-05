#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2022-08-25
# @Author  : wuxiangbin
# @Site    : www.0-9.ink
# @File    : test.py
# @Software: zawn_utils
# @Function:
import datetime
import json
import unittest

from zawn_orm import field
from zawn_orm import model
from zawn_orm.impl.mongodb import MongoDB

with open('../uri.json', 'rb') as fp:
    config = json.load(fp)

test_json = {
    'id': 1,
    'name': '1',
    'height': 180.5,
    'create_time': '2022-01-01T00:00:00.000+0800',
    'balance': '100.00',
    'enabled': True,
    'object_field': {
        's_id': '11',
        's_name': 11,
        's_height': '181.5',
        's_create_time': '2020-01-01T00:00:00.000+0800',
        's_balance': '200.00',
        's_enabled': 1,
    },
    'array_field': [
        {
            's_id': '11',
            's_name': 11,
            's_height': '181.5',
            's_balance': '200.00',
            's_enabled': 1,
            'b': 123,
        },
        {
            's_id': '110',
            's_name': 110,
            's_height': '185.5',
            's_balance': '250.00',
            's_enabled': 0,
            'b': lambda x: x,
        },
    ],
}


class TestMongoDB(unittest.IsolatedAsyncioTestCase):

    async def init_database(self):
        database = MongoDB()
        await database.connect(config['mongodb_uri'])
        model.Model.set_database(database)

    def init_class(self):
        class EmbeddedModel(model.Model):
            s_name = field.StringField()
            s_id = field.IntegerField()
            s_height = field.FloatField()
            s_create_time = field.DatetimeField()
            s_balance = field.DecimalField()
            s_enabled = field.BooleanField()

        class TestModel(model.Model):
            id = field.IntegerField()
            name = field.StringField()
            height = field.FloatField()
            create_time = field.DatetimeField()
            balance = field.DecimalField()
            enabled = field.BooleanField()
            object_field = field.EmbeddedDictField(EmbeddedModel)
            array_field = field.EmbeddedListField(EmbeddedModel)

        self.EmbeddedModel = EmbeddedModel
        self.TestModel = TestModel

    async def asyncSetUp(self) -> None:
        self.test_json = test_json
        await self.init_database()
        self.init_class()

    async def asyncTearDown(self) -> None:
        pass

    async def test__objects_equal(self):
        self.assertEqual(self.TestModel().table_name, 'test_model')
        self.assertEqual(self.EmbeddedModel().table_name, 'embedded_model')
        self.assertEqual(self.TestModel().table_name, 'test_model')
        self.assertEqual(self.TestModel(), self.TestModel(), '相同模型的objects返回对象应该相同')
        self.assertEqual(self.EmbeddedModel(), self.EmbeddedModel(), '相同模型的objects返回对象应该相同')
        self.assertNotEqual(self.TestModel(), self.EmbeddedModel(), '不同模型的objects返回对象应该不同')

    async def test__transform(self):
        now = datetime.datetime.now().astimezone()
        now_str = now.strftime(field.DatetimeField.datetime_format)
        test_model = self.TestModel()
        test_json = self.test_json
        test_json['create_time'] = now_str

        test_from_json = test_model.from_json(test_json)
        test_to_db = test_model.to_db(test_from_json)
        test_from_db = test_model.from_db(test_to_db)
        test_to_json = test_model.to_json(test_from_db)

        self.assertEqual(test_from_json['create_time'], now)
        self.assertEqual(test_to_db['create_time'], now)
        self.assertEqual(test_from_db['create_time'], now)
        self.assertEqual(test_to_json['create_time'], now_str)

    async def test__write_and_read(self):
        now = datetime.datetime.now().astimezone()
        now_str = now.strftime(field.DatetimeField.datetime_format)
        id_1 = int(now.timestamp())
        id_2 = id_1 + 1
        test_model = self.TestModel()
        test_json = self.test_json
        test_json['create_time'] = now_str
        test_json['id'] = id_1
        test_json_2 = test_json.copy()
        test_json_2['id'] = id_2

        test_from_json = test_model.from_json(test_json)
        test_to_db = test_model.to_db(test_from_json)
        test_from_json_2 = test_model.from_json(test_json_2)
        test_to_db_2 = test_model.to_db(test_from_json_2)
        operation_list = [
            test_model.new_operation('delete', {}, {}),
            test_model.new_operation('insert', {}, test_to_db),
            test_model.new_operation('update', {'id': id_1}, {'$inc': {'balance': 100}}),
            test_model.new_operation('insert', {}, test_to_db_2),
            test_model.new_operation('delete', {'id': id_2}, {}),
        ]
        result = await test_model.execute(operation_list)

        query = test_model.new_query({'$project': {'_id': 0, 'create_time': 1}})
        meta, data = await test_model.search(query)
        test_from_db = [test_model.from_db(i) for i in data]
        test_to_json = [test_model.to_json(i) for i in test_from_db]

        self.assertEqual(result[test_model.table_name]['nInserted'], 2)
        self.assertGreaterEqual(result[test_model.table_name]['nRemoved'], 0)
        self.assertGreater(meta['total'], 0)
        self.assertTrue(test_to_json[0]['create_time'].startswith('2022-08'))
        self.assertIsNone(test_to_json[0].get('id'))


if __name__ == '__main__':
    unittest.main()
