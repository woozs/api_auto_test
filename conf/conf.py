#!/usr/bin/env.ini python
# -*- coding: utf-8 -*-
# @Time    : 2019/9/9 16:35
# @Author  : mrwuzs
# @Site    : 
# @File    : conf.py
# @Software: PyCharm

from configparser import ConfigParser
from common import log
import os


class Config:
    # titles:
    TITLE_ENV = "env"
    TITLE_EMAIL = "email"
    TITLE_TEST_DATA = "test_data"


    # values:
    # [env.ini]
    VALUE_TESTER = "tester"
    VALUE_ENVIRONMENT = "environment"
    VALUE_VERSION_CODE = "versionCode"
    VALUE_HOST = "host"
    VALUE_LOGIN_INFO = "loginInfo"
    # [mail]
    VALUE_SEND = "send"
    VALUE_SMTP_SERVER = "smtpserver"
    VALUE_SENDER = "sender"
    VALUE_RECEIVER = "receiver"
    VALUE_USERNAME = "username"
    VALUE_PASSWORD = "psw"
    #[test_data]
    VALUE_TOKEN = "token_id"

    # path
    path_dir = str(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

    def __init__(self):
        """
        初始化
        """
        self.config = ConfigParser()
        self.log = log.MyLog()
        self.conf_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cfg.ini')
        self.xml_report_path = Config.path_dir+'/report/xml'
        self.html_report_path = Config.path_dir+'/report/html'

        if not os.path.exists(self.conf_path):
            raise FileNotFoundError("请确保配置文件存在！")

        self.config.read(self.conf_path, encoding='utf-8')

        self.tester = self.get_conf(Config.TITLE_ENV, Config.VALUE_TESTER)
        self.environment = self.get_conf(Config.TITLE_ENV, Config.VALUE_ENVIRONMENT)
        self.versionCode = self.get_conf(Config.TITLE_ENV, Config.VALUE_VERSION_CODE)
        self.host = self.get_conf(Config.TITLE_ENV, Config.VALUE_HOST)
        self.loginInfo = self.get_conf(Config.TITLE_ENV, Config.VALUE_LOGIN_INFO)

        self.smtpserver = self.get_conf(Config.TITLE_EMAIL, Config.VALUE_SMTP_SERVER)
        self.sender = self.get_conf(Config.TITLE_EMAIL, Config.VALUE_SENDER)
        self.receiver = self.get_conf(Config.TITLE_EMAIL, Config.VALUE_RECEIVER)
        self.username = self.get_conf(Config.TITLE_EMAIL, Config.VALUE_USERNAME)
        self.password = self.get_conf(Config.TITLE_EMAIL, Config.VALUE_PASSWORD)
        self.send = self.get_conf(Config.TITLE_EMAIL, Config.VALUE_SEND)
        self.token =  self.get_conf(Config.TITLE_TEST_DATA,Config.VALUE_TOKEN)

    def get_conf(self, title, value):
        """
        配置文件读取
        :param title:
        :param value:
        :return:
        """
        return self.config.get(title, value)

    def set_conf(self, title, value, text):
        """
        配置文件修改
        :param title:
        :param value:
        :param text:
        :return:
        """
        self.config.set(title, value, text)
        with open(self.conf_path, "w+") as f:
            return self.config.write(f)

    def add_conf(self, title):
        """
        配置文件添加
        :param title:
        :return:
        """
        self.config.add_section(title)
        with open(self.conf_path, "w+") as f:
            return self.config.write(f)


if __name__ == "__main__":
    cnf = Config()
    cnf.set_conf("test_data","project_id","23456787654321")