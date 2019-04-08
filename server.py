# -*- coding: utf-8 -*-
import socketserver
import time
from DBserver import DBConnector

stat = DBConnector('record')


class TCPhandler(socketserver.BaseRequestHandler):
    def handle(self):
        while True:
            time.sleep(0.001)
            data = self.request.recv(4096).decode().strip()
            if not data or len(data) == 0:
                continue
            if data[-1] == "u":
                stat.update(data[0:-1])
            elif data[-1] == "q":
                if "user_records" in data:
                    returnData = self.getRecord(data[:-1])
                    self.request.sendall(returnData.encode())
                elif "drugs" in data:
                    returnData = self.getDrugsInfo(data[:-1])
                    self.request.sendall(returnData.encode())
                elif "user" in data:
                    returnData = self.getUserInfo(data[:-1])
                    self.request.sendall(returnData.encode())
            else:
                self.request.sendall((str({"result": "false", "infos": "[]"}).replace("'", '"') + "\n").encode())

    def getDrugsInfo(self, sql):
        res = stat.query(sql)
        if res is None or len(res[0]) != 6:
            return str({"result": "false", "infos": "[]"}).replace("'", '"') + "\n"
        else:
            result = "ok"
            infos = []
            for row in res:
                infos.append({"d_name": row[1], "d_productor": row[2], "d_description": row[3], "d_ean": row[0]})
        return str({"result": result, "infos": infos}).replace("'", '"') + "\n"

    def getUserInfo(self, sql):
        res = stat.query(sql)
        if res is None:
            return str({"result": "false", "infos": "[]"}).replace("'", '"') + "\n"
        else:
            result = "ok"
            infos = []
            for row in res:
                infos.append({"boxs_temp": row[3], "boxs_humidity": row[4], "user_state": row[5], "user_hr": row[6],
                              "user_spo2": row[7]})
        return str({"result": result, "infos": infos}).replace("'", '"') + "\n"
        res = stat.query(sql)
        if res is None:
            return str({"result": "false", "infos": "[]"}).replace("'", '"') + "\n"
        else:
            result = "ok"
            infos = []
            for row in res:
                infos.append({"d_ean": row[0], "date": row[1], "count": row[2], "user_account": row[3]})
        return str({"result": result, "infos": infos}).replace("'", '"') + "\n"
        
    def getRecord(self, sql):
        res = stat.query(sql)
        if res is None:
            return str({"result": "false", "infos": "[]"}).replace("'", '"') + "\n"
        else:
            result = "ok"
            infos = []
            for row in res:
                infos.append({"d_ean": row[0], "date": row[1], "count": row[2], "user_account": row[3]})
        return str({"result": result, "infos": infos}).replace("'", '"') + "\n"


host = ''
port = 12343
server = socketserver.ThreadingTCPServer((host, port), TCPhandler)
server.serve_forever()
