import os
import socket
import threading
import time


datatypes_enum = [int, float, complex, list, tuple, range, str, dict,
                    bool, bytes, bytearray, memoryview, set, frozenset]



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
                content = '{' + str(datatypes_enum.index(type)) + ';' + content + '}'
                self.socket.sendto(bytes(content, 'utf-8'), (self.ip, self.port))

            else:
                return False

    def ErrorHandle(self, error):



        return (err, errorID)


    def receiveData(self):

        return True


    def getMachineInfo(self):


        return info
