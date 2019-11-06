#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/10/29 16:45
# @Author  : mrwuzs
# @Site    : 
# @File    : Ports.py
# @Software: PyCharm

import os

from Common import Log
from Common import ConfigHttp
from Conf import Config
from Conf import ConfRelevance


BASE_PATH = str(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
CONF_PATH = BASE_PATH + "\\Conf\\cfg.ini"


class Ports:
    def __init__(self):
        self.config = Config.Config()
        self.log = Log.MyLog()
        self.data = ConfRelevance.ConfRelevance(
            CONF_PATH, "test_data").get_relevance_conf()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
            "Content-Type": "application/json",
            "X-Auth-Token": self.config.token}

        # self.log

    def get_ports(self):
        """
        获取token
        :return: token-id
        """

        self.log.debug("Headers：%s" % self.headers)
        url = "http://" + self.config.host + ":9696/v2.0/ports?network_id=%s"%self.data["network_id"]
        results = ConfigHttp.get(self.headers, url, data=None)
        return results



    def delete_all_port(self):
        """
        删除所有的port
        :return:
        """
        code, data = self.get_ports()
        for i in data["ports"]:
            url = "http://" + self.config.host + ":9696/v2.0/ports/%s"%i["id"]
            self.log.debug("删除port：%s," % i["id"])
            code,responce = ConfigHttp.delete(self.headers, url, data=None)
            self.log.debug("请求返回为：%s,%s"%(code,responce))

if __name__ == '__main__':
    Ports().delete_all_port()


