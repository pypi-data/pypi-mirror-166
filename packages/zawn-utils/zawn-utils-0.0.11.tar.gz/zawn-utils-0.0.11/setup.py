#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2022-08-11
# @Author  : wuxiangbin
# @Site    : www.0-9.ink
# @File    : setup.py
# @Software: zawn_utils
# @Function:
from setuptools import setup, find_packages  # 这个包没有的可以pip一下

setup(
    name="zawn-utils",  # 这里是pip项目发布的名称
    version="0.0.11",  # 版本号，数值大的会优先被pip
    keywords=["zawn"],  # 关键字
    description="zawn's private utils.",  # 描述
    long_description="zawn's private utils.",
    license="MIT Licence",  # 许可证

    url="https://github.com/zawn/utils",  # 项目相关文件地址，一般是github项目地址即可
    author="zawn",  # 作者
    author_email="zawn@qq.com",

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=["pymongo", "motor", "pandas", "openpyxl"],  # 这个项目依赖的第三方库
)
