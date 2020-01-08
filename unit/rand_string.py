#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/9/26 8:54
# @Author  : mrwuzs
# @Site    : 
# @File    : rand_string.py
# @Software: PyCharm
import random
import string

def random_string(num_length):
    """
    从a-zA-Z0-9生成指定数量的随机字符
    :param num_length: 字符串长度
    :return:
    """
    try:
        num_length = int(num_length)
    except ValueError:
        raise AssertionError("从a-zA-Z0-9生成指定数量的随机字符失败！长度参数有误  %s" % num_length)
    num = ''.join(random.sample(string.ascii_letters + string.digits, num_length))
    return num


if __name__ == "__main__":
    print(random_string(5))
