#!/usr/bin/env.ini python
# -*- coding: utf-8 -*-
# @Time    : 2019/9/10 20:50
# @Author  : mrwuzs
# @Site    :
# @File    : Token.py
# @Software: PyCharm

import requests
import os

from Common import Log
from Common import ParamManage
from Conf import Config
from Conf import ConfRelevance


BASE_PATH = str(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
CONF_PATH = BASE_PATH + "\\Conf\\cfg.ini"


class Token:
    def __init__(self):
        self.config = Config.Config()
        self.log = Log.MyLog()
        self.relevance = ConfRelevance.ConfRelevance(
            CONF_PATH, "test_data").get_relevance_conf()
        # self.log

    def get_token(self):
        """
        获取token
        :return: token-id
        """
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
            "Content-Type": "application/json"}
        self.log.debug("Headers：%s" % headers)
        login_url = "http://" + self.config.host + ":5000/v3/auth/tokens"
        self.log.debug("login_url：%s" % login_url)
        self.log.debug("处理认证参数")
        param = ParamManage.manage(self.config.loginInfo, self.relevance)
        self.log.debug("param:%s" % param)
        self.log.info("获取token")
        response = requests.post(login_url, param, headers=headers)
        self.log.debug("response：%s"%response)
        token = response.headers.get("X-Subject-Token")
        self.log.info("成功获取token:%s" % token)
        return token

    def save_token(self):
        """
        保存token到配置文件
        :return:
        """
        token = self.get_token()
        self.log.info("保存token_id：%s到配置文件" % token)
        self.config.set_conf("test_data", "token_id", token)


if __name__ == '__main__':
    token = Token()
    print(token.get_token())
    token.save_token()
