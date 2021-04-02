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

    def wait(self):
        if self.socket is not None and self.socketOpen:
            while True:
                data, addr = self.socket.recvfrom(4096)
                decoded_data = data.decode('utf-8')

                return decoded_data

    def getMachineInfo(self):
        self.sendData('MachineInfoRequest', str)





        return info

    def sendBoundingBox(Self, box, confidence, label):
        #Bounding box in standard fractional format: [xmin, ymin, xmax, ymax] where values are a ratio of image width/height
        #We will be rounding the confidence to 4 decimal points
        #Label in as enumerated int values only (e.g. 0, 1, 2 where 0=dog, 1=cat, 3=person)
        if isinstance(label, int):
            outGoingData = '[{.4f},{.4f},{.4f},{.4f},{:.4f},{}]'.format(box[0], box[1], box[2], box[3], confidence, label)
            self.sendData(content, list)
