#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/10/18 17:22
# @Author  : mrwuzs
# @Site    :
# @File    : add_Role_admin.py
# @Software: PyCharm
import requests
import os
import allure

from Common import Log
from Common import ParamManage
from Conf import Config
from Conf import ConfRelevance


BASE_PATH = str(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
CONF_PATH = BASE_PATH + "\\Conf\\cfg.ini"


class Project_Add_Rule:
    """给项目添加admin权限"""

    def __init__(self):
        self.config = Config.Config()
        self.log = Log.MyLog()
        self.relevance = ConfRelevance.ConfRelevance(
            CONF_PATH, "test_data").get_relevance_conf()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
            "Content-Type": "application/json",
            "X-Auth-Token": "${token_id}$"}

        self.address = {
            "address": "/v3/projects/${project_id}$/users/${admin_id}$/roles/${admin_role_id}$"}

    def project_add_role(self):
        """
        给项目添加权限
        :return:
        """
        self.log.debug("处理header")
        headers = ParamManage.manage(self.headers, self.relevance)
        self.log.debug("Headers：%s" % headers)
        self.log.debug("处理address")
        address = ParamManage.manage(self.address, self.relevance)
        self.log.debug("address:%s" % address)
        login_url = "http://" + self.config.host + ":5000" + address["address"]
        self.log.debug("login_url：%s" % login_url)
        self.log.info("给项目添加admin权限")
        with allure.step("给项目添加权限"):
            allure.attach("address:%s" % address["address"])
        response = requests.put(login_url, headers=headers)
        if response.status_code == 204:
            self.log.info("项目成功添加admin权限")
            return
        else:
            raise Exception("项目添加admin权限失败，请确认参数")


if __name__ == '__main__':
    add_role_test = Project_Add_Rule()
    add_role_test.project_add_role()
