# @Time: 2019/12/4 10:49
# @User: Win-lhy
# @IDE: PyCharm
# @Author: lhy
# @File: ConnectDb2.py

import ibm_db
import datetime
from config.db2config import dbbase
from publib.savedata.savelogs.SaveLog import SaveLog

savelog = SaveLog().save_log()
class ConnectDb2:
    def __init__(self):
        self.db2info = dbbase

    def content_db2(self, dbbasename='db99'):
        dbinfo = self.db2info[dbbasename]
        savelog.info(f'连接db2数据库[{dbbasename}]')
        dbinfostr = f"DATABASE={dbinfo['DATABASE']};HOSTNAME={dbinfo['HOSTNAME']};" \
                    f"PORT={dbinfo['PORT']};PROTOCOL={dbinfo['PROTOCOL']};" \
                    f"UID={dbinfo['UID']};PWD={dbinfo['PWD']};"
        conn = ibm_db.connect(dbinfostr, "", "")
        if conn:
            return conn
        else:
            assert 0 == 1, savelog.error(f'连接到db2数据库[{dbbasename}]-->失败')

    def get_db2_data(self, sqlstr, dbbasename='db99'):
        conn = self.content_db2(dbbasename)
        savelog.debug(f'db2数据库[{dbbasename}]内执行[{sqlstr}]')
        stmt = ibm_db.exec_immediate(conn, sqlstr)
        result = ibm_db.fetch_both(stmt)
        savelog.debug(f'db2数据库[{dbbasename}]内查询到的结果：{result}')
        ibm_db.close(conn)
        savelog.debug(f'关闭与db2数据库[{dbbasename}]的连接')
        return result


    def set_db2_data(self, sqlstr, dbbasename='db99'):
        conn = self.content_db2(dbbasename)
        savelog.debug(f'db2数据库[{dbbasename}]内执行[{sqlstr}]')
        ibm_db.exec_immediate(conn, sql)
        ibm_db.close(conn)
        savelog.debug(f'关闭与db2数据库[{dbbasename}]的连接')
        return

    def filterdict(self, datadict):
        wantemp = {}
        for key, value in datadict.items():
            if isinstance(key, int):
                continue
            if isinstance(value, datetime.date):
                value = value.strftime('%Y-%m-%d')
            key = key.lower()
            wantemp[key] = value
        return wantemp



if __name__ == '__main__':
    cd2 = ConnectDb2()
    sql = r"select agentcode,NAME,IDNOTYPE,IDNO,MOBILE,MANAGECOM,AGENTSTATE,EMPLOYDATE from db2inst1.laagent t where t.agentcode='G2550000139';"
    aa = cd2.get_db2_data(sql)
    print(aa)
    import datetime

    print(cd2.filterdict(aa))