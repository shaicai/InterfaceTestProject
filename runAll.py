import os
import unittest
from common.log import Logg
from common import readConfig as readConfig
from common import HTMLTestRunner
localReadConfig = readConfig.ReadConfig()
cc = Logg()


class AllTest:
    #  设置初始值，获取各个路径，设置全局变量
    def __init__(self):
        global log, logger, resultPath, fp
        log = cc.get_logger()
        logger = cc.get_logger()
        #  获取报告路径
        resultPath = cc.get_report_path()
        fp = open(resultPath, 'wb')
        #  得到文件的路径/caselist.txt
        self.caseListFile = os.path.join(readConfig.proDir, "caselist.txt")
        #  获取文件的文字路径
        self.caseFile = os.path.join(readConfig.proDir, "testCase")
        self.caseList = []

    #  设置执行的case
    def set_case_list(self):
        fb = open(self.caseListFile)
        for value in fb.readlines():
            #  获取data值，user/testStudentLogin
            data = str(value)
            if data != '' and not data.startswith("#"):
                self.caseList.append(data.replace("\n", ""))
        fb.close()

    #  设置测试套件
    def set_case_suite(self):
        self.set_case_list()
        test_suite = unittest.TestSuite()
        suite_module = []
        for case in self.caseList:
            #  截取后缀testStudentLogin
            case_name = case.split("/")[-1]
            #  定义测试目录为当前目录：
            #  top_level_dir = None:测试模块的顶级目录，如果没有顶级目录，默认为None
            discover = unittest.defaultTestLoader.discover(self.caseFile, pattern=case_name + '.py', top_level_dir=None)
            suite_module.append(discover)
        if len(suite_module) > 0:
            for suite in suite_module:
                for test_name in suite:
                    test_suite.addTest(test_name)
        else:
            return None
        return test_suite

    #  报告执行
    def run(self):
        try:
            #  执行测试套件
            suit = self.set_case_suite()
            #  执行日志信息
            if suit is not None:
                logger.info("********TEST START********")
                #  执行测试报告
                runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title=u"接口测试报告", description=u"用例执行情况")
                #  运行测试用例
                runner.run(suit)
            else:
                logger.info("没有测试案例")
                # pass
        except Exception as ex:
            logger.error(str(ex))
        finally:
            logger.info("测试结束")
            fp.close()


if __name__ == '__main__':
        obj = AllTest()
        obj.run()
