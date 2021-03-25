import os
import socket
import threading
import time




class EthernetComm():

    def __init__(self, ip , port):

        self.ip = ip
        self.port = port
        self.deviceName = ''
        self.socket = None
        self.socketOpen = False

    def open(self):
        if self.socket is None:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.ip, self.port))
            self.socketOpen = True
        else:
            return False

    def close(self):
        if self.socket is not None:
            self.socket.close()
            self.socketOpen = False
        else:
            return False

    def sendData(self, content, type):
        if self.socket is not None and self.socketOpen:
            if isinstance(content, type):
                self.socket.sendto(bytes(content, 'utf-8'), (self.ip, self.port))

            else:
                return False
