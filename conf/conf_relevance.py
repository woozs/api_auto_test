#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/10/9 22:37
# @Author  : mrwuzs
# @Site    :
# @File    : conf_relevance.py
# @Software: PyCharm


import configparser

from common.log import MyLog as logging
from common.function_replace import function_replace


class ConfRelevance:
    # 关联文件读取配置
    def __init__(self, _path, title):

        logging.info("初始化关联文件")
        config = configparser.ConfigParser()
        config.read(_path, encoding="utf-8")
        self.host = config[title]

    def get_relevance_conf(self):
        relevance = dict()
        logging.debug("读取初始关联文件内容：   %s" % self.host.items())
        for key, value in self.host.items():
            relevance[key] = function_replace(value)
        logging.debug("初始关联内容数据处理后：   %s" % relevance)
        return relevance


if __name__ == "__main__":
    host = ConfRelevance("D:\\4_code\\os_l_test\\conf\\cfg.ini", "test_data")
    print(host.get_relevance_conf())
