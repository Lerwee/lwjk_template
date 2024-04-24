# linux系统下多端探测模板使用说明

#### 介绍
**以下是 多端探测模板 说明**
一共存在两个模板，分别为
UDP响应探测【agent发起】.yaml
ICMP响应探测【agent发起】.yaml

实现逻辑：
1.  操作系统以安装agent
2.  编写自定义键值，另键值对应本地探测脚本
3.  脚本实现对目标IP设备的PING探测或UDP端口探测

#### 使用说明
##### ICMP响应探测
1.  下载模板文件`ICMP响应探测【agent发起】.yaml`导入监控平台
2.  在agent配置文件中添加`ping_check.conf`中自定义键值行
3.  agent所在操作系统导入脚本`ping.sh`
4.  使用`ICMP响应探测【agent发起】`模板添加对象监控，填写监控对象宏
##### UDP响应探测
1.  下载模板文件`UDP响应探测【agent发起】.yaml`导入监控平台
2.  在agent配置文件中添加`udp_check.conf`中自定义键值行
3.  agent所在操作系统导入脚本`udp_check.py`
4.  使用`UDP响应探测【agent发起】`模板添加对象监控，填写监控对象宏

