import os
import codecs
import configparser

proDir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
configPath = proDir+"\data\config.ini"


class ReadConfig:
    def __init__(self):
        fd = open(configPath)
        data = fd.read()
        if data[:3] == codecs.BOM_UTF8:
            data = data[3:]
            file = codecs.open(configPath, "w")
            file.write(data)
            file.close()
        fd.close()
        # 创建对象
        self.cf = configparser.ConfigParser()

        # 读取配置
        self.cf.read(configPath)

    def get_http(self, name):
        value = self.cf.get("HTTP", name)
        return value

    def get_headers(self, name):
        value = self.cf.get("HEADERS", name)
        return value

    def set_headers(self, name, value):
        self.cf.set("HEADERS", name, value)
        with open(configPath, 'w+') as f:
            self.cf.write(f)
            
    def get_db(self, name):
        value = self.cf.get("DATABASE", name)
        return value
