#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/10/9 18:06
# @Author  : mrwuzs
# @Site    : 
# @File    : CheckResult.py
# @Software: PyCharm
import operator
import re

import allure

from Common import CheckJson, ExpectedManage, CustomFail
from run import failureException


def check(test_name, case_data, code, data, relevance, _path, success):
    """
    校验测试结果
    :param test_name:  测试用例
    :param case_data:  测试用例
    :param code:  HTTP状态
    :param data:  返回的接口json数据
    :param relevance:  关联值对象
    :param _path:  case路径
    :param success:  全局测试结果
    :return:
    """
    # 不校验
    if case_data["check_type"] == 'no_check':
        with allure.step("不校验结果"):
            pass

    # 校验json格式
    elif case_data["check_type"] == 'json':
        expected_request = case_data["expected_request"]
        # 判断预期结果格式，如果是字符串，则打开文件路径，提取保存在文件中的期望结果
        if isinstance(case_data["expected_request"], str):
                expected_request = ExpectedManage.read_json(test_name, expected_request, relevance, _path, success)
        with allure.step("JSON格式校验"):
            allure.attach("期望code", str(case_data["expected_code"]))
            allure.attach('期望data', str(expected_request))
            allure.attach("实际code", str(code))
            allure.attach('实际data', str(data))
        if int(code) == case_data["expected_code"]:
            if not data:
                data = "{}"
            # json校验
            CheckJson.check_json(expected_request, data, success)
        else:
            success["result"] = False
            if case_data.get("CustomFail"):
                info = CustomFail.custom_manage(case_data.get("CustomFail"), relevance)
                raise failureException(str(info)+"\nhttp状态码错误！\n %s != %s" % (code, case_data["expected_code"]))
            else:
                raise failureException("http状态码错误！\n %s != %s" % (code, case_data["expected_code"]))

    # 只校验HTTP状态
    elif case_data["check_type"] == 'only_check_status':
        with allure.step("校验HTTP状态"):
            allure.attach("期望code", str(case_data["expected_code"]))
            allure.attach("实际code", str(code))
        if int(code) == case_data["expected_code"]:
            pass
        else:
            success["result"] = False
            if case_data.get("CustomFail"):
                info = CustomFail.custom_manage(case_data.get("CustomFail"), relevance)
                raise failureException(str(info)+"\nhttp状态码错误！\n %s != %s" % (code, case_data["expected_code"]))
            else:
                raise failureException("http状态码错误！\n %s != %s" % (code, case_data["expected_code"]))

    # 完全校验
    elif case_data["check_type"] == 'entirely_check':
        expected_request = case_data["expected_request"]
        # 判断预期结果格式，如果是字符串，则打开文件路径，提取保存在文件中的期望结果
        if isinstance(case_data["expected_request"], str):
            expected_request = ExpectedManage.read_json(test_name, expected_request, relevance, _path, success)
        with allure.step("完全校验"):
            allure.attach("期望code", str(case_data["expected_code"]))
            allure.attach('期望data', str(expected_request))
            allure.attach("实际code", str(code))
            allure.attach('实际data', str(data))
        if int(code) == case_data["expected_code"]:
            result = operator.eq(expected_request, data)
            if result:
                pass
            else:
                success["result"] = False
                if case_data.get("CustomFail"):
                    info = CustomFail.custom_manage(case_data.get("CustomFail"), relevance)
                    raise failureException(str(info)+"\n完全校验失败！ %s ! = %s" % (expected_request, data))
                else:
                    raise failureException("完全校验失败！ %s ! = %s" % (expected_request, data))
        else:
            success["result"] = False
            raise failureException("http状态码错误！\n %s != %s" % (code, case_data["expected_code"]))

    # 正则校验
    elif case_data["check_type"] == 'Regular_check':
        if int(code) == case_data["expected_code"]:
            try:
                result = ""  # 初始化校验内容
                if isinstance(case_data["expected_request"], list):
                    # 多个正则表达式校验，遍历校验
                    for i in case_data["expected_request"]:
                        result = re.findall(i.replace("\"", "\'"), str(data))
                        allure.attach('校验完成结果\n', str(result))
                else:
                    # 单个正则表达式
                    result = re.findall(case_data["expected_request"].replace("\"", "\'"), str(data))
                    with allure.step("正则校验"):
                        allure.attach("期望code", str(case_data["expected_code"]))
                        allure.attach('正则表达式', str(case_data["expected_request"]).replace("\'", "\""))
                        allure.attach("实际code", str(code))
                        allure.attach('实际data', str(data))
                        allure.attach(case_data["expected_request"].replace("\"", "\'")+'校验完成结果',
                                      str(result).replace("\'", "\""))
                # 未匹配到校验内容
                if not result:
                    success["result"] = False
                    if case_data.get("CustomFail"):
                        info = CustomFail.custom_manage(case_data.get("CustomFail"), relevance)
                        raise failureException(str(info) + "\n正则未校验到内容！ %s" % case_data["expected_request"])
                    else:
                        raise failureException("正则未校验到内容！ %s" % case_data["expected_request"])
            # 正则表达式为空时
            except KeyError:
                success["result"] = False
                raise failureException("正则校验执行失败！ %s\n正则表达式为空时" % case_data["expected_request"])
        else:
            success["result"] = False
            raise failureException("http状态码错误！\n %s != %s" % (code, case_data["expected_code"]))

    # 数据库校验
    elif case_data["check_type"] == "datebase_check":
        pass
    else:
        success["result"] = False
        raise failureException("无该校验方式%s" % case_data["check_type"])


if __name__ == "__main__":
    _test_name = '创建网络'
    _case_data = {'check_type': 'json', 'datebase': None, 'expected_code': 201, 'expected_request': "network_result.json"}
    _code = 201
    _data = {'network': {'status': 'ACTIVE', 'subnets': [], 'name': 'iYKlITwxsp68vBCk7AHF_netwrok', 'provider:physical_network': 'physnet2', 'admin_state_up': True, 'tenant_id': '0fc01b274b6e427d9cbb3555389aa6f6', 'mtu': 0, 'router:external': False, 'qos_policy_id': None, 'shared': False, 'provider:network_type': 'vxlan', 'id': 'f416bcb9-c4df-4fd8-be59-88966f86b135', 'provider:segmentation_id': 1022}}
    _relevance = {'name': '10', 'type': 'Web', 'version': 'StvXfe9YZ2', 'description': 'api_auto_EqKBGiwgol', 'project_id': '0fc01b274b6e427d9cbb3555389aa6f6', 'token_id': 'cb54e6d1b37a4ee6b23f51ea764cffe0', 'project_name': 'D46Pgr2dshlXH3ecTQ7E', 'network_name': 'iYKlITwxsp68vBCk7AHF_netwrok', 'subnet_name': 'a2kCXxNW6J9nrzIEHRuM_subnet', 'network_id': '1bf48f72-7ece-4a10-ac6b-220f43da31df', 'subnet_id': '8a57ec3c-dc96-4d57-9368-c5d922f2b387', 'image_id': 'b4e9e907-686e-440d-bc1a-d73a8decfa54', 'flavor_id': 'flavor-1-1-1', 'server_name': 'wuzs_XR3kjzoNG9wmpME7u0in', 'server_id': 'd0a3a6b4-6f6b-4a7c-89b8-379e5dfef7b3', 'project_token_name': 'V63q02APpfrRcnbLzdTC', 'admin_id': '0ec82b7380cb4d0c80058501938cdf48', 'admin_role_id': 'cc33f2c3a47247329d0ee7043c4f475f', 'volume_name': 'volume_0CvRSMuFrfNJm4enb3hI', 'volume_id': 'e0404b30-8d58-4d2c-a087-6317844d79dd', 'server_snap_name': 'snap_8JkrX4yjSduLBPHcmTxC', 'volume_snapshot_id': '603eeb61-49fc-4b3e-9655-cfe1e099886a'}
    path = r'H:\api_auto_test\Params\Param'
    _success = {'result': True}
    check(_test_name, _case_data, _code, _data, _relevance, path, _success)
