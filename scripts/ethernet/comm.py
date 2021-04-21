import socket
import serial
from threading import Thread, Lock
import time


datatypes_enum = [int, float, complex, list, tuple, range, str, dict,
                    bool, bytes, bytearray, memoryview, set, frozenset]

class SerialComm():

    def __init__(self, baud, port):
        self.port = port
        self.baud = baud
        self.serial = None

    def open(self):
        if not self.serial.is_open:
            self.serial = serial.Serial(self.port, self.baud, timeout=1)
        else:
            return False

    def close(self):
        if self.serial.is_open:
            self.serial.close()
        else:
            return False
            

    def sendData(self, content, type):

        if self.serial is not None and self.serial.is_open:
            if isinstance(content, type):
                content = '{' + str(datatypes_enum.index(type)) + ';' + content + '}'
                self.serial.write(bytes(content, 'utf-8'))
            else:
                return False



class EthernetComm():

    def __init__(self, ip , port):

        self.ip = ip
        self.port = port
        self.deviceName = ''
        self.socket = None
        self.socketOpen = False
        self.output_array = []
        self.commStream = None

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
        #Sends 'encoded' data to connected controller in the form:
        #{datatype;transmitted_data} where datatype is an enumerated value. Data sent as a string
        #to controller. BYTE_TO_datatype should be used in MWiec working file to properly store
        #transmitted data
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
        #Not sure how well this works yet. Needs testing
        if self.socket is not None and self.socketOpen:
            while True:
                data, addr = self.socket.recvfrom(4096)
                decoded_data = data.decode('utf-8')

                return decoded_data

    def getMachineInfo(self):
        self.sendData('MachineInfoRequest', str)





        return info

    def sendBoundingBox(self, box, confidence, label):
        #Bounding box in standard fractional format: [xmin, ymin, xmax, ymax] where values are a ratio of image width/height
        #We will be rounding the confidence to 4 decimal points
        #Label in as enumerated int values only (e.g. 0, 1, 2 where 0=dog, 1=cat, 3=person)
        if isinstance(label, int):
            outGoingData = '[{:.4f},{:.4f},{:.4f},{:.4f},{:.4f},{}]'.format(box[0], box[1], box[2], box[3], confidence, label)
            self.sendData(outGoingData, str)

    def openCommStream(self):
        #Opens comm streaming thread for continous transmission
        #Currently only supports single-box detector transmission
        if self.commStream is None:
            self.commStream = Thread(target=self.comm)
            self.commStream.start()
        return False


    def comm(self):
        while self.socket is not None and self.socketOpen:
            if self.output_array:
                with Lock():
                    self.sendBoundingBox(self.output_array[0], self.output_array[1], self.output_array[2])
                    self.output_array.clear()
        self.commStream = None
        return False
