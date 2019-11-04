#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/9/26 8:50
# @Author  : mrwuzs
# @Site    : 
# @File    : ChoiceData.py
# @Software: PyCharm

import random


def choice_data(data):
    """
    获取随机整型数据
    :param data:
    :return:
    """
    _list = data.split(",")
    num = random.choice(_list)
    return num


if __name__ == "__main__":
    print(choice_data("200, 100, 5"))
