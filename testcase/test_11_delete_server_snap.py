#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/10/29 9:56
# @Author  : mrwuzs
# @Site    : 
# @File    : test_11_delete_server_snap.py
# @Software: PyCharm
import allure
import pytest
import os
import time

from Conf.Config import Config
from Common import Assert
from unit import load_yaml, Token
from Common import requestSend
from Conf import  ConfRelevance
from Common import Log
from Common import CheckResult

BASE_PATH = str(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
CASE_PATH = BASE_PATH + "\\Params\\Param\\server_snapshot"
CONF_PATH = BASE_PATH + "\\Conf\\cfg.ini"
case_dict = load_yaml.load_case(CASE_PATH+"\\delete_server_snap.yaml")

@allure.feature(case_dict["testinfo"]["title"])  # feature定义功能
class Test_Server_Snap:
    @classmethod
    def setup_class(cls):
        #初始化用例参数，将全局变量替换成配置文件中得变量
        cls.result = {"result": True}
        #更新配置文件中的token
        cls.token = Token.Token()
        cls.token.save_token()
        cls.log = Log.MyLog()
        cls.Assert =  Assert.Assertions()

    def setup(self):
        self.relevance =  ConfRelevance.ConfRelevance(CONF_PATH,"test_data").get_relevance_conf()

    @pytest.mark.parametrize("case_data", case_dict["test_case"])
    @allure.story("删除虚拟机快照")
    @pytest.mark.flaky(reruns=3)
    def test_server_snap(self,case_data):
        for k, v in enumerate(case_dict["test_case"]):  # 遍历用例文件中所有用例的索引和值
            try:
                if case_data == v:
                    # 修改方法的__doc__在下一次调用时生效，此为展示在报告中的用例描述
                    Test_Server_Snap.test_server_snap.__doc__ = case_dict["test_case"][k + 1]["info"]
            except IndexError:
                pass
        if not self.result["result"]:
            # 查看类变量result的值，如果未False，则前一接口校验错误，此接口标记未失败，节约测试时间
            pytest.xfail("前置接口测试失败，此接口标记为失败")
        if case_data["request_type"] == "get":
            time.sleep(case_data["sleep_time"])

        code, data = requestSend.send_request(case_data, case_dict["testinfo"].get("host"),
                                              case_dict["testinfo"].get("address"),
                                              str(case_dict["testinfo"].get("port")),
                                              self.relevance, CASE_PATH, self.result)
        CheckResult.check(case_data["test_name"], case_data["check"][0], code, data, self.relevance, CASE_PATH,
                          self.result)

if __name__ == "__main__":
    pytest.main(["-s", "test_11_delete_server_snap.py"])