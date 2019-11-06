#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/9/25 11:20
# @Author  : mrwuzs
# @Site    : 
# @File    : LoadYaml.py
# @Software: PyCharm

import os
import yaml
import re



import yaml


def load_case(file):
    """
    case初始化步骤
    :param _path:  case路径
    :return:
    """
    with open(file, 'r', encoding="utf-8") as load_f:
        project_dict = yaml.load(load_f, Loader=yaml.FullLoader)
    return project_dict


if __name__ == "__main__":
    print(load_case(r'D:\4_code\os_l_test\Params\Param\Project.yaml'))