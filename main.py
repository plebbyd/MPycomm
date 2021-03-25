from scripts.ethernet.comm import EthernetComm


if __name__ == '__main__':
    a = EthernetComm('192.168.207.78', 10000)
    a.open()
    print(isinstance('Hello World!', str))
    a.sendData('Hello World!', str)
