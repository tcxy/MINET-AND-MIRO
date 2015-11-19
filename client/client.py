#!/usr/bin/env python
# -*- coding:utf-8 -*-
#

import socket
import json

class TcpClient:
    HOST = "localhost"
    PORT = 12345
    BUFSIZ = 1024
    ADDR = (HOST, PORT)

    def __init__(self):
        self.isMIRO = False
        self.isLogin = False
        self.jdata = {}
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(self.ADDR)
        self.send_ack_msg()

    def send_ack_msg(self):
        ack_msg ='{"action": "handshake", "agent": "MINET"}'
        self.send_json(ack_msg)
        if self.jdata.get("server") != "MIRO":
            print "Server is not MIRO"
            self.client.close()
        else:
            self.isMIRO = True
            print "Connect to MIRO"

    def register(self, username, password, nickname):
        register_msg = '{"action": "register", "username": "%s", "password": "%s", "nickname": "%s"}' % (username, password, nickname)
        self.send_json(register_msg)
        if self.jdata.get("code") == "REGISTER_SUCCESS":
            print "Register success"
        else:
            print "Register fail, reason:", self.jdata.get("message")


    def login(self, username, password):
        register_msg = '{"action": "login", "username": "%s", "password": "%s"}' % (username, password)
        self.send_json(register_msg)
        if self.jdata.get("code") == "LOGIN_SUCCESS":
            self.isLogin = True
            print "Login success"
        else:
            print "Login fail, reason:", self.jdata.get("message")

    def start_query(self):
        while True:
            data = raw_input(">")
            if not data:
                break
            self.client.send(data.encode('utf8'))
            data = self.client.recv(self.BUFSIZ)
            if not data:
                break
            print data.decode('utf8')


    def send_json(self, message):
        try:
            print "Send: {}".format(message)
            self.client.sendall(message)
            response = self.client.recv(self.BUFSIZ)
            self.jdata = json.loads(response)
            print "Recv: ", self.jdata
        except Exception as e:
            print e


    def __exit__(self):
        self.client.send("EXIT")
        self.client.close()

if __name__ == "__main__":
    # Port 0 means to select an arbitrary unused port

    # msg1 = {'src':'hello', 'dst':"bar"}
    # jmsg1 = json.dumps(msg1)
    client = TcpClient()
    client.register('hhhh','hhhh','hhhh')
    client.login('hhhh','hhhh')
    # client.send_json(jmsg1)
    client.start_query()