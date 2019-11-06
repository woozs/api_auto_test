# #!/usr/bin/env.ini python
# # -*- coding: utf-8 -*-
# # @Time    : 2019/9/20 11:06
# # @Author  : mrwuzs
# # @Site    :
# # @File    : test_02_network.py
# # @Software: PyCharm
#
#
#
import allure
import pytest
import os

from Conf.Config import Config
from Common import Assert
from unit import LoadYaml, Token
from Common import RequestSend
from Conf import  ConfRelevance
from Common import Log
from Common import CheckResult


BASE_PATH = str(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
CASE_PATH = BASE_PATH + "\\Params\\Param\\network"
CONF_PATH = BASE_PATH + "\\Conf\\cfg.ini"
case_dict = LoadYaml.load_case(CASE_PATH + "\\create_network.yaml")

@allure.feature(case_dict["testinfo"]["title"])  # feature定义功能
class Test_Network:

    @classmethod
    def setup_class(cls):
        """
        初始化用例参数，将全局变量替换成配置文件中得变量
        :return:
        """
        cls.result = {"result": True}
        cls.token = Token.Token()
        cls.token.save_token()
        cls.log = Log.MyLog()
        cls.Assert =  Assert.Assertions()

    def setup(self):
        self.relevance =  ConfRelevance.ConfRelevance(CONF_PATH,"test_data").get_relevance_conf()


    @pytest.mark.parametrize("case_data", case_dict["test_case"])
    @allure.story("网络创建和查询")
    def test_network(self,case_data):
        # 参数化修改test_network注释
        for k, v in enumerate(case_dict["test_case"]):  # 遍历用例文件中所有用例的索引和值
            try:
                if case_data == v:
                    # 修改方法的__doc__在下一次调用时生效，此为展示在报告中的用例描述
                    Test_Network.test_network.__doc__ = case_dict["test_case"][k + 1]["info"]
            except IndexError:
                pass

        if not self.result["result"]:
            # 查看类变量result的值，如果未False，则前一接口校验错误，此接口标记未失败，节约测试时间
            pytest.xfail("前置接口测试失败，此接口标记为失败")
        code, data = RequestSend.send_request(case_data, case_dict["testinfo"].get("host"),
                                              case_dict["testinfo"].get("address"),
                                              str(case_dict["testinfo"].get("port")),
                                              self.relevance, CASE_PATH, self.result)
        expected_code = case_data["check"][0]["expected_code"]
        network_id = data["network"]["id"]
        network_name = data["network"]["name"]
        self.log.debug("data:%s"%data)
        self.Assert.assert_code(code,expected_code)
        #保存创建的网络id和网络名称
        if case_data["request_type"] == "post":
            self.log.info("保存network_id到全局配置文件")
            conf =Config()
            conf.set_conf("test_data","network_id",network_id)
            conf.set_conf("test_data", "network_name_for_check", network_name)

        self.log.debug("保存network_name到全局配置文件,用于虚拟校验")
        CheckResult.check(case_data["test_name"], case_data["check"][0],
                          code, data, self.relevance, CASE_PATH, self.result)


if __name__ == "__main__":
    pytest.main(["-s", "test_02_network.py"])