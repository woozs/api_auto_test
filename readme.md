# 环境要求：

```
requests_toolbelt==0.9.1
requests==2.20.0
allure_python_commons==2.8.5
pytest==5.2.1
simplejson==3.16.0
config==0.4.2
PyYAML==5.1.2
```

# 安装allure

XQwindows下安装 Allure工具
环境
1、安装JDK1.8+
2、安装Allure
下载Allure的zip安装包，点击此处
解压到allure-commandline目录
进入bin目录，运行allure.bat
添加allure到环境变量PATH（\安装路径\allure-commandline\bin）

# 测试框架介绍

![](https://raw.githubusercontent.com/JasonsteagleWu/picgo_01/master/20191029094204.png)

# 配置文件

```ini
[email]#配置邮件发送和接受
send = yes
smtpserver = smtp.qq.com
port = 465
sender = xxxxxxxx
psw = xxxxx
receiver = 627383987@qq.com,mrwuzs@ctsi.com.cn
username = 627383987@qq.com

[env]
#定义环境信息，用于报告展示和接口数据
tester = wuzushun
environment = 192.168.54.120
versioncode = 1.0
host = 192.168.54.120
logininfo = {"auth": {"scope": {"project": {"domain":{"id": "default"},"name": "${project_token_name}$"}}, "identity":{"password": {"user": {"domain":{"id": "default"},"password":"admin","name":"admin"}},"methods":["password"]}}}
openstack_version = liberty
virtual = VMware
nova_api = v2
cinder_api = v2
neutron_api = v2
glance_api = v2
keystone_api = v3

[test_data]
#测试数据，用于解决环境资源依赖问题
name = $RandomInt(0,10)$
type = Web
version = $RandomString(10)$
description = api_auto_$RandomString(10)$
project_id = 693fff2b334d48eeb3921e4dd1d4a592
token_id = 49aa0e8a330c4c2d9e12121b4bd280e3
project_name = $RandomString(20)$
network_name = $RandomString(20)$_netwrok
subnet_name = $RandomString(20)$_subnet
network_id = 83723762-af39-4fdc-ae5b-28b0ef04496e
subnet_id = 8a57ec3c-dc96-4d57-9368-c5d922f2b387
image_id = b4e9e907-686e-440d-bc1a-d73a8decfa54  
#必须配置，用于创建虚拟机
flavor_id = flavor-1-1-1  #必须配置，用于创建虚拟机
server_name = wuzs_$RandomString(20)$
server_id = d0a3a6b4-6f6b-4a7c-89b8-379e5dfef7b3
project_token_name = admin
admin_id = 0ec82b7380cb4d0c80058501938cdf48  
#必须配置，用户授权用
admin_role_id = cc33f2c3a47247329d0ee7043c4f475f  
#必须配置，给用户授权用
volume_name = volume_$RandomString(20)$
volume_id = e0404b30-8d58-4d2c-a087-6317844d79dd
server_snap_name = snap_8JkrX4yjSduLBPHcmTxC
volume_snapshot_id = 603eeb61-49fc-4b3e-9655-cfe1e099886a

```

1，需要现在opentack获取

image_id，flavor_id，admin_id，role_id

```
admin_id = `openstack user list | awk  '/admin/{print$2}'`
role_id = `openstack role list | awk  '/admin/{print$2}'`
image_id= glance images-list#选择合适的镜像
flavor_id =  获取合适的镜像
```

# 测试用例示例

如创建网络，测试用例为yaml文件，按照示例增加用例

```yaml
testinfo:
      id: test_02_create_network        # 用例ID， 用于识别   
      title: 创建网络                 # 用例标题，在报告中作为一级目录显示  必填 string
      port: 9696          # 请求的端口号
      address: /v2.0/networks # 请求地址 选填（此处不填，每条用例必填） string
# 前置条件，case之前需关联的接口
premise:
# 测试用例
test_case:
      # 第一条case，info可不填
    - test_name: 创建网络       # 必填，parameter为文件路径时
      info: 创建网络
      http_type: http          # 请求协议
      request_type: post      # 请求类型
      parameter_type: raw     # 参数类型
      address: /v2.0/networks
      headers:                # 请求头
            Content-Type: application/json
            X-Auth-Token: ${token_id}$
      timeout: 20 
      parameter:
        network:
          admin_state_up: true
#          dns_domain:
#          mtu: 1500
          name: ${network_name}$
#          port_security_enabled:
#          project_id: ${project_id}$
#          provider:network_type:
#          provider:physical_network:
#          provider:segmentation_id:
#          qos_policy_id:
#          router:external:
#          segments:
#          shared: Flase
          tenant_id:  ${project_id}$
#          vlan_transparent:
#          description: "auto_wuzs"
#          is_default:
#          availability_zone_hints:
      file: false
      check:             # 校验列表  list or dict
          - check_type: json # 校验类型 string   不校验时 datebase， expected_code, expected_request 均可不填
            datebase:
            expected_code: 201
            expected_request: network_result.json  #result，用于校验
      relevance:  # 关联键
    - test_name: 查看网络
      info: 查询网络
      http_type: http          # 请求协议
      request_type: get      # 请求类型
      parameter_type: raw     # 参数类型
      address: /v2.0/networks/${network_id}$
      headers:                # 请求头
        Content-Type: application/json
        X-Auth-Token: ${token_id}$
      timeout: 20
      parameter:
        network:
          admin_state_up: true
          name: ${network_name}$
          tenant_id:  ${project_id}$
      file: false
      check:             # 校验列表  list or dict
          - check_type: json # 校验类型 string   不校验时 datebase， expected_code, expected_request 均可不填
            datebase:
            expected_code: 200
            expected_request: {}
      relevance:  # 关联键

```

需要json的文件校验，可以把json文件名写到expected_request，用于校验,如：用于校验json文件，按照示例更改，根据需要可以添加需要校验内容

```json
[{
	"json": [{
		"network": {
			"status": "ACTIVE",
			"subnets": [],
			"provider:physical_network": "physnet2",
			"admin_state_up": true,
			"mtu": 0,
			"router:external": false,
			"qos_policy_id": null,
			"shared": false,
			"provider:network_type": "vlan"}}],
	"test_name": "创建网络"},
	{
	"json": [{
		"network": {
			"status": "ACTIVE",
			"subnets": [],
			"provider:physical_network": "physnet2",
			"admin_state_up": true,
			"mtu": 0,
			"router:external": false,
			"qos_policy_id": null,
			"shared": false,
			"provider:network_type": "vlan"}}],
	"test_name": "查看网络"}
]
```



# 用例执行

用到的插件

```
@pytest.mark.flaky(reruns=3)#失败重跑，尝试重跑3次
@allure.feature # 用于定义被测试的功能，被测产品的需求点
@allure.story # 用于定义被测功能的用户场景，即子功能点
@allure.attach # 用于向测试报告中输入一些附加的信息，通常是一些测试数据信息
@pytest.mark.parametrize #参数化
```

# 测试报告查看

![](https://raw.githubusercontent.com/JasonsteagleWu/picgo_01/master/20191101174308.png)![](https://raw.githubusercontent.com/JasonsteagleWu/picgo_01/master/20191101174105.png)

![](https://raw.githubusercontent.com/JasonsteagleWu/picgo_01/master/20191101174356.png)

