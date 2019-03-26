# _*_ coding:utf-8 _*_
import pymysql
from sshtunnel import SSHTunnelForwarder

class DBConnector(object):

    # 传入需要连接的数据库的名称dbname和待执行的sql语句sql
    def __init__(self, dbname):
        """
        database name
        :param dbname:
        """
        self.dbname = dbname
        self.row_each_page = 5  # 每一页显示五条数据
        self.cursor = self.__getConn__()

    def close(self):
        self.cursor.close()
        self.db_connect.close()
        self.server.close()

    def __getConn__(self):
        self.server = SSHTunnelForwarder(
            ('120.79.92.230', 22),  # 跳板机（堡垒机）B配置
            ssh_password="Shirlim123",
            ssh_username="root",
            remote_bind_address=("127.0.0.1", 3306))  # 数据库存放服务器C配置
        self.server.start()

        # 打开数据库连接
        self.db_connect = pymysql.connect(host='127.0.0.1',  # 本机主机A的IP（必须是这个）
                                          port=self.server.local_bind_port,
                                          user="root",
                                          passwd="123456",
                                          db=self.dbname)  # 需要连接的数据库的名称

        try:
            # 使用cursor()方法获取操作游标
            cursor = self.db_connect.cursor()
            return cursor

        except Exception as data:
            print('Error: connected failed: %s' % data)

    def query(self, sql):
        """
        查询
        :param sql:sql语句
        :param cursor:处理类
        :return:查询结果
        """
        try:
            self.db_connect.commit()
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        except Exception as data:
            print('Error: query failed: %s' % data)

    def update(self, sql):
        """
        :param sql:
        :return:
        """
        try:
            self.cursor.execute(sql)
            self.db_connect.commit()
        except Exception as data:
            print('Error: update failed: %s' % data)

    def query_page(self, sql: str, pageNum: int):
        """

        :param sql:
        :return:
        """
        sql = sql + ' limit ' + str((pageNum - 1) * 5) + ',5'
        res = self.query(sql)
        returnStr = ''
        for row in res:
            for i in range(len(row) - 1):
                returnStr += row[i] + ' '
            returnStr += (row[-1] + '*')
        return returnStr

def trans_json(rv):
    payload = []
    content = {}
    for result in rv:
        for i,col in enumerate(result):
            content[str(i)] = result[i]
        payload.append(content)
        content = {}
    return payload

if __name__ == '__main__':
    user_account = '123456'
    sql_info = "select * from user"
    stat = DBConnector('record')
    info = stat.query(sql_info)
    if info is not None:
        data = trans_json(info)
        print(data)
    stat.close()
