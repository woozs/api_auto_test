#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/10/19 17:46
# @Author  : mrwuzs
# @Site    :
# @File    : test_06_os_volume_attachments.py
# @Software: PyCharm

import allure
import pytest
import os
import time

from common import assert_pro
from unit import load_yaml, token
from common import request_send
from conf import conf_relevance
from common import log
from common import check_result


BASE_PATH = str(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
CASE_PATH = BASE_PATH + "\\params\\param\\os_volume_attach_detach"
CONF_PATH = BASE_PATH + "\\conf\\cfg.ini"
case_dict = load_yaml.load_case(CASE_PATH + "\\os_volume_attac_and_detach.yaml")


@allure.feature(case_dict["testinfo"]["title"])  # feature定义功能
class Test_Os_Volume_Attachments:
    @classmethod
    def setup_class(cls):
        # 初始化用例参数，将全局变量替换成配置文件中得变量
        # cls.rel = ini_rel
        cls.result = {"result": True}
        # 更新配置文件中的token
        cls.token = token.Token()
        cls.token.save_token()
        cls.log = log.MyLog()
        cls.Assert = assert_pro.Assertions()

    def setup(self):
        self.relevance = conf_relevance.ConfRelevance(
            CONF_PATH, "test_data").get_relevance_conf()

    @pytest.mark.parametrize("case_data", case_dict["test_case"])
    @allure.story("虚拟机挂载和卸载")
    @pytest.mark.flaky(reruns=3)
    def test_os_volume_attachments(self, case_data):
        # 参数化修改test_os_volume_attachments注释
        for k, v in enumerate(case_dict["test_case"]):  # 遍历用例文件中所有用例的索引和值
            try:
                if case_data == v:
                    # 修改方法的__doc__在下一次调用时生效，此为展示在报告中的用例描述
                    Test_Os_Volume_Attachments.test_os_volume_attachments.__doc__ = case_dict[
                        "test_case"][k + 1]["info"]
            except IndexError:
                pass

        if not self.result["result"]:
            # 查看类变量result的值，如果未False，则前一接口校验错误，此接口标记未失败，节约测试时间
            pytest.xfail("前置接口测试失败，此接口标记为失败")

        if case_data["request_type"] == "get":
            time.sleep(case_data["sleep_time"])
        #send_request(_data, _host, _address,_port, _relevance, path, _success)
        code, data = request_send.send_request(
            case_data, case_dict["testinfo"].get("host"), case_dict["testinfo"].get("address"), str(
                case_dict["testinfo"].get("port")), self.relevance, CASE_PATH, self.result)
        expected_code = case_data["check"][0]["expected_code"]

        self.Assert.assert_code(code, expected_code)
        # 完整校验
        check_result.check(
            case_data["test_name"],
            case_data["check"][0],
            code,
            data,
            self.relevance,
            CASE_PATH,
            self.result)


if __name__ == "__main__":
    pytest.main(["-s", "test_06_os_volume_attachments.py"])
