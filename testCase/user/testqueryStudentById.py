# -*- coding:utf-8 -*-
import unittest
import paramunittest
from common import readConfig as readConfig
from common import common
from common import configHttp
from common import log as log
localReadConfig = readConfig.ReadConfig()
localConfigHttp = configHttp.ConfigHttp()
queryStudentById_xls = common.get_xls("userCase.xlsx", "queryStudentById")


@paramunittest.parametrized(*queryStudentById_xls)
class QueryStudentById(unittest.TestCase):
    def setParameters(self, case_name, timestamp, errno, city_name):
        self.case_name = str(case_name)
        self.timestamp = str(timestamp)
        self.errno = str(errno)
        self.cityName = str(city_name)
        self.info = None
        self.url = None

    def setUp(self):
        # 初始化
        self.log = log.Logg()
        self.logger = self.log.get_logger()
        print(self.case_name + "测试开始前准备")

    #  获取url地址
    def testQueryStudentById(self):
        '''根据学员id查询学员信息接口'''
        self.url = common.get_url_from_xml('queryStudentById')
        localConfigHttp.set_url(self.url)
        #  获取commontoken信息
        token_v = common.get_visitor_token()
        header = {"Content-Type": 'application/json', "authorization": token_v}
        localConfigHttp.set_headers(header)
        # set param
        send_param = {"timestamp": self.timestamp}
        localConfigHttp.set_data(send_param)
        # 请求对应封装接口
        self.respon = localConfigHttp.post_with_json()

        # 调用checkResult方法
        self.checkResult()

    def tearDown(self):
        pass
    # 较验json格式返回值

    def checkResult(self):
        # 获取json格式值
        self.info = self.respon.json()
        common.show_return_msg(self.respon)
        self.info = self.respon.json()
        #  判断状态是否是200
        if self.respon.status_code == 200:
            print(self.info['error'])
            self.assertEqual(self.info['errno'], int(self.errno))
            self.assertEqual(self.info['data']['cityName'], str(self.cityName))
