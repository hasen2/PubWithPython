# @Time: 2019/12/9 17:12
# @User: Win-lhy
# @IDE: PyCharm
# @Author: lhy
# @File: ConnectToMysql.py


import MySQLdb
from config.Mysqlconfig import mysqlbase
from publib.savedata.savelogs.SaveLog import SaveLog

savelog = SaveLog().save_log()

class ConnectToMysql:
    def __init__(self):
        pass

    def connect_mysql(self, basename='本地'):
        """
        根据传入的ipnum，自动匹配并连接对应的mysql数据库信息
        :param ipnum: 数据库序号[104]
        """
        # 数据库地址
        address = mysqlbase[basename]
        savelog.debug(f'''连接数据库[{address['host']}][{address['dbname']}]''')
        connection = MySQLdb.connect\
            (host=address['host'], # 指定ip
             user=address['username'],  # 用户名
             passwd=address['passwd'], # 密码
             db=address['dbname'],  #连接的库
             charset=address['charset'] # 指定数据库对应的编码
             )
        return connection, connection.cursor()  # 建立游标



    def operate_datas(self,sqllist,basename='本地'):
        """
        执行增删改语句
        :param sqllist: 需要执行的sql列表，列表的元素为字典，字典的key是sql的注释，value是具体的sql语句
        :return: 列表（每条sql操作的行数）
        """
        conn,connmysql = self.connect_mysql(basename=basename)
        operatenumlist = []
        savelog.info(f'本次执行的sql：{sqllist}')
        for sqldict in sqllist:
            for key, value in sqldict.items():
                savelog.debug(f'执行sql[{key}:{value}]')
                connmysql.execute(value)  # 注释sql，查询
                numrows = connmysql.rowcount  # 返回最近一次操作到的行数
                operatenumlist.append(numrows)
                savelog.debug(f'操作的行数：{numrows}')
                conn.commit()
        savelog.info(f'执行结束。')
        connmysql.close()
        return operatenumlist

    def get_datas(self,sqllist,basename='本地' ):
        """
        执行查询语句
        :param sqllist: 需要执行的sql列表，列表的元素为字典，字典的key是sql的注释，value是具体的sql语句
        :return: 列表（每条sql查询到的结果）
        """
        _,connmysql = self.connect_mysql(basename=basename)
        getdatas = []
        savelog.info(f'本次查询的sql：{sqllist}')
        for sqldict in sqllist:
            for key, value in sqldict.items():
                savelog.debug(f'执行sql[{key}:{value}]')
                connmysql.execute(value)
                alldatas = connmysql.fetchall()
                # self.aa.autocommit(True)
                getdatas.append(alldatas)
                savelog.debug(f'查出的数据：{alldatas}')
        savelog.info(f'本次查询出的所有数据：{getdatas}')
        connmysql.close()
        return getdatas[0] if len(getdatas) > 0 else getdatas

    def close_mysql(self,conn):
        conn.close()
        savelog.debug(f'关闭数据库的连接。')




if __name__ == '__main__':
    sql2dict={
        # 'sql':"select sportStartTime,SportEndTime,createdate from usr_sport where UserSysID = 300093 and sportStartTime >= '2019-05-01'and sportflag=1;",
        # 'sql':'insert into usr_sport VALUES(\'2019-05-17\',\'2019-05-17\', 300093 ,"0","506","20","999",\'2019-05-17\',\'2019-05-17\',\'2019-05-17\',"1")'
        'sql':f'''select tpbh.headkey,tpbh.headvalue
from tb_pub_body_head tpbh
where tpbh.headclasstype='head001';'''
    }

    sql2list=[sql2dict]
    test = ConnectToMysql()
    aa=test.get_datas(sql2list)



    print(aa)

