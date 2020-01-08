#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/10/9 18:07
# @Author  : mrwuzs
# @Site    : 
# @File    : check_json.py
# @Software: PyCharm

from run import failureException

result = 'success'  # 初始化结果结果为success


def check_json(src_data, dst_data, success):
    """
    校验的json
    :param src_data:  校验内容
    :param dst_data:  接口返回的数据（被校验的内容)
    :param success:  全局测试结果
    :return:
    """
    global result

    if isinstance(src_data, dict):
        # 若为dict格式
        for key  in src_data:

            if key not in dst_data:
                success["result"] = False
                raise failureException("JSON格式校验，关键字 %s 不在返回结果 %s" % (key, dst_data))

            elif  type(src_data[key]) is not dict and src_data[key]  != dst_data[key]:
                value = src_data[key]

                success["result"] = False
                raise failureException("JSON格式校验，关键字 %s 不在返回结果 %s" % (value, dst_data))

            else:
                this_key = key
                # 递归
                if isinstance(src_data[this_key], dict) and isinstance(dst_data[this_key], dict):
                    check_json(src_data[this_key], dst_data[this_key], success)
                elif isinstance(type(src_data[this_key]), type(dst_data[this_key])):
                    success["result"] = False
                    raise failureException("JSON格式校验，关键字 %s 与 %s 类型不符" % (src_data[this_key], dst_data[this_key]))
                else:
                    pass

    else:
        success["result"] = False
        raise failureException("JSON校验内容非dict格式")


if __name__ == "__main__":
    src = {'status': 'active', 'name': 'snap', 'deleted': False, 'disk_format': 'vmdk', 'is_public': False, 'properties': {'instance_uuid': 'd00438ed-d2f7-48a8-8a47-e3e707f5759b', 'image_type': 'snapshot', 'hypervisor_type': 'vmware', 'vmware_disktype': 'streamOptimized', 'vmware_image_version': '1', 'vmware_adaptertype': 'ide', 'vmware_ostype': 'centos64Guest'}}
    dst = {'status': 'ACTIVE', 'subnets': [], 'name': 'iYKlITwxsp68vBCk7AHF_netwrok', 'provider:physical_network': 'physnet2', 'admin_state_up': True, 'tenant_id': '0fc01b274b6e427d9cbb3555389aa6f6', 'mtu': 0, 'router:external': False, 'qos_policy_id': None, 'shared': False, 'provider:network_type': 'vlan', 'id': 'f416bcb9-c4df-4fd8-be59-88966f86b135', 'provider:segmentation_id': 1022}
    _success = dict()
    _success["result"] = True
    check_json(src, dst, _success)
    print(_success["result"])
    # check_json(dis_src, dst, _success)
    # print(_success["result"])
