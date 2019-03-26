import serial
from DBProcessing import DBConnector
import time

user_account = '123465'

if __name__ == "__main__":
    ser = serial.Serial('ttyUSB0', 115200, timeout=0.5)
    tmp = ''
    if not ser.isOpen():
        print('serial failed')
    else:
        print('serial success')
        stat = DBConnector('record')  # choose database
        sql_query = "SELECT d_name,d_productor,d_description from user_drugs,drugs where user_account = '" + user_account + "' and user_drugs.d_ean = drugs.d_ean"
        while True:  # 系统持续运行
            data = ser.readline()
            if data != b'':
                print(data)  # debug
                if len(data) == 3:  # 查询固定页数的药品
                    returnStr = stat.query_page(sql_query, data[1])
                    ser.write(b'\xaa' + returnStr.encode('gb2312') + b'\x0d')
                if len(data) == 15:
                    ean = data[:14].decode()
                    durg_info = "select * from drugs where d_ean = '{}'".format(ean)
                    info = stat.query(comfirm_info)
                    sendtxt = info[1] + ' ' + info[2] + ' ' + info[3]
                    ser.write(b'\xbb' + sendtxt.encode('gb2312') + b'\x0d')
                    # 更新数据库
                    record_update = "INSERT into user_record VALUES('{}',CURDATE(),1,'{}') on DUPLICATE KEY UPDATE count = count +1".format(
                        info[0], user_account)
                    stat.update(record_update)
                if len(data) == 14:
                    # 返回确认信息
                    comfirm_info = "select * from drugs where d_ean = '{}'".format(data.decode())
                    info = stat.query(comfirm_info)
                    tmp = info[0]
                    sendtxt = info[1] + ' ' + info[2] + ' ' + info[3]
                    ser.write(b'\xbb' + sendtxt.encode('gb2312') + b'\x0d')
                if len(data) == 1:
                    if data[0] == 1:
                        sql_insert = "insert into user_drugs values ('" + user_account + "','" + tmp + "')"
                        stat.update(sql_insert)
            else:
                t = time.strftime('%H', time.localtime(time.time()))
                if t == '07' or t == '12' or t == '18':  # 定时吃药
                    ser.write(b'\xaa' + b'\x0d')
                print('no data')  # debug
