# -*- coding:utf-8 -*-
import unittest
#  参数化
import paramunittest
#  读取配置信息
from common import readConfig as readConfig
#  调用公共方法
from common import common
#  导入它的方法 主要1.设置URL以及请求信息等 2.调用封装的GET POST JSON格式格式方法
from common import configHttp
#  调用读取配置信息
localReadConfig = readConfig.ReadConfig()
#  调用读取请求方法

localConfigHttp = configHttp.ConfigHttp()
#  调用common公共读取EXCEL方法
studentLogin_xls = common.get_xls("userCase.xlsx", "studentLogin")
#  参数化读取 *代表读取所有的case


@paramunittest.parametrized(*studentLogin_xls)
class StudentLogin(unittest.TestCase):
    #  读取EXCEL值
    def setParameters(self, case_name, method, phone, password, result_type, message_code, login_type, timestamp,
                      errno, error):
        self.case_name = str(case_name)
        self.method = str(method)
        self.phone = str(phone)
        self.password = str(password)
        self.resultType = str(result_type)
        self.messageCode = str(message_code)
        self.loginType = str(login_type)
        self.timestamp = str(timestamp)
        self.errno = str(errno)
        self.error = str(error)
        self.info = None
        self.url = None

    def setUp(self):
        # 初始化
        print(self.case_name + "测试开始前准备")

    def testStudentLogin(self):
        '''学生端登陆'''
        self.url = common.get_url_from_xml('studentLogin')
        #  设置到confighttp
        localConfigHttp.set_url(self.url)
        print("第一步：设置url  " + self.url)
        header = {"Content-Type": 'application/json'}
        print("第二步：设置header信息(token等)")
        localConfigHttp.set_headers(header)

        # set param
        print("第三步：设置发送请求的参数")
        send_param = {"phone": self.phone, "password": self.password, "messageCode": self.messageCode,
                      "loginType": self.loginType, "timestamp": self.timestamp}
        localConfigHttp.set_data(send_param)
        # 请求对应封装接口
        print("第四步：发送请求json格式直接调用confighttp中的方法")
        self.respon = localConfigHttp.post_with_json()

        # 调用checkResult方法
        print("第五步：检查较验结果是否正确")
        self.checkResult()

    def tearDown(self):
        pass

    # 较验json格式返回值
    def checkResult(self):
        # 获取json格式值
        self.info = self.respon.json()
        #  调用show_return_msg方法是为了把url json值打印到报告每条CASE详情中
        common.show_return_msg(self.respon)
        #  判断状态是否是200
        if self.resultType == '0' and self.respon.status_code == 200:
            #  预期接口返回的200与EXCEL读取200是否一致
            self.assertEqual(self.info['errno'], int(self.errno))
            self.assertEqual(self.info['error'], "操作成功")
        if self.resultType == '1' and self.respon.status_code == 200:
            self.assertEqual(self.info['errno'], int(self.errno))
            self.assertEqual(self.info['error'], self.error)
