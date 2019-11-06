#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/10/18 11:32
# @Author  : mrwuzs
# @Site    : 
# @File    : test_04_server.py
# @Software: PyCharm

import os,time
import allure,pytest
from Conf.Config import Config
from Conf import  ConfRelevance
from unit import LoadYaml, Token
from Common import RequestSend,Log,CheckResult,Assert

BASE_PATH = str(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
CASE_PATH = BASE_PATH + "\\Params\\Param\\server"
CONF_PATH = BASE_PATH + "\\Conf\\cfg.ini"
case_dict = LoadYaml.load_case(CASE_PATH + "\\create_server.yaml")

@allure.feature(case_dict["testinfo"]["title"])  # feature定义功能
class Test_Server:
    @classmethod
    def setup_class(cls):
        #初始化用例参数，将全局变量替换成配置文件中得变量
        cls.result = {"result": True}
        #更新配置文件中的token
        cls.token = Token.Token()
        cls.token.save_token()
        cls.log = Log.MyLog()
        cls.Assert =  Assert.Assertions()
        #

    def setup(self):
        self.relevance =  ConfRelevance.ConfRelevance(CONF_PATH,"test_data").get_relevance_conf()


    @pytest.mark.parametrize("case_data", case_dict["test_case"])
    @allure.story("创建和查询虚拟机")
    @pytest.mark.flaky(reruns=3)
    def test_server(self,case_data):
        for k, v in enumerate(case_dict["test_case"]):  # 遍历用例文件中所有用例的索引和值
            try:
                if case_data == v:
                    # 修改方法的__doc__在下一次调用时生效，此为展示在报告中的用例描述
                    Test_Server.test_server.__doc__ = case_dict["test_case"][k + 1]["info"]
            except IndexError:
                pass

        if not self.result["result"]:
            # 查看类变量result的值，如果未False，则前一接口校验错误，此接口标记未失败，节约测试时间
            pytest.xfail("前置接口测试失败，此接口标记为失败")

        code, data = RequestSend.send_request(case_data, case_dict["testinfo"].get("host"),
                                              case_dict["testinfo"].get("address"), str(case_dict["testinfo"].get("port")), self.relevance, CASE_PATH, self.result)
        expected_code = case_data["check"][0]["expected_code"]
        server_id = data["server"]["id"]
        self.Assert.assert_code(code,expected_code)

        if case_data["request_type"] == "post":
            self.log.info("保存server_id到全局配置文件")
            conf =Config()
            conf.set_conf("test_data","server_id",server_id)
        if case_data["sleep_time"] :
            self.log.info("虚拟机已创建，等待创建........")
            time.sleep(case_data["sleep_time"])

        CheckResult.check(case_data["test_name"], case_data["check"][0], code, data, self.relevance, CASE_PATH,
                          self.result)

if __name__ == "__main__":
    pytest.main(["-s", "test_04_server.py"])
