#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2022-09-02
# @Author  : wuxiangbin
# @Site    : www.0-9.ink
# @File    : exception.py
# @Software: zawn_utils
# @Function:


class ModelNotFoundError(Exception):
    """ 模型未找到错误 """
    pass


class NodeNotFoundError(Exception):
    """ 节点未找到错误 """
    pass


class NodeTickError(Exception):
    """ 节点嘀嗒执行错误 """
    pass
