from publib.apidatalib.GetDataToApi import GetDataToApi
from publib.apidatalib.MysqlGetData import MysqlGetData

# 将库里的各个类设置为全局变量，引用时直接引用该文件夹
class apidatalib(GetDataToApi,MysqlGetData):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    # def __init__(self,driver):
    #     super().__init__(driver)