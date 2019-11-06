#!/usr/bin/env.ini python
# -*- coding: utf-8 -*-
# @Time    : 2019/9/11 15:34
# @Author  : mrwuzs
# @Site    :
# @File    : run.py
# @Software: PyCharm


"""
运行用例集：
    python3 run.py

# '--allure_severities=critical, blocker'
# '--allure_stories=测试模块_demo1, 测试模块_demo2'
# '--allure_features=测试features'

"""

import pytest

from Common import Log
from Common import Shell
from Conf import Config
from Common import Email
from unit import InitializeEnv


failureException = AssertionError

if __name__ == '__main__':

    conf = Config.Config()
    log = Log.MyLog()
    log.info('初始化配置文件, path=' + conf.conf_path)
    shell = Shell.Shell()
    xml_report_path = conf.xml_report_path
    html_report_path = conf.html_report_path

    # 初始化allure环境配置文件environment.xml
    InitializeEnv.Init_Env().init()

    # 定义测试集
    args = ['-s', '-q', '--alluredir', xml_report_path]
    # args = ['-s', '-q', '--alluredir', "H:\\api_auto_test\\Report\xml"]
    pytest.main(args)
    cmd = 'allure generate %s -o %s  --clean' % (
        xml_report_path, html_report_path)
    log.info("执行allure，生成测试报告")
    try:
        shell.invoke(cmd)
    except Exception:
        log.error('执行用例失败，请检查环境配置')
        raise

    if conf.send == "yes":
        try:
            mail = Email.SendMail()
            mail.sendMail()
        except Exception as e:
            log.error('发送邮件失败，请检查邮件配置')
            raise
    elif conf.send == "no":
        log.info("配置为发送邮件")
    else:
        raise RuntimeError('配置文件错误:send只能为"yes" or "no"')
