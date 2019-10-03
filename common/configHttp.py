import requests
from common import readConfig as readConfig
from common import log as log
localReadConfig = readConfig.ReadConfig()


# 初始化配置信息，以及请求URL公共方法的一些封装
class ConfigHttp:
    def __init__(self):
        # 全局变量
        global scheme, host, port, timeout
        self.logger = log.Logg().get_logger()
        scheme = localReadConfig.get_http("scheme")
        host = localReadConfig.get_http("baseurl")
        port = localReadConfig.get_http("port")
        timeout = localReadConfig.get_http("timeout")
        self.headers = {}
        self.params = {}
        self.data = {}
        self.url = None
        self.files = {}
        self.state = 0

    def set_url(self, url):
        self.url = scheme+'://'+host+url

    def set_headers(self, header):
        self.headers = header

    def set_params(self, param):
        self.params = param

    def set_data(self, data):
        self.data = data

    def set_files(self, filename):
        if filename != '':
            file_path = 'F:/AppTest/Test/interfaceTest/testFile/img/' + filename
            self.files = {'file': open(file_path, 'rb')}

        if filename == '' or filename is None:
            self.state = 1

    # get 公共方法封装
    def get(self):
        try:
            response = requests.get(self.url, headers=self.headers, params=self.params, timeout=float(timeout))
            return response
        except TimeoutError:
            self.logger.error("Time out")
            return None

    # 定义post方法
    def post(self):
        try:
            response = requests.post(self.url, headers=self.headers, params=self.params, data=self.data,
                                     timeout=float(timeout))
            return response
        except TimeoutError:
            self.logger.error("Time out")
            return None

    def post_with_file(self):
        try:
            response = requests.post(self.url, headers=self.headers, data=self.data, files=self.files,
                                     timeout=float(timeout))
            return response
        except TimeoutError:
            self.logger.error("Time out")
            return None

    def post_with_json(self):
        try:
            response = requests.post(self.url, headers=self.headers, json=self.data, timeout=4)
            return response
        except TimeoutError:
            self.logger.error("Time out")
            return None
