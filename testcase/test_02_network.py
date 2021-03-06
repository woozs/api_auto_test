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

from conf.conf import Config
from common import assert_pro
from unit import load_yaml, token
from common import request_send
from conf import conf_relevance
from common import log
from common import check_result


BASE_PATH = str(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
CASE_PATH = BASE_PATH + "\\params\\param\\network"
CONF_PATH = BASE_PATH + "\\conf\\cfg.ini"
case_dict = load_yaml.load_case(CASE_PATH + "\\create_network.yaml")


@allure.feature(case_dict["testinfo"]["title"])  # feature定义功能
class Test_Network:

    @classmethod
    def setup_class(cls):
        """
        初始化用例参数，将全局变量替换成配置文件中得变量
        :return:
        """
        cls.result = {"result": True}
        cls.token = token.Token()
        cls.token.save_token()
        cls.log = log.MyLog()
        cls.Assert = assert_pro.Assertions()

    def setup(self):
        self.relevance = conf_relevance.ConfRelevance(
            CONF_PATH, "test_data").get_relevance_conf()

    @pytest.mark.parametrize("case_data", case_dict["test_case"])
    @allure.story("网络创建和查询")
    def test_network(self, case_data):
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
        code, data = request_send.send_request(case_data, case_dict["testinfo"].get("host"),
                                               case_dict["testinfo"].get("address"),
                                               str(case_dict["testinfo"].get("port")),
                                               self.relevance, CASE_PATH, self.result)
        expected_code = case_data["check"][0]["expected_code"]
        network_id = data["network"]["id"]
        network_name = data["network"]["name"]
        self.log.debug("data:%s" % data)
        self.Assert.assert_code(code, expected_code)
        # 保存创建的网络id和网络名称
        if case_data["request_type"] == "post":
            self.log.info("保存network_id到全局配置文件")
            conf = Config()
            conf.set_conf("test_data", "network_id", network_id)
            conf.set_conf("test_data", "network_name_for_check", network_name)

        self.log.debug("保存network_name到全局配置文件,用于虚拟校验")
        check_result.check(case_data["test_name"], case_data["check"][0],
                           code, data, self.relevance, CASE_PATH, self.result)


if __name__ == "__main__":
    pytest.main(["-s", "test_02_network.py"])
