#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/10/20 19:36
# @Author  : mrwuzs
# @Site    : 
# @File    : InitializeEnv.py
# @Software: PyCharm

import os
from Common.Log import MyLog as logging
from Conf.ConfRelevance import ConfRelevance




BASE_PATH = str(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
CONF_PATH = BASE_PATH + "\\Conf\\cfg.ini"
ENV_PATH  = BASE_PATH + "\\Report\\xml\\environment.xml"


class Init_Env:
    """初始化环境信息，更新xml文件"""

    def __init__(self):
        logging.info("初始化关联文件")
        self.data =  ConfRelevance(CONF_PATH,"env").get_relevance_conf()




    def dict_to_xml(self):
        parameter = []
        for k in sorted(self.data.keys()):
            xml = []
            v = self.data.get(k)
            if k == 'detail' and not v.startswith('<![CDATA['):
                v = '<![CDATA[{}]]>'.format(v)
            xml.append('<key>{value}</key>'.format(value=k))
            xml.append('<value>{value}</value>'.format(value=v))
            parameter.append('<parameter>{}</parameter>'.format(''.join(xml)))

        return '<environment>{}</environment>'.format(''.join(parameter))

    def save_to_xml(self):
        data = self.dict_to_xml()
        with open(ENV_PATH,'w') as f:
            f.write(data)

    def init(self):
        self.save_to_xml()


if __name__ == '__main__':
    Init =  Init_Env()
    Init.init()


