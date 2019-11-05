#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/9/10 22:17
# @Author  : wuzushun
# @Site    : 
# @File    : test_01_project.py
# @Software: PyCharm

import allure
import pytest
import os

from Conf.Config import Config
from Common import Assert
from unit import load_yaml, Token,add_Role_admin
from Common import requestSend
from Conf import  ConfRelevance
from Common import Log


BASE_PATH = str(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
CASE_PATH = BASE_PATH + "\\Params\\Param\\project"
CONF_PATH = BASE_PATH + "\\Conf\\cfg.ini"

case_dict = load_yaml.load_case(CASE_PATH+"\\create_project.yaml")


@allure.feature(case_dict["testinfo"]["title"])  # feature定义功能
class TestAddProject:

    @classmethod
    def setup_class(cls):
        #初始化用例参数，将全局变量替换成配置文件中得变量
        # cls.rel = ini_rel
        with allure.step("初始化环境变量"):
            cls.log = Log.MyLog()
            cls.Assert = Assert.Assertions()
            cls.log.info("设置project_token_name为amdin")
            conf = Config()
            conf.set_conf("test_data", "project_token_name", "admin")
            cls.result = {"result": True}
            #更新配置文件中的token
            cls.token = Token.Token()
            cls.token.save_token()

    def setup(self):
        self.relevance =  ConfRelevance.ConfRelevance(CONF_PATH,"test_data").get_relevance_conf()

    @classmethod
    def teardown_class(cls):
        with allure.step("新建项目赋权"):
            cls.log.info("给新建项目赋权")
            role =  add_Role_admin.Project_Add_Rule()
            role.project_add_role()

    @pytest.mark.parametrize("case_data", case_dict["test_case"])
    @allure.story("创建项目")
    def test_project_crate(self,case_data):
        # 参数化修改test_project_crate注释
        for k, v in enumerate(case_dict["test_case"]):  # 遍历用例文件中所有用例的索引和值
            try:
                if case_data == v:
                    # 修改方法的__doc__在下一次调用时生效，此为展示在报告中的用例描述
                    TestAddProject.test_add_project.__doc__ = case_dict["test_case"][k + 1]["info"]
            except IndexError:
                pass

        if not self.result["result"]:
            # 查看类变量result的值，如果未False，则前一接口校验错误，此接口标记未失败，节约测试时间
            pytest.xfail("前置接口测试失败，此接口标记为失败")

        #send_request(_data, _host, _address,_port, _relevance, path, _success)
        code, data = requestSend.send_request(case_data, case_dict["testinfo"].get("host"),
                                              case_dict["testinfo"].get("address"),
                                              str(case_dict["testinfo"].get("port")),
                                              self.relevance, CASE_PATH, self.result)
        project_id = data["project"]["id"]
        project_name= data["project"]["name"]
        self.Assert.assert_code(code,201)
        with allure.step("保存项目信息到全局配置文件"):
            allure.attach("项目id:%s"%project_id)
            allure.attach("项目名称:%s" % project_name)
        self.log.info("保存project_id到全局配置文件")
        conf =Config()
        conf.set_conf("test_data","project_id",project_id)
        self.log.info("保存项目名称为project_token_name到全局配置文件")
        conf.set_conf("test_data","project_token_name",project_name)


if __name__ == "__main__":
    pytest.main(["-s", "test_01_project.py"])