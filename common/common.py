import requests
import json
import os
from common.log import Logg
from xlrd import open_workbook
import common.readConfig as readConfig
from xml.etree import ElementTree as ElementTree
from common import configHttp as configHttp
# 导入方法
localReadConfig = readConfig.ReadConfig()
# 获取文件的路径
proDir = readConfig.proDir
localConfigHttp = configHttp.ConfigHttp()
logger = Logg().get_logger()
caseNo = 0


def get_visitor_token():
    send_param = {"phone": 14000000000, "password": "e10adc3949ba59abbe56e057f20f883e", "messageCode": "0",
                  "loginType": "1", "timestamp": "0"}
    urllist = localReadConfig.get_http("BASEURL")
    headers = {"Content-Type": 'application/json'}
    res = requests.post("http://"+urllist + "/backend/student/unauth/login", data=json.dumps(send_param),
                        headers=headers, timeout=4)
    # header中获取token
    token = res.headers['authorization']
    logger.debug("Create token:%s" % token)
    return token


# 返回接口信息公共方法
def show_return_msg(response):
    # 返回response返回信息
    url = response.url
    # 返回json返回值
    msg = response.text
    print("\n请求地址：" + url)
    # 可以显示中文
    print("\n请求返回值:" + '\n' + json.dumps(json.loads(msg), ensure_ascii=False, sort_keys=True, indent=4))


# 从excel文件中读取测试用例
def get_xls(xls_name, sheet_name):
    """
    get intetface data from xls file
    :param xls_name:
    :param sheet_name:
    :return:
    """
    cls = []
    xls_path = os.path.join(proDir, "testFile", 'case', xls_name)
    # D:\interfaceTest\testFile\case\userCase.xlsx
    # 打开文件
    file = open_workbook(xls_path)
    # 按照名称获取工作列表
    sheet = file.sheet_by_name(sheet_name)
    # 获取页的一行
    nrows = sheet.nrows
    for i in range(nrows):
        if sheet.row_values(i)[0] != u'case_name':
            cls.append(sheet.row_values(i))
    return cls


# 从interfaceurl.xml中获取接口url对应路径
def get_url_from_xml(name):
    url_list = []
    url_path = os.path.join(proDir, 'testFile', 'interfaceURL.xml')
    # 解析xml
    tree = ElementTree.parse(url_path)
    for u in tree.findall('url'):
        url_name = u.get('name')
        if url_name == name:
            for c in u.getchildren():
                url_list.append(c.text)
    url = '/backend/'+'/'.join(url_list)
    return url


if __name__ == "__main__":
    get_visitor_token()
