#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from socket import *

HOST = '120.79.92.230'

PORT = 12343

BUFFSIZE = 4096

ADDR = (HOST, PORT)

tctimeClient = socket(AF_INET, SOCK_STREAM)

tctimeClient.connect(ADDR)

while True:
    data = input(">")
    if not data:
        break
    tctimeClient.send(data.encode())
    data = tctimeClient.recv(BUFFSIZE).decode()
    if not data:
        break
    print(data)
tctimeClient.close()
