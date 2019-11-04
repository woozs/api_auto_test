#!/usr/bin/env.ini python
# -*- coding: utf-8 -*-
# @Time    : 2019/9/11 15:34
# @Author  : mrwuzs
# @Site    : 
# @File    : Shell.py
# @Software: PyCharm

"""
封装执行shell语句方法

"""

import subprocess


class Shell:
    @staticmethod
    def invoke(cmd):
        output, errors = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        o = output.decode("utf-8")
        return o
