#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2022-07-17
# @Author  : wuxiangbin
# @Site    : www.0-9.ink
# @File    : token_helper.py
# @Software: property
# @Function: token模块
import base64
import hashlib
import json
import time
from typing import Tuple


class TokenHelper(object):
    """ token助手 """

    _ENCODING = 'utf-8'
    _PRIVATE_KEY = 'zawn@qq.com'.encode(_ENCODING)
    _KEY = None
    _EXP_OFFSET = 86400  # 过期偏移量，秒

    @classmethod
    def set_key(cls, key: str) -> None:
        """ 设置加密密钥 """
        cls._KEY = key.encode(cls._ENCODING)

    @classmethod
    def get_sign_string(cls, data: dict) -> str:
        """ 获取哈希字符串，返回大写签名字符串 """

        # 实例化哈希对象
        hash = hashlib.sha3_256()
        hash.update(cls._KEY)

        # 对字典对key进行排序处理
        keys = sorted([i for i in data.keys() if isinstance(i, str)])

        # 把所有key和value加入哈希算法进行处理
        for index, key in enumerate(keys):
            hash.update(key.encode(cls._ENCODING))
            value = data[key]
            if not isinstance(value, str):
                value = str(value)
            hash.update(value.encode(cls._ENCODING))
            hash.update(cls._PRIVATE_KEY)
            hash.update(cls._KEY)
            hash.update(f'{index % 3}'.encode(cls._ENCODING))

        # 返回大写签名字符串
        return hash.hexdigest().upper()

    @classmethod
    def sign(cls, data: dict) -> str:
        """ 对数据进行签名，返回令牌 """

        data = data.copy()
        # 令牌过期时间，如果没有传入值，则以当前时间+偏移量
        data['exp'] = isinstance(data.get('exp'), int) and abs(data.get('exp')) or int(time.time() + cls._EXP_OFFSET)
        # 获取签名字符串，加入数据sign字段
        data['sign'] = cls.get_sign_string(data)
        # 输出json字符串
        token = json.dumps(data, allow_nan=False, separators=(',', ':'), sort_keys=True)
        return base64.b64encode(token.encode(cls._ENCODING)).decode(cls._ENCODING)

    @classmethod
    def decode(cls, token: str) -> dict:
        """ 解码令牌 """

        token = base64.b64decode(token.encode(cls._ENCODING) + b'===')
        return json.loads(token)

    @classmethod
    def validate(cls, token: str) -> Tuple[bool, str, dict]:
        """ 校验令牌 """

        data = cls.decode(token)

        # 获取过期时间
        if not isinstance(data.get('exp'), int):
            return False, '过期时间解析失败[exp]', data

        # 检查过期时间
        if data['exp'] < int(time.time()):
            return False, '令牌已过期[exp]', data

        # 获取签名字段
        if not data.get('sign'):
            return False, '缺少签名字段[sign]', data

        # 校验签名
        sign = data.pop('sign')
        _sign = cls.get_sign_string(data)
        if sign != _sign:
            return False, '签名不一致[sign]', data

        return True, '签名校验成功', data


if __name__ == '__main__':
    key = 'baserver'
    TokenHelper.set_key(key)
    data = {'user_id': 'my_user_id'}
    print(data)
    token = TokenHelper.sign(data)
    print(token)
    data = TokenHelper.validate(token)
    print(data)
