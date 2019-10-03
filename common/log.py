import os
import logging
from datetime import datetime
from common import readConfig as readConfig
localReadConfig = readConfig.ReadConfig


class Logg:
    def __init__(self):
        global logPath, resultPath, proDir
        proDir = readConfig.proDir
        #  创建结果文件夹
        resultPath = os.path.join(proDir, "result")
        # os.path.exists()方法可以直接判断文件/文件夹是否存在
        if not os.path.exists(resultPath):
            os.mkdir(resultPath)
        #  os.path.join拼接
        logPath = os.path.join(resultPath, str(datetime.now().strftime("%Y%m%d%H%M%S")))
        #  使用接口debug，info，warn，error，critical之前必须创建Logger实例
        self.logger = logging.getLogger()
        #  logger,setLevel(logging.ERROR)# 设置日志的级别为ERROR，即只有日志级别大于ERROR的日志才会输出
        self.logger.setLevel(logging.INFO)

        # Handler 处理器，将（记录器产生的）日志记录发送至合适的目的地
        handler = logging.FileHandler(os.path.join(resultPath, "output.log"), encoding="utf-8")
        # formatter 格式化器，指明了最终输出中日志记录的布局
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        #  使用Formatter对象设置日志信息最后的规则、结构和内容，默认的时间格式为%Y-%m-%d %H:%M:%S
        handler.setFormatter(formatter)
        #  为Logger实例增加一个处理器
        self.logger.addHandler(handler)

    def get_logger(self):
        #  获取记录
        return self.logger

    def build_start_line(self, case_no):
        #  写入起始行
        self.logger.info("--------" + case_no + " START--------")

    def bulid_end_line(self, case_no):
        #  写入结束行
        self.logger.info("--------" + case_no + " END--------")

    def build_case_line(self, case_name, code, msg):
        #  编写测试用例行
        self.logger.info(case_name + " - Code:" + code + " - msg:" + msg)

    def get_report_path(self):
        #  获取报告路径
        report_path = os.path.join(resultPath, "report.html")
        return report_path

    def get_result_path(self):
        #  获取测试结果路径
        return logPath
