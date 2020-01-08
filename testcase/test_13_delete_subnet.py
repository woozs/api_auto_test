#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/10/29 9:57
# @Author  : mrwuzs
# @Site    :
# @File    : test_13_delete_subnet.py
# @Software: PyCharm


import allure
import pytest
import os
import time


from common import assert_pro
from unit import LoadYaml, Token, Ports
from common import request_send
from conf import conf_relevance
from common import log
from common import check_result


BASE_PATH = str(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
CASE_PATH = BASE_PATH + "\\params\\param\\subnet"
CONF_PATH = BASE_PATH + "\\conf\\cfg.ini"
case_dict = LoadYaml.load_case(CASE_PATH + "\\delete_subnet.yaml")


@allure.feature(case_dict["testinfo"]["title"])  # feature定义功能
class Test_Delete_Subnet:

    @classmethod
    def setup_class(cls):
        # 初始化用例参数，将全局变量替换成配置文件中得变量
        # cls.rel = ini_rel
        cls.result = {"result": True}
        # 更新配置文件中的token
        cls.token = Token.Token()
        cls.token.save_token()
        cls.log = log.MyLog()
        cls.Assert = assert_pro.Assertions()

    def setup(self):
        self.relevance = conf_relevance.ConfRelevance(
            CONF_PATH, "test_data").get_relevance_conf()

        # self.relevance = init.ini_request(case_dict, self.relevance, PATH, self.result)

    @pytest.mark.parametrize("case_data", case_dict["test_case"])
    @allure.story("删除子网")
    # @pytest.mark.scenarios_3(1)
    def test_delete_subnet(self, case_data):

        if case_data["request_type"] == "delete":
            Ports.Ports().delete_all_port()

        # 参数化修改test_add_project 注释
        for k, v in enumerate(case_dict["test_case"]):  # 遍历用例文件中所有用例的索引和值
            try:
                if case_data == v:
                    # 修改方法的__doc__在下一次调用时生效，此为展示在报告中的用例描述
                    Test_Delete_Subnet.test_delete_subnet.__doc__ = case_dict[
                        "test_case"][k + 1]["info"]
            except IndexError:
                pass

        if not self.result["result"]:
            # 查看类变量result的值，如果未False，则前一接口校验错误，此接口标记未失败，节约测试时间
            pytest.xfail("前置接口测试失败，此接口标记为失败")

        time.sleep(case_data["sleep_time"])

        #send_request(_data, _host, _address,_port, _relevance, path, _success)
        code, data = request_send.send_request(
            case_data, case_dict["testinfo"].get("host"), case_dict["testinfo"].get("address"), str(
                case_dict["testinfo"].get("port")), self.relevance, CASE_PATH, self.result)

        check_result.check(
            case_data["test_name"],
            case_data["check"][0],
            code,
            data,
            self.relevance,
            CASE_PATH,
            self.result)


if __name__ == "__main__":
    pytest.main(["-s", "test_13_delete_subnet.py"])
